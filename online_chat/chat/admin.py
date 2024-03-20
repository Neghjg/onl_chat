from django.contrib import admin
from chat.models import ChatMessage3, UserMessege3
# Register your models here.


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id',  'created', 'updated')


class UserMessegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'user', 'text')


admin.site.register(ChatMessage3, ChatMessageAdmin)
admin.site.register(UserMessege3, UserMessegeAdmin)