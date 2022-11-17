import re
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from recipes.models import Ingredient, Recipe, Tag


class RecipeSerialzer(serializers.ModelSerializer):
    """
    Сериализатор рецептов
    """

    author = SlugRelatedField(slug_field='username', read_only=True)
    tag = SlugRelatedField(slug_field='slug', read_only=True)
    image = serializers.CharField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author', 'image')


class TagSerialzer(serializers.ModelSerializer):
    """
    Сериализатор тегов
    """

    class Meta:
        model = Tag
        fields = '__all__'


class IngredienSerialzer(serializers.ModelSerializer):
    """
    Сериализатор ингредиентов
    """

    class Meta:
        model = Ingredient
        fields = '__all__'
