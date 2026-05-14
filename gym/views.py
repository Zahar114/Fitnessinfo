from django.shortcuts import render
from .models import MuscleGroup, Exercise, NutritionPlan


def home(request):
    muscle_groups = MuscleGroup.objects.all()
    exercises = Exercise.objects.all()
    nutrition_plans = NutritionPlan.objects.all()

    context = {
        'title': 'Fitness Info',
        'muscle_groups': muscle_groups,
        'exercises': exercises,
        'nutrition_plans': nutrition_plans,
    }

    return render(request, 'gym/home.html', context)


def category_exercises(request, category_id):
    muscle_groups = MuscleGroup.objects.all()
    category = MuscleGroup.objects.get(id=category_id)
    exercises = Exercise.objects.filter(muscle_group=category)

    context = {
        'title': category.name,
        'muscle_groups': muscle_groups,
        'category': category,
        'exercises': exercises,
    }

    return render(request, 'gym/category.html', context)


def nutrition(request):
    muscle_groups = MuscleGroup.objects.all()
    nutrition_plans = NutritionPlan.objects.all()

    context = {
        'title': 'Харчування',
        'muscle_groups': muscle_groups,
        'nutrition_plans': nutrition_plans,
    }

    return render(request, 'gym/nutrition.html', context)
def workouts(request):
    muscle_groups = MuscleGroup.objects.all()
    exercises = Exercise.objects.all()
    
    context = {
        'title': 'Тренування',
        'muscle_groups': muscle_groups,
        'exercises': exercises,
    }
    return render(request, 'gym/workouts.html', context)