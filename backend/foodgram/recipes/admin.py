from django.contrib import admin

from recipes.models import Ingredient, Recipe, Tag


class RecipesAdmin(admin.ModelAdmin):
    """Админка рецептов"""

    list_display = ('id', 'author', 'name', 'image', 'text', 'cooking_time')
    list_filter = ('id', 'name', 'text')
    search_fields = ('name', 'text')
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    """Админка тегов"""

    list_display = ('id', 'name', 'color', 'slug')
    list_filter = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов"""

    list_display = ('id', 'name', 'measurement_unit', 'amount')
    list_filter = ('id', 'name', 'measurement_unit', 'amount')
    search_fields = ('name', 'measurement_unit', 'amount')
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
