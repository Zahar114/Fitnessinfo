from django.contrib import admin
from .models import MuscleGroup, Exercise, NutritionPlan


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'muscle_group', 'created_at', 'updated_at')
    search_fields = ('name', 'muscle_group__name')
    list_filter = ('muscle_group',)


@admin.register(NutritionPlan)
class NutritionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'calories', 'protein', 'created_at', 'updated_at')
    search_fields = ('name',)