from django.contrib import admin
from .models import ShoppingList, Meal, Like
# Register your models here.

admin.site.register(ShoppingList)
admin.site.register(Meal)
admin.site.register(Like)
