from django.contrib import admin
from .models import Follower, UserAction


# Register your models here.
admin.site.register(Follower)
admin.site.register(UserAction)