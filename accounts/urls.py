from django.urls import path,include
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
	path('login/', UserLoginView.as_view(), name='sigin'),
	path('registeration/', SignUpView.as_view(), name='signup'),
    path('profile/me/', UserDetailView.as_view(), name='user_profile'),
    path('profile_update/', UserProfileUpdateView.as_view(), name='profile-update'),
]
