# Generated by Django 4.2.7 on 2024-03-08 10:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_chatmessage3_usermessege3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessege3',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_message', to=settings.AUTH_USER_MODEL),
        ),
    ]