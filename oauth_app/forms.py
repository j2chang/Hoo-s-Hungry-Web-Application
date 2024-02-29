from django.forms import ModelForm
from django import forms
from .models import myUser

class UserForm(ModelForm):
    class Meta:
        model = myUser
        fields = ['email', 'userName', 'firstName', 'lastName', 'user_type',]

class EditUserForm(ModelForm):
    class Meta:
        model = myUser
        fields = ['email', 'userName', 'firstName', 'lastName',]

class RestaurantFilterForm(forms.Form):
    zip_code = forms.CharField(required=False)
    star_rating = forms.IntegerField(required=False)
    cuisine_type = forms.CharField(required=False)
    price_range = forms.CharField(required=False)

class SurveyForm(ModelForm):
    class Meta:
        model = myUser
        fields = ['american_food', 'mexican_food', 'asian_food', 'mediterranean_food', 'vegetarian_food', 'fast_food', 'dessert_food',]

