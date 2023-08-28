import os
import uuid
import boto3
from .models import ShoppingList, Meal, Like
from .forms import  MealForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.formsets import formset_factory
# Create your views here.
from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

# Define the home view
@login_required
def home(request):
  meals = Meal.objects.all()
  return render(request, 'home.html', {
    'meals': meals
  })

@login_required
def shopping_list(request):
  return render(request, 'shopping_list.html')

@login_required
def meals_index(request):
  meals = Meal.objects.all()
  return render(request, 'meals/index.html', {
     'meals': meals
  }) 
  
@login_required
def meals_detail(request, meal_id):
  meal = Meal.objects.get(id=meal_id)
  like = Like.objects.filter(user_id=request.user.id, meal_id=meal_id)
  if (len(like)):
    button_msg = 'UNLIKE'
  else:
    button_msg = 'LIKE'
  return render(request, 'meals/detail.html', { 'meal' : meal, 'button' : button_msg })

def meals_delete(request, meal_id):
   meal = Meal.objects.get(id=meal_id)
   meal.delete()
   return redirect('index')

def meals_like(request, meal_id):
  like = Like.objects.filter(user_id=request.user.id, meal_id=meal_id)
  if (len(like)):
    like.delete()
  else:
    Like.objects.create(user_id=request.user.id, meal_id=meal_id)
  return redirect('detail', meal_id=meal_id)

class MealCreate(LoginRequiredMixin, CreateView):
  model = Meal
  fields = ['name', 'ingredients']

  def form_valid(self, form):
    photo_file = self.request.FILES.get('photo-file', None)
    if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = 'mealplanner/' + uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
          bucket = os.environ['BUCKET_NAME']
          s3.upload_fileobj(photo_file, bucket, key)
          # build the full url string
          url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
          # we can assign to meal_id or meal (if you have a meal object)
          form.instance.photo_url = url
      except Exception as e:
          print('An error occurred uploading file to S3')
          print(e)
    form.instance.user = self.request.user
    return super().form_valid(form)
  
class MealDelete(LoginRequiredMixin, DeleteView):
  model = Meal
  success_url = '/meals'






  

  


  



