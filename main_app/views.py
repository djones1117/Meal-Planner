from .models import ShoppingList, Meal
from .forms import  MealForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.formsets import formset_factory
# Create your views here.
from django.shortcuts import render

# Define the home view
def home(request):
  meals = Meal.objects.all()
  return render(request, 'home.html', {
    'meals': meals
  })

def shopping_list(request):
  return render(request, 'shopping_list.html')

def meals_index(request):
  meals = Meal.objects.all()
  return render(request, 'meals/index.html', {
     'meals': meals
  }) 
  

def meals_detail(request):
  return render(request, 'meals/detail.html')

class MealCreate(CreateView):
  model = Meal
  fields = ['name', 'ingredients']
  success_url = '/'

class MealDelete(DeleteView):
  model = Meal
  success_url = '/meals'



  

  


  



