from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_views

app_name = "authorization"

urlpatterns = [
    path('login/', login, name = 'login'),
    path("logout/", logout_user, name="logout"),
    path("registration/", registration, name="registration"),
]