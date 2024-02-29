from django.db import models
from django.forms import forms
from django_google_maps import fields as map_fields
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    place_id = models.CharField(max_length=255, null=True, blank=True, unique = True, default="default")
    zip_code = models.CharField(max_length=10, null=True)
    star_rating = models.IntegerField(null=True)
    cuisine_type = models.CharField(max_length=50, null=True)
    price_range = models.CharField(max_length=50, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)

    def __str__(self):
        return f'{self.name, self.place_id, self.address, self.latitude, self.longitude}'

class Reviews(models.Model):
    review_text = models.CharField(max_length=500)
    pub_date = models.DateTimeField("date published")
    is_approved = models.BooleanField(default=False)
    is_reviewed = models.BooleanField(default=False)
    is_rejection_acknowledged = models.BooleanField(default=False)
    status = models.CharField(max_length=500, default="Your submitted review is waiting for approval.")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, to_field='place_id', db_column='place_id',
                                 related_name='reviews', default="default")

    def __str__(self):
        return f'{self.user, self.review_text, self.place_id, self.pub_date, self.status, self.is_reviewed, self.is_approved, self.is_rejection_acknowledged}'


class Star(models.Model):
    rating = models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    place_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE, to_field='place_id', db_column='place_id',
                                 related_name='stars', default="default")
    def __str__(self):
        return f'{self.rating}'

from django.db import models
from django_google_maps import fields as map_fields

# Create your models here.

class myUser(models.Model):
    # ID users by this id as primary key
    ADMIN = [
        ("a", "Admin"),
        ("u", "Common"),
    ]
    id = models.IntegerField(primary_key=True)
    userName = models.CharField(max_length=50)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    user_type = models.CharField(max_length=1, choices=ADMIN)
    vegetarian_food = models.BooleanField(default=False)
    american_food = models.BooleanField(default=False)
    mexican_food = models.BooleanField(default=False)
    asian_food = models.BooleanField(default=False)
    fast_food = models.BooleanField(default=False)
    dessert_food = models.BooleanField(default=False)
    mediterranean_food = models.BooleanField(default=False)


    def __str__(self):
        return self.firstName

class Favorite(models.Model):
    user = models.ForeignKey(myUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE) # Assuming Restaurant is another model you have
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.userName} - {self.restaurant.name}"