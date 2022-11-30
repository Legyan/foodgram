from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Админка пользователей"""
    model = User
    list_display = (
        'pk', 'username',
        'first_name', 'last_name',
        'mail', 'password'
    )
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
