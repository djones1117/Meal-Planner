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
    picture = models.CharField(max_length=200)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Ingredient(models.Model):
    item = models.CharField(max_length=100)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    

