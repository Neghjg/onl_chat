from django.contrib import admin
from chat.models import ChatMessage3, UserMessege3
# Register your models here.


class UserMessegeTabAdmin(admin.TabularInline):
    model = UserMessege3
    fields = ('id', 'user', 'text', 'created')
    search_fields = ('user__username', 'chat_room__id', 'id')
    readonly_fields = ('id', 'user', 'text', 'created')
    extra = 1

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id',  'created', 'updated')
    list_filter = ('created', 'updated')
    search_fields = ('id', 'user__username')
    fields = ( 'user', 'group_name', 'group_photo', ('created', 'updated'))
    readonly_fields = ('created', 'updated', 'user')
    inlines = [UserMessegeTabAdmin,]
    
    


class UserMessegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat_room', 'user', 'text')
    list_filter = ('created',)
    search_fields = ('id', 'user__username')
    fields = ( 'user', 'text', 'created')
    readonly_fields = ('created', 'user', 'text')
    
    



admin.site.register(ChatMessage3, ChatMessageAdmin)
admin.site.register(UserMessege3, UserMessegeAdmin)