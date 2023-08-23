from django.db import models
#from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class ShoppingList(models.Model):
    item = models.CharField(max_length=100)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)


class Meal(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField(max_length=500)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)


class Photo(models.Model):
    url = models.CharField(max_length=200)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for meal_id: {self.meal_id} @{self.url}"
    

    

