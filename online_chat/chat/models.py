from django.db import models
from authorization.models import User
from django.urls import reverse
# Create your models here.


class ChatMessage2(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_2')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    


class UserMessege2(models.Model):
    chat_room = models.ForeignKey(ChatMessage2, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_room')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    text = models.TextField(max_length=3000, null=True, blank=True)