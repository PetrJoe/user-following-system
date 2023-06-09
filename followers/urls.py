from django.urls import path
from .views import *

urlpatterns = [
    path('follow/', follow_user, name='follow_user'),
    path('followers/<int:follower_id>/', remove_follower, name='remove_follower'),
    path('my_followers/', my_followers, name='my_followers'),
]
