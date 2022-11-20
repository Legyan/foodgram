from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('pk', 'username',
                    'first_name', 'last_name',
                    'email', 'password'
                    )
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
