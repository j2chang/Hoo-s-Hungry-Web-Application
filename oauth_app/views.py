from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic, View
from django.conf import settings
import googlemaps
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .import views
import logging
from django.shortcuts import render, redirect
from oauth_app.models import Reviews, Favorite
from .models import Category
from .models import myUser
from .forms import UserForm, EditUserForm, SurveyForm
import requests
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantFilterForm
import json
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# def index(request):
#     return HttpResponse("You're at the home page of the Restaurant Finder.")

def setupprofile(request):
    print("at edit profile view")
    try:
        newUser = myUser.objects.get(id=request.user.id)
        print("user already exists")
        if newUser.user_type == "u":
            return HttpResponseRedirect(reverse('userview'))
        else:
            return HttpResponseRedirect(reverse('adminview'))
    except:
        print("user does not exist yet")
        newUser = myUser(id=request.user.id, userName=str(request.user))
        django_user = User.objects.get(username=request.user)
        form = UserForm()
        context = {'form':form}
        if request.POST:
            form = UserForm(request.POST, instance=newUser)
            if form.is_valid():
                form.save()
                django_user.username = newUser.userName
                django_user.first_name = newUser.firstName
                django_user.last_name = newUser.lastName
                django_user.save()
                if newUser.user_type == "u":
                    return HttpResponseRedirect(reverse('userview'))
                else:
                    return HttpResponseRedirect(reverse('adminview'))
        return render(request, 'setupprofile.html', context)

def editprofile(request):
    activeUser = myUser.objects.get(id=request.user.id)
    django_user = User.objects.get(username=request.user)
    form = EditUserForm(instance=activeUser)
    context={'form':form}
    if request.POST:
        form = EditUserForm(request.POST, instance=activeUser)
        if form.is_valid():
            form.save()
            django_user.username = activeUser.userName
            django_user.first_name = activeUser.firstName
            django_user.last_name = activeUser.lastName
            django_user.save()
            if activeUser.user_type == "u":
                    return HttpResponseRedirect(reverse('userview'))
            else:
                    return HttpResponseRedirect(reverse('adminview'))
    return render(request, 'editprofile.html', context)




class loginVerificationView(generic.ListView):
    template_name = "loginVerification.html"
    def get_queryset(self):
        """
        Currently Empty.
        """
        return


class UserView(generic.ListView):
    template_name = "user.html"
    def get_queryset(self):
        """
        Currently Empty.
        """
        return

class restuarantAdminView(generic.ListView):
    template_name = "restaurantAdmin.html"
    def get_queryset(self):
        """
        Currently Empty.
        """
        return

class welcomeView(generic.ListView):
    template_name = "welcome.html"
    def get_queryset(self):
        """
        Currently Empty.
        """
        return

class welcomeAdminView(generic.ListView):
    template_name = "welcomeAdmin.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activeUser = myUser.objects.get(id=self.request.user.id)
        context['usertype'] = activeUser.user_type
        return context

    def get_queryset(self):
        """
        Currently Empty.
        """
        return

def surveyView(request):
    activeUser = myUser.objects.get(id=request.user.id)
    form = SurveyForm(instance=activeUser)
    context={'form':form}
    if request.POST:
        # form but we have some of the info filled out
        form = SurveyForm(request.POST, instance=activeUser)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('userview'))
    return render(request, 'survey.html', context)
    def get_queryset(self):
        """
        Currently Empty.
        """
        return

class CategoriesView(generic.ListView):
    template_name = "categories.html"
    context_object_name = "categories"

    def get_queryset(self):
        """
        Return the list of categories.
        """
        return Category.objects.all()

# class dummyView(generic.ListView):
#     template_name = "dummyRestaurant.html"
#     context_object_name = "Reviews"  # Set the context object name for the template
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         # Calculate the average rating
#         context['average'] = Star.objects.aggregate(Avg('rating'))['rating__avg']
#         return context
#
#     def get_queryset(self):
#         """
#         Get the queryset for displaying reviews.
#         """
#         return Reviews.objects.all()

class dummyView(generic.ListView):
    template_name = "dummyRestaurant.html"
    context_object_name = "Reviews"  # Set the context object name for the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        # Check if 'place_id' is present in kwargs
        place_id = kwargs.get('place_id')
        if place_id:
            # Calculate the average rating
            ratings = Star.objects.filter(place_id=place_id)
            context['average'] = ratings.aggregate(Avg('rating'))['rating__avg']

        return context

    def get_queryset(self):
        """
        Get the queryset for displaying reviews.
        """
        return Reviews.objects.all()


class restaurantPageView(generic.ListView):
    template_name = "restaurantPage.html"
    context_object_name = "Reviews"  # Set the context object name for the template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activeUser = myUser.objects.get(id=self.request.user.id)
        restaurant = get_object_or_404(Restaurant, place_id=self.kwargs['place_id'])
        #print(f"Debug (restaurantPageView): {restaurant.place_id}")
        # Calculate the average rating
        context['restaurant_id'] = restaurant.id
        context['average'] = Star.objects.filter(place_id=restaurant.place_id).aggregate(Avg('rating'))['rating__avg']
        context['restaurant_name'] = restaurant.name
        context['restaurant_address'] = restaurant.address
        context['place_id'] = restaurant.place_id
        context['user_type'] = activeUser.user_type
        context['latitude'] = restaurant.latitude
        context['longitude'] = restaurant.longitude

        return context



    def get_queryset(self):
        """
        Get the queryset for displaying reviews.
        """
        restaurant = get_object_or_404(Restaurant, place_id=self.kwargs['place_id'])
        return Reviews.objects.filter(place_id=restaurant.place_id)



def map(request):
    key = settings.GOOGLE_MAPS_API_KEY
    context = {
        'key':key,
    }
    query_param = request.GET.get('q')
    if query_param is not None:
        gmaps = googlemaps.Client(key=key)
        location = 'near me'
        if 'vegetarian' in query_param:
            keyword = 'vegetarian restaurant'
            types = ['restaurant', 'meal_takeaway']
            places = gmaps.places(query=keyword, location=location, type=types)
            return render(request, 'vegetarian_map.html', {'filtered_restaurants': places})
    else:
        place_id = request.GET.get('place_id')

        ratings = Star.objects.filter(place_id=place_id)
        average = ratings.aggregate(Avg('rating'))['rating__avg']
        context['average'] = average
        context['place_id'] = place_id

        return render(request, 'map.html', context)

def surveymap(request):
    key = settings.GOOGLE_MAPS_API_KEY
    context = {
        'key':key,
    }
    query_param = request.GET.get('q')
    if query_param is not None:
        gmaps = googlemaps.Client(key=key)
        location = 'near me'
        if 'vegetarian' in query_param:
            keyword = 'vegetarian restaurant'
            types = ['restaurant', 'meal_takeaway']
            places = gmaps.places(query=keyword, location=location, type=types)
            return render(request, 'vegetarian_map.html', {'filtered_restaurants': places})
    else:
        place_id = request.GET.get('place_id')

        ratings = Star.objects.filter(place_id=place_id)
        average = ratings.aggregate(Avg('rating'))['rating__avg']
        context['average'] = average
        context['place_id'] = place_id

        return render(request, 'surveyMap.html', context)

def login(request):
    return render(request, 'index.html')


class adminVerification(generic.ListView):
    template_name = "adminVerification.html"

    def get_queryset(self):
        """
        Currently Empty.
        """
        return


class viewReviews(generic.ListView):
    template_name = "seeReviews.html"
    context_object_name = "Reviews"
    def get_context_data(self, **kwargs):
        print("Debug: Inside get_context_data")
        context = super().get_context_data(**kwargs)

        # Get the restaurant object based on the place_id from the URL
        restaurant = get_object_or_404(Restaurant, place_id=self.kwargs['place_id'])
        print(f"Debug: {restaurant.place_id}")


        # Include the restaurant object and ID in the context
        context['restaurant'] = restaurant
        context['place_id'] = restaurant.place_id
        return context

    def get_queryset(self):
        # Filter reviews based on the current restaurant's ID
        return Reviews.objects.filter(place_id=self.kwargs['place_id'])

def newReview(request, place_id):
    review_text = request.POST['Review']
    pub_date = timezone.now()
    user = request.user
    restaurant = get_object_or_404(Restaurant, place_id=place_id)
    r = Reviews(review_text=review_text, pub_date=pub_date, user=user, is_approved=False, place_id=restaurant)
    r.save()
    return HttpResponseRedirect('/restaurantPage/' + place_id + '/')

class commentApprovalView(generic.ListView):
    template_name = "commentApproval.html"
    context_object_name = "Reviews"  # Set the context object name for the template
    def get_queryset(self):
        """
        Get the queryset for displaying reviews.
        """
        return Reviews.objects.all().order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activeUser = myUser.objects.get(id=self.request.user.id)
        context['usertype'] = activeUser.user_type
        for review in context['Reviews']:
            review.restaurant_name = review.place_id.name
        return context


def approveReview(request, review_id):
    context_object_name = "Reviews"
    review = Reviews.objects.get(pk=review_id)
    review.is_approved = True
    review.is_reviewed = True
    review.save()
    return redirect('/commentApproval/')

def rejectReview(request, review_id):
    context_object_name = "Reviews"
    activeUser = myUser.objects.get(id=request.user.id)
    print(activeUser.user_type)
    activeUser = myUser.objects.get(id=request.user.id)
    usertype = activeUser.user_type
    review = Reviews.objects.get(pk=review_id)
    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason')
        if rejection_reason:
            review.status = 'Your review was rejected by admins because: "' + rejection_reason + '"'
            review.is_reviewed = True
            review.save()
            return redirect('/commentApproval/')
   

    # Render the rejection form template
    return render(request, 'rejectionForm.html', {'review': review, 'usertype': activeUser.user_type})
    

def acknowledgeRejection(request, review_id, place_id):
    review = Reviews.objects.get(pk=review_id)
    review.is_rejection_acknowledged = True
    review.save()
    review.delete()
    return redirect('/restaurantPage/' + place_id + '/')


from .models import Star

# def add_rating(request, place_id):
#     if request.method == 'POST':
#         rating = request.POST.get('rating')
#         if rating:
#             restaurant = get_object_or_404(Restaurant, place_id=place_id)
#             Star.objects.create(rating=rating, place_id=restaurant)
#             return redirect('/restaurantPage/' + place_id + '/')
#     restaurant = get_object_or_404(Restaurant, place_id=place_id)
#     restaurant_name = restaurant.name
#
#     return render(request, 'add_rating.html', {'place_id': place_id, 'restaurant_name': restaurant_name})

# def add_rating(request, place_id):
#     if request.method == 'POST':
#         rating = request.POST.get('rating')
#         if rating:
#             restaurant = get_object_or_404(Restaurant, place_id=place_id)
#             Star.objects.create(rating=rating, place_id=restaurant)
#             return redirect('restaurantPage', place_id=place_id)
#
#     restaurant = get_object_or_404(Restaurant, place_id=place_id)
#     restaurant_name = restaurant.name
#
#     return render(request, 'add_rating.html', {'place_id': place_id, 'restaurant_name': restaurant_name})

def add_rating(request, place_id):
    if request.method == 'POST':
        rating = request.POST.get('rating')
        if rating:
            restaurant = get_object_or_404(Restaurant, place_id=place_id)
            Star.objects.create(rating=rating, place_id=restaurant)
            return redirect('restaurantPage', place_id=place_id)

    restaurant = get_object_or_404(Restaurant, place_id=place_id)
    restaurant_name = restaurant.name

    return render(request, 'add_rating.html', {'place_id': place_id, 'restaurant_name': restaurant_name})


def average_rating(request, place_id):
    ratings = Star.objects.filter(place_id=place_id)
    average = ratings.aggregate(Avg('rating'))['rating__avg']

    restaurant = get_object_or_404(Restaurant, place_id=place_id)
    restaurant_name = restaurant.name

    context = {
        'average': average,
        'place_id': place_id,
        'restaurant_name': restaurant_name,
    }

    return render(request, 'average_rating.html', context)

def filter_restaurants(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Extract parameters from the request
        zip_code = request.GET.get('zip_code', '')
        star_rating = request.GET.get('star_rating', '')
        cuisine_type = request.GET.get('cuisine_type', '')
        price_range = request.GET.get('price_range', '')

        print('cuisine_type' + cuisine_type)

        # Build the Google Places API URL
        api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'key': 'AIzaSyDanA6l1HRqKXW2s_ILjBelO5iLF9ZShsc',
            'location': '38.0336,-78.5080',  # HARDCODED
            'radius': '5000',  # Define the radius in meters
            'type': 'restaurant',
            'keyword': cuisine_type
            # Add other parameters as needed
        }

        # Make the API request
        response = requests.get(api_url, params=params)

        # Handle the response
        if response.status_code == 200:
            response_data = response.json()
            restaurant_names = [place['name'] for place in response_data.get('results', [])]

            # Print the list of restaurant names
            print("Filtered Restaurants:", json.dumps(restaurant_names, indent=4))
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Failed to fetch data from Google Places API'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

def filter_survey(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        cuisine_type = ''

        activeUser = myUser.objects.get(id=request.user.id)
        if activeUser.vegetarian_food:
            cuisine_type = '(vegetarian food)'
        if activeUser.american_food and cuisine_type != "":
            cuisine_type = cuisine_type + "|(american food)"
        elif activeUser.american_food:
            cuisine_type = '(american food)'
        if activeUser.mexican_food and cuisine_type != "":
            cuisine_type = cuisine_type + "|(mexican food)"
        elif activeUser.mexican_food:
            cuisine_type = '(mexican food)'
        if activeUser.asian_food and cuisine_type != "":
            cuisine_type = cuisine_type + "|(asian food)"
        elif activeUser.asian_food:
            cuisine_type = '(asian food)'
        if activeUser.fast_food and cuisine_type != "":
            cuisine_type = cuisine_type + "|(fast food)"
        elif activeUser.fast_food:
            cuisine_type = '(fast food)'
        if activeUser.dessert_food and cuisine_type != "":
            cuisine_type = cuisine_type + "|(dessert)"
        elif activeUser.dessert_food:
            cuisine_type = '(dessert)'
        if activeUser.mediterranean_food and cuisine_type != "":
            cuisine_type = cuisine_type + "|(mediterranean food)"
        elif activeUser.mediterranean_food:
            cuisine_type = '(mediterranean food)'

        print('cuisine_type' + cuisine_type)

        # Build the Google Places API URL
        api_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            'key': 'AIzaSyDanA6l1HRqKXW2s_ILjBelO5iLF9ZShsc',
            'location': '38.0336,-78.5080',  # HARDCODED
            'radius': '5000',  # Define the radius in meters
            'type': 'restaurant',
            'keyword': cuisine_type
            # Add other parameters as needed
        }

        # Make the API request
        response = requests.get(api_url, params=params)

        # Handle the response
        if response.status_code == 200:
            response_data = response.json()
            restaurant_names = [place['name'] for place in response_data.get('results', [])]

            # Print the list of restaurant names
            print("Filtered Restaurants:", json.dumps(restaurant_names, indent=4))
            return JsonResponse(response.json())
        else:
            return JsonResponse({'error': 'Failed to fetch data from Google Places API'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


def addRestaurant(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        place_id = request.POST.get('place_id')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        # Extract other relevant data from the request

        # Save the restaurant to the database
        new_restaurant = Restaurant(name=name, place_id=place_id, address=address, latitude=latitude, longitude=longitude)
        new_restaurant.save()

        return JsonResponse({'id': new_restaurant.id, 'name': new_restaurant.name, 'place_id': new_restaurant.place_id
                             , 'address': new_restaurant.address, 'latitude': new_restaurant.latitude, 'longitude': new_restaurant.longitude,})

    return JsonResponse({'error': 'Invalid request method'})

class CheckRestaurantView(View):
    def get(self, request, *args, **kwargs):
        place_id = request.GET.get('place_id')
        restaurant = Restaurant.objects.filter(place_id=place_id).first()

        if restaurant:
            data = {
                'exists': True,
                'restaurant': {
                    'name': restaurant.name,
                    'place_id': restaurant.place_id,
                    # Include other fields you need
                }
            }
        else:
            data = {'exists': False}

        return JsonResponse(data)

def restaurant_list(request):
    activeUser = myUser.objects.get(id=request.user.id)
    usertype = activeUser.user_type
    restaurants = Restaurant.objects.order_by('name')
    return render(request, 'restaurant_list.html', {'restaurants': restaurants, 'usertype': activeUser.user_type})


def restPageMapView(request):
    key = settings.GOOGLE_MAPS_API_KEY
    context = {
        'key':key,
    }
    return render(request, 'restPageMap.html', context)

@login_required
def add_to_favorites(request, restaurant_id):
    if request.user.is_authenticated:
        # Access an attribute to trigger the evaluation of SimpleLazyObject
        my_user = get_my_user_instance(request)  # You need to implement this
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        Favorite.objects.get_or_create(user=my_user, restaurant=restaurant)
        return redirect('favorites')
    else:
        # Redirect to login page or give an appropriate response for unauthenticated users
        return redirect('login')

def remove_from_favorites(request, restaurant_id):
    my_user = get_my_user_instance(request)  # You need to implement this
    Favorite.objects.filter(user=my_user, restaurant_id=restaurant_id).delete()
    return redirect('favorites')

def get_my_user_instance(request):
    # Implement logic to retrieve myUser instance based on request
    # This could be based on session data, a cookie, or some other method
    print(myUser.objects.get(id=request.user.id))
    return myUser.objects.get(id=request.user.id)

def favorites(request):
    my_user = get_my_user_instance(request)  # You need to implement this
    favorites = Favorite.objects.filter(user=my_user).select_related('restaurant')
    return render(request, 'favorites.html', {'favorites': favorites})

