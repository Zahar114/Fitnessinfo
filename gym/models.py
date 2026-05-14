from django.db import models


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено о")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено о")

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=100, verbose_name="Назва")
    muscle_group = models.ForeignKey(
        MuscleGroup,
        on_delete=models.CASCADE,
        related_name="exercises",
        verbose_name="Група м'язів"
    )
    description = models.TextField(verbose_name="Опис")
    difficulty = models.CharField(max_length=50, verbose_name="Складність")
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