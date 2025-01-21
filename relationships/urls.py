from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/follow/', views.FollowView.as_view(), name='follow'),
    path('<str:username>/unfollow/', views.UnfollowView.as_view(), name='unfollow'),
    path('<str:username>/followers/', views.FollowerListView.as_view(), name='followers'),
    path('<str:username>/following/', views.FollowingListView.as_view(), name='following'),
    path('<str:username>/action/', views.UserActionView.as_view(), name='user-action'),
    path('actions/', views.UserActionListView.as_view(), name='user-action-list'),
]