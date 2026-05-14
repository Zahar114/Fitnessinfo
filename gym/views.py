from django.shortcuts import render


def home(request):
    context = {
        'title': 'Fitness Info'
    }

    return render(request, 'gym/home.html', context)


def workouts(request):
    context = {
        'title': 'Тренування',
        'description': 'Тут знаходяться тренування для всіх груп м’язів.'
    }

    return render(request, 'gym/workouts.html', context)


def nutrition(request):
    context = {
        'title': 'Харчування',
        'description': 'Правильне спортивне харчування для спортсменів.'
    }

    return render(request, 'gym/nutrition.html', context)