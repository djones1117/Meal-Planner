from django.contrib import admin
from .models import ShoppingList, Meal
# Register your models here.

admin.site.register(ShoppingList)
admin.site.register(Meal)
