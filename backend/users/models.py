from django.contrib.auth.models import AbstractUser
from django.db import models

from core.constants import EMAIL_MAX_LENGTH, USERNAME_MAX_LENGTH
from core.validators import validator_username


class User(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        verbose_name='Имя',
        help_text = 'Введите ваше имя'
    )
    last_name = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        verbose_name='Фамилия',
        help_text='Введите вашу фамилию'
    )
    username = models.CharField(
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        verbose_name='Никнейм',
        help_text='Введите ваш никнейм',
        validators=[validator_username]
    )
    email = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        unique=True,
        verbose_name='Почта',
        help_text='Введите вашу электронную почту'
    )
    avatar = models.ImageField(
        upload_to='users/',
        verbose_name='Аватар',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')

    class Meta:
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'Пользователь {self.username}'


class Subscription(models.Model):
    """Модель подписки."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subscriptions'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings'
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'подписка пользователя'
        verbose_name_plural = 'Подписки пользователя'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('following')),
                name='user_not_following'
            )
        ]

    def __str__(self):
        return f'{self.user.username} на {self.following.username}'