import os
import uuid
import boto3
from .models import Meal, Like
from django.views.generic.edit import CreateView, DeleteView
from django.forms.formsets import formset_factory

# Create your views here.
from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Definign the sign up page
def signup(request):
    error_message = ""
    if request.method == "POST":
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect("index")
        else:
            error_message = "Invalid sign up - try again"
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {"form": form, "error_message": error_message}
    return render(request, "registration/signup.html", context)


# Defining the landing page
def landing(request):
    return render(request, "landing.html")

# Defining the home page that will show all of the posts in the database
@login_required
def home(request):
    # Grabbing all of the meals in the database
    meals = Meal.objects.all()
    # Sorting the meals by reversed id (last one created will show first)
    meals = meals.order_by('-id')
    for meal in meals:
        # Checking if there is a meal that has been liked by the logged in user and assigning a boolean value to a new variable in the meal dictionary
        meal.user_liked = Like.objects.filter(user=request.user, meal=meal).exists()
    return render(request, "home.html", {"meals": meals})

# Defining the meals index page that will show all of the posts related to the logged in user
@login_required
def meals_index(request):
    # Grabbing all of the meals that the logged in user has created
    meals = Meal.objects.filter(user=request.user)
    liked_meal_ids = Like.objects.filter(user=request.user).values_list('meal_id', flat=True)
    # Grabbing all of the meals that have been liked by the logged in user
    liked_meals = Meal.objects.filter(id__in=liked_meal_ids)
    # Attaching both lists and sorting their data so the last one created shows first
    meals = (meals | liked_meals).order_by('-id')
    for meal in meals:
        meal.user_liked = Like.objects.filter(user=request.user, meal=meal).exists()
    return render(request, "meals/index.html", {"meals": meals})

# Defining the function that will delete a meal from the database
def meals_delete(request, meal_id):
    # Getting the meal to delete from the database by its id
    meal = Meal.objects.get(id=meal_id)
    # Removing such meal from the database
    meal.delete()
    return redirect("index")

# Defining the function that will allow the user to "like" or "unlike" a meal
def meals_like(request, meal_id):
  # Assigning the URL we're currently at to a variable
  referer = request.META.get('HTTP_REFERER')
  # Filtering the meal to "like"/"unlike" from the database (this will create a query set with the corresponding instance of the Like model if it finds one, or else the set will be empty)
  like = Like.objects.filter(user_id=request.user.id, meal_id=meal_id)
  # Checking if the list from the query set is empty or not
  if (len(like)):
    # If the instance is found in the query set, then remove it from the database (that means that the user wants to "unlike" the meal)
    like.delete()
  else:
    # If the list from the query set is empty (its length is 0), that means that the meal isn't liked by the logged in user yet so it will create a new intance of the Like Model (that means the user wants to "like" the meal)
    Like.objects.create(user_id=request.user.id, meal_id=meal_id)
  return redirect(referer, meal_id=meal_id)

# Defining the class that will create the meals
class MealCreate(LoginRequiredMixin, CreateView):
    model = Meal
    fields = ["name", "ingredients"]
    # Defining the form the user has to fill to create the meal
    def form_valid(self, form):
        photo_file = self.request.FILES.get("photo-file", None)
        if photo_file:
            s3 = boto3.client("s3")
            # need a unique "key" for S3 / needs image file extension too
            key = (
                "mealplanner/"
                + uuid.uuid4().hex[:6]
                + photo_file.name[photo_file.name.rfind(".") :]
            )
            # just in case something goes wrong
            try:
                bucket = os.environ["BUCKET_NAME"]
                s3.upload_fileobj(photo_file, bucket, key)
                # build the full url string
                url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
                # we can assign to meal_id or meal (if you have a meal object)
                form.instance.photo_url = url
            except Exception as e:
                print("An error occurred uploading file to S3")
                print(e)
        # Assigning the logged in user as the creator of that intance of the Meal model
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    # Every time a meal is created, send the user to the home page
    success_url = '/home'

# Defining the class that will delete the meals
class MealDelete(LoginRequiredMixin, DeleteView):
    model = Meal

    # Every time a meal is created, send the user to the meals index page
    success_url = '/meals'