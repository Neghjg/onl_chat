from django.db import models
from authorization.models import User
# Create your models here.
    
    
class ChatMessage3(models.Model):
    user = models.ManyToManyField(User, related_name='users', verbose_name="Пользователи")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    group_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Название группы")
    group_photo = models.ImageField(upload_to='users_images/', default='users_images/vk_default.jpg', blank=True, null=True, verbose_name="Изображение группы")
    
    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        
    def __str__(self):
        return 'Чат №{}'.format(self.id)
    
    


class UserMessege3(models.Model):
    chat_room = models.ForeignKey(ChatMessage3, on_delete=models.CASCADE, null=True, blank=True, related_name="chat_room", verbose_name="Номер чата")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_message", verbose_name="Пользователь")
    text = models.TextField(max_length=3000, null=True, blank=True, verbose_name="Сообщение")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        
    def __str__(self):
        return 'Сообщение №{}'.format(self.id)