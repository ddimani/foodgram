# Generated by Django 4.2.20 on 2025-04-13 12:09

import core.validators
import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, default='', null=True, upload_to='users/', verbose_name='Аватар'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(help_text='Введите ваш никнейм', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator(), core.validators.validator_username], verbose_name='Никнейм'),
        ),
    ]
