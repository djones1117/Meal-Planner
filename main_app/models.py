from django.db import models
#from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class ShoppingList(models.Model):
    item = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Recipe(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)



