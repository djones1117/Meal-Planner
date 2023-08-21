from .models import ShoppingList, Meal, Ingredient

# Create your views here.
from django.shortcuts import render

# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def shopping_list(request):
  return render(request, 'shopping_list.html')

def meals_index(request):
  return render(request, 'meals/index.html') 

def meals_detail(request):
  return render(request, 'meals/detail.html')

