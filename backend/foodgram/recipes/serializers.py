from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from recipes.models import Recipe


class RecipeSerialzer(serializers.ModelSerializer):
    """Сериализатор рецептов"""

    author = SlugRelatedField(slug_field='username', read_only=True)
    image = serializers.CharField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author', 'image')
