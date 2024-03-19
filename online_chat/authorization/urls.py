from django.urls import path
from .views import *

app_name = "authorization"

urlpatterns = [
    path('login/', login, name = 'login'),
    path("logout/", logout_user, name="logout"),
    path("registration/", registration, name="registration"),
    path('profile/', profile, name='profile'),
    path("", index_redirect, name="index_redirect")
]