from django.contrib import admin

from recipes.models import (Ingredient, Recipe,
                            RecipeIngredient, Tag)
from users.models import Favorites


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    """Админка рецептов"""
    inlines = (IngredientInline,)
    list_display = (
        'id', 'author', 'name', 'image', 'text',
        'cooking_time', 'favorites_count'
    )
    list_filter = ('tags',)
    search_fields = ('author', 'name', 'text')
    empty_value_display = '-пусто-'

    def favorites_count(self, obj):
        return Favorites.objects.filter(recipe=obj).count()

    favorites_count.short_description = 'Добавлений в избранное'


class TagAdmin(admin.ModelAdmin):
    """Админка тегов"""
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов"""
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('name',)
    list_per_page = 200
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
