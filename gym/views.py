from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from .models import ProductCategory, Product, NewsletterSubscriber, ProductRating


def get_common_context():
    return {
        "categories": ProductCategory.objects.all()
    }


def home(request):
    context = get_common_context()
    context["title"] = "FitShop"
    context["products"] = Product.objects.annotate(avg_rating=Avg("ratings__rating"))

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
    context["products"] = Product.objects.filter(category=category).annotate(avg_rating=Avg("ratings__rating"))

    return render(request, "gym/category.html", context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = get_common_context()

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