from django.contrib import admin
from recipes.models import Favorites, ShoppingCart
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode


from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Админка пользователей"""
    model = User
    list_display = (
        'id', 'username',
        'first_name', 'last_name',
        'email', 'favorites', 'shopping_cart'
    )
    search_fields = ('username', 'email')
    empty_value_display = '-пусто-'

    def favorites(self, obj):
        count = Favorites.objects.filter(user=obj).count()
        url = (
            reverse("admin:recipes_favorites_changelist")
            + "?"
            + urlencode({"user": f"{obj.id}"})
        )
        return format_html(f'<a href="{url}">{count} рецептов</a>')

    def shopping_cart(self, obj):
        count = ShoppingCart.objects.filter(user=obj).count()
        url = (
            reverse("admin:recipes_shoppingcart_changelist")
            + "?"
            + urlencode({"user": f"{obj.id}"})
        )
        return format_html(f'<a href="{url}">{count} рецептов</a>')

    shopping_cart.short_description = "Список для покупок"
    favorites.short_description = 'Избранное'


admin.site.register(User, UserAdmin)
