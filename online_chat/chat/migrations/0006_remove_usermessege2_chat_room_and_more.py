# Generated by Django 4.2.7 on 2024-03-20 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_chatmessage3_group_name_chatmessage3_group_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermessege2',
            name='chat_room',
        ),
        migrations.RemoveField(
            model_name='usermessege2',
            name='user',
        ),
        migrations.DeleteModel(
            name='ChatMessage2',
        ),
        migrations.DeleteModel(
            name='UserMessege2',
        ),
    ]