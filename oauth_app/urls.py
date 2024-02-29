"""
URL configuration for project_a_11 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from oauth_project.project_a_11 import settings
from django.contrib import admin
from . import views
from django.urls import include, path
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import CheckRestaurantView, restaurant_list

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('setupprofile/', views.setupprofile, name='setupprofile'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('accounts/', include('allauth.urls')),
    path('user/', views.UserView.as_view(), name='userview'),
    path('restaurantAdmin/', views.restuarantAdminView.as_view()),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('welcome/', views.welcomeView.as_view(), name='welcomeview'),
    path('survey/', views.surveyView, name='surveyview'),
    path('surveymap/', views.surveymap, name='surveymap'),
    path('filter-survey/', views.filter_survey, name='filter_survey'),
    path('categories/', views.CategoriesView.as_view(), name='categories'),
    path('map/', views.map, name="map"),
    path('dummy/', views.dummyView.as_view(), name='dummy'),
    path('login/', views.login, name='login'),
    path('adminVerification/', views.adminVerification.as_view()),
    path('dummy/<str:place_id>/', views.dummyView.as_view(), name='dummy'),
    path('restaurantPage/<str:place_id>/', views.restaurantPageView.as_view(), name='restaurantPage'),
    path('loginVerification/', views.loginVerificationView.as_view()),
    path('newreview/<str:place_id>/', views.newReview, name='newreview'),
    path('reviews/<str:place_id>/', views.viewReviews.as_view(), name='viewreviews'),
    path('welcomeAdmin/', views.welcomeAdminView.as_view(), name='adminview'),
    path('commentApproval/', views.commentApprovalView.as_view(), name = 'approveReview'),
    path('commentApproval/<int:review_id>/', views.approveReview, name='approveReview'),
    path('rejectReview/<int:review_id>/', views.rejectReview, name='rejectReview'),
    path('acknowldgeRejection/<int:review_id>/<str:place_id>/', views.acknowledgeRejection, name='acknowledgeRejection'),
    path('add_rating/<str:place_id>/', views.add_rating, name='add_rating'),

    path('average_rating/<str:place_id>/', views.average_rating, name='average_rating'),
    path('filter-restaurants/', views.filter_restaurants, name='filter_restaurants'),
    path('addRestaurant/', views.addRestaurant, name='addRestaurant'),
    path('checkRestaurant/', CheckRestaurantView.as_view(), name='checkRestaurant'),
    path('restaurant_list/', restaurant_list, name='restaurant_list'),
    path('restPageMap/', views.restPageMapView, name="restPageMap"),
    path('add-to-favorites/<int:restaurant_id>/', views.add_to_favorites, name='add-to-favorites'),

    path('remove-from-favorites/<int:restaurant_id>/', views.remove_from_favorites, name='remove-from-favorites'),
    path('favorites/', views.favorites, name='favorites'),

]

