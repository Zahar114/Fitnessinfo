from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('workouts/', views.workouts),
    path('nutrition/', views.nutrition),
]