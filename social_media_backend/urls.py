# project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('', include('posts.urls')),
    path('users/', include('relationships.urls')),
    path('feed/', include('feed.urls')),
]