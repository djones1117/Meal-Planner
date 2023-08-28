from django.urls import path
from . import views

urlpatterns = [
  path('home/', views.home, name='home'),
  path('', views.landing, name='landing'),
  path('meals/', views.meals_index, name='index'),
  path('meals/create/', views.MealCreate.as_view(), name='meals_create'),
  path('accounts/signup/', views.signup, name='signup'),
  path('meals/<int:meal_id>/delete/', views.meals_delete, name="delete"),
  path('meals/<int:meal_id>/like/', views.meals_like, name="meals_like"),
]