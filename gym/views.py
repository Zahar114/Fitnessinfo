from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product, NutritionPlan


def home(request):
    categories = ProductCategory.objects.all()
    products = Product.objects.all()[:6]

    return render(request, 'gym/home.html', {
        'title': 'FitShop',
        'categories': categories,
        'products': products,
    })


def category_products(request, category_id):
    categories = ProductCategory.objects.all()
    category = get_object_or_404(ProductCategory, id=category_id)
    products = Product.objects.filter(category=category)

    return render(request, 'gym/category.html', {
        'title': category.name,
        'categories': categories,
        'category': category,
        'products': products,
    })


def product_detail(request, product_id):
    categories = ProductCategory.objects.all()
    product = get_object_or_404(Product, id=product_id)

    return render(request, 'gym/product_detail.html', {
        'title': product.name,
        'categories': categories,
        'product': product,
    })


def nutrition(request):
    categories = ProductCategory.objects.all()
    nutrition_plans = NutritionPlan.objects.all()

    return render(request, 'gym/nutrition.html', {
        'title': 'Харчування',
        'categories': categories,
        'nutrition_plans': nutrition_plans,
    })