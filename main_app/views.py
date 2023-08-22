from .models import ShoppingList, Meal, Ingredient
from .forms import IngredientForm, MealForm
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
  return render(request, 'meals/index.html') 

def meals_detail(request):
  return render(request, 'meals/detail.html')

def add_meal(request):
    IngredientFormSet = formset_factory(IngredientForm, validate_min=True)
    if request.method == 'POST':
        form = MealForm(request.POST)
        formset = IngredientFormSet(request.POST)
        if all([form.is_valid(), formset.is_valid()]):
            meal = form.save()
            for inline_form in formset:
                if inline_form.cleaned_data:
                    ingredient = inline_form.save(commit=False)
                    ingredient.meal_id = meal.id
                    ingredient.save()
            return render(request, 'meals/index.html', {})
    else:
        form = MealForm()
        formset = IngredientFormSet()

    return render(request, 'meals/add_meal.html', {'form': form,'formset': formset})
  

  


  



