# Generated by Django 4.2.7 on 2024-03-10 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0004_user_last_online_user_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_online',
            field=models.DateTimeField(auto_now=True, verbose_name='last_online'),
        ),
    ]
