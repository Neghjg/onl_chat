from django.urls import path

from . import views


app_name = "chat"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.chat_search, name="search"),
    path("<slug:room_name>/", views.room, name="room"),
    path("private/<slug:user_name>", views.user_name, name="user_name")
]