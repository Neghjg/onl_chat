from django.contrib import admin
from chat.models import ChatMessage2, UserMessege2, ChatMessage3, UserMessege3
# Register your models here.


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user1', 'user2', 'created', 'updated')


class UserMessegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'user', 'text')


admin.site.register(ChatMessage2, ChatMessageAdmin)
admin.site.register(UserMessege2, UserMessegeAdmin)


class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id',  'created', 'updated')


class UserMessegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'user', 'text')


admin.site.register(ChatMessage3, ChatMessageAdmin)
admin.site.register(UserMessege3, UserMessegeAdmin)