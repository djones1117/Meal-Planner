from django.forms import ModelForm
from .models import Ingredient, Meal

class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'picture']

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['item']