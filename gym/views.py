from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
import random

from .models import (
    ProductCategory,
    Product,
    NewsletterSubscriber,
    ProductRating,
    Order,
    PasswordResetCode,
)


def get_common_context():
    return {
        "categories": ProductCategory.objects.all()
    }


def home(request):
    context = get_common_context()
    context["title"] = "FitShop"
    context["products"] = Product.objects.all()

    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            return redirect("home")

    return render(request, "gym/home.html", context)


def category_products(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)

    context = get_common_context()
    context["title"] = category.name
    context["category"] = category
    context["products"] = Product.objects.filter(category=category)

    return render(request, "gym/category.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        name = request.POST.get("name")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if name and rating:
            ProductRating.objects.create(
                product=product,
                name=name,
                rating=int(rating),
                comment=comment
            )
            return redirect("product_detail", product_id=product.id)

    context = get_common_context()
    context["title"] = product.name
    context["product"] = product
    context["average_rating"] = product.ratings.aggregate(Avg("rating"))["rating__avg"]

    return render(request, "gym/product_detail.html", context)


def add_to_cart(request, product_id):
    cart = request.session.get("cart", [])
    cart.append(product_id)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", [])

    if product_id in cart:
        cart.remove(product_id)

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def cart(request):
    cart_items = request.session.get("cart", [])
    products = Product.objects.filter(id__in=cart_items)

    context = get_common_context()
    context["title"] = "Кошик"
    context["products"] = products
    context["total"] = sum(product.price for product in products)

    return render(request, "gym/cart.html", context)


@login_required
def create_order(request):
    cart_items = request.session.get("cart", [])
    products = Product.objects.filter(id__in=cart_items)

    if products.exists():
        total = sum(product.price for product in products)

        order = Order.objects.create(
            user=request.user,
            total=total
        )

        order.products.set(products)

        request.session["cart"] = []
        request.session.modified = True

    return redirect("profile")


def register_view(request):
    context = get_common_context()
    context["title"] = "Реєстрація"

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if username and email and password:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            return redirect("profile")

    return render(request, "gym/register.html", context)


def login_view(request):
    context = get_common_context()
    context["title"] = "Вхід"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("profile")

        context["error"] = "Неправильний логін або пароль"

    return render(request, "gym/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def profile(request):
    context = get_common_context()
    context["title"] = "Особистий кабінет"

    if request.user.is_staff:
        context["orders"] = Order.objects.all().order_by("-created_at")
    else:
        context["orders"] = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "gym/profile.html", context)


def password_reset_request(request):
    context = get_common_context()
    context["title"] = "Відновлення пароля"

    if request.method == "POST":
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user:
            code = str(random.randint(100000, 999999))

            PasswordResetCode.objects.create(
                user=user,
                code=code
            )

            send_mail(
                "Код для відновлення пароля",
                f"Ваш тимчасовий код: {code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            request.session["reset_user_id"] = user.id
            return redirect("password_reset_confirm")

        context["error"] = "Користувача з таким email не знайдено"

    return render(request, "gym/password_reset_request.html", context)


def password_reset_confirm(request):
    context = get_common_context()
    context["title"] = "Зміна пароля"

    user_id = request.session.get("reset_user_id")

    if not user_id:
        return redirect("password_reset_request")

    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        code = request.POST.get("code")
        new_password = request.POST.get("new_password")

        reset_code = PasswordResetCode.objects.filter(
            user=user,
            code=code
        ).last()

        if reset_code and new_password:
            user.password = make_password(new_password)
            user.save()

            PasswordResetCode.objects.filter(user=user).delete()

            return redirect("login")

        context["error"] = "Неправильний код"

    return render(request, "gym/password_reset_confirm.html", context)