from django.contrib import admin

from users.models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админ панель для модели пользователей."""

    list_display = (
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'avatar'
    )
    list_editable = (
        'email',
        'username',
        'first_name',
        'last_name',
        'avatar'
    )
    search_fields = ('email', 'username',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Админ панель для модели подписок."""

    list_display = ('id', 'user', 'following')
    list_editable = ('user', 'following')
