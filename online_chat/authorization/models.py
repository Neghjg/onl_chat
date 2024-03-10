from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images/', default='users_images/vk_default.jpg', blank=True, null=True, verbose_name='photo_user')
    online = models.BooleanField(default=False, verbose_name='online_status')
    last_online = models.DateTimeField(auto_now=True, verbose_name='last_online')
    
    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return self.username