from django.contrib import admin

# Register your models here.
from oauth_app.models import Reviews, Star, myUser, Restaurant

#admin.site.register(myUser)
admin.site.register(Restaurant)
admin.site.register(Reviews)
admin.site.register(Star)