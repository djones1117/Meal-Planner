from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('shoppinglist/', views.shopping_list, name='shopping_list' ),
  path('meals/', views.meals_index, name='index'),
  path('meals/<int:meal_id>/', views.meals_detail, name='detail'),
  path('meals/create/', views.add_meal, name='meals_create'),
]