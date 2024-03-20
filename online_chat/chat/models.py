from django.db import models
from authorization.models import User
# Create your models here.
    
    
class ChatMessage3(models.Model):
    user = models.ManyToManyField(User, related_name='users')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    group_name = models.CharField(max_length=100, blank=True, null=True)
    group_photo = models.ImageField(upload_to='users_images/', default='users_images/vk_default.jpg', blank=True, null=True)
    
    


class UserMessege3(models.Model):
    chat_room = models.ForeignKey(ChatMessage3, on_delete=models.CASCADE, null=True, blank=True, related_name='chat_room')
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_message')
    text = models.TextField(max_length=3000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)