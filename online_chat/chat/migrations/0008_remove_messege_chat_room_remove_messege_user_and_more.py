# Generated by Django 4.2.7 on 2024-03-20 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_chat_messege'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='messege',
            name='chat_room',
        ),
        migrations.RemoveField(
            model_name='messege',
            name='user',
        ),
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='Messege',
        ),
    ]
