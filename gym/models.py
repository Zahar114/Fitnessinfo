from django.db import models
from django.contrib.auth.models import User


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name


class Product(models.Model):
    image_url = models.URLField(verbose_name="Посилання на фото", blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name="Назва")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name="products", verbose_name="Категорія")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='products/', verbose_name="Фото", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name


class NutritionPlan(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    calories = models.IntegerField(verbose_name="Калорії")
    protein = models.IntegerField(verbose_name="Білки")
    description = models.TextField(verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name
    
class NewsletterSubscriber(models.Model):
    email = models.EmailField(verbose_name="Email")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")

    def __str__(self):
        return self.email


class ProductRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings", verbose_name="Товар")
    name = models.CharField(max_length=100, verbose_name="Ім’я")
    rating = models.IntegerField(verbose_name="Оцінка")
    comment = models.TextField(verbose_name="Коментар", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")

    def __str__(self):
        return f"{self.product.name} - {self.rating}"
    from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    products = models.ManyToManyField(Product, verbose_name="Товари")
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Сума")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")

    def __str__(self):
        return f"Замовлення #{self.id} - {self.user.username}"


class PasswordResetCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    code = models.CharField(max_length=6, verbose_name="Код")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")

    def __str__(self):
        return f"{self.user.username} - {self.code}"