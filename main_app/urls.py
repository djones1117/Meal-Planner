from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('shoppinglist/', views.shopping_list, name='shopping_list' ),
  path('meals/', views.meals_index, name='index'),
  path('meals/<int:meal_id>/', views.meals_detail, name='detail'),
  path('meals/<int:meal_id>/add_photo/', views.add_photo, name='add_photo'),
  path('meals/create/', views.MealCreate.as_view(), name='meals_create'),
  path('accounts/signup/', views.signup, name='signup'),
  path('meals/<int:meal_id>/delete/', views.meals_delete, name="delete"),
]