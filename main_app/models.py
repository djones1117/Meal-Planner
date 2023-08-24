from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class ShoppingList(models.Model):
    item = models.CharField(max_length=100)
    #user = models.ForeignKey(User, on_delete=models.CASCADE)


class Meal(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.TextField(max_length=500)
    photo_url = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'meal_id': self.id})

    

    

