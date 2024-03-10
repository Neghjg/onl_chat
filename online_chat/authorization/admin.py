from django.contrib import admin
from authorization.models import User
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "first_name", "last_name", "email", ]
    search_fields = ["id", "username", "first_name", "last_name", "email",]