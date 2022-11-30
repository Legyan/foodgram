from django.contrib import admin

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipesAdmin(admin.ModelAdmin):
    """Админка рецептов"""
    inlines = (IngredientInline,)
    list_display = ('id', 'author', 'name', 'image', 'text', 'cooking_time')
    list_filter = ('name', 'tags')
    search_fields = ('name', 'text')
    empty_value_display = '-пусто-'


class TagAdmin(admin.ModelAdmin):
    """Админка тегов"""
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')


class IngredientAdmin(admin.ModelAdmin):
    """Админка ингредиентов"""
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('name', 'measurement_unit')
    list_per_page = 200
    empty_value_display = '-пусто-'


admin.site.register(Recipe, RecipesAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
