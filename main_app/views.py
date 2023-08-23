import os
import uuid
import boto3
from .models import ShoppingList, Meal, Photo
from .forms import  MealForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.formsets import formset_factory
# Create your views here.
from django.shortcuts import render, redirect

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
  

def meals_detail(request, meal_id):
  meal = Meal.objects.get(id=meal_id)
  return render(request, 'meals/detail.html', { 'meal' : meal })

def add_photo(request, meal_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # we can assign to meal_id or meal (if you have a meal object)
            Photo.objects.create(url=url, meal_id=meal_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
  return redirect('detail', meal_id=meal_id)

class MealCreate(CreateView):
  model = Meal
  fields = ['name', 'ingredients']
  success_url = '/'

class MealDelete(DeleteView):
  model = Meal
  success_url = '/meals'




  

  


  



