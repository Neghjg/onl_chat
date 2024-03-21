from django.urls import path
from . import views


app_name = "chat"

urlpatterns = [
    path("", views.index, name="index"),
    path("search/", views.chat_search, name="search"),
    path("<slug:room_id>/", views.room, name="room"),
    path("private/<slug:user_name>/<slug:group_id>/", views.user_name, name="user_name"),
    path("add_to_group/<slug:user_name>/<slug:room_id>/", views.add_to_group, name="add_to_group"),
    path("kickout_from_group/<slug:user_name>/<slug:room_id>/", views.kickout_from_group, name="kickout_from_group"),
    path("change_group/<slug:room_id>", views.change_group, name="change_group")
]