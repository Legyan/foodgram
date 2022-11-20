from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from recipes.models import Recipe, RecipeIngredient, Tag


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

    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ['id', 'name', 'measurement_unit', 'amount']

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class RecipeSerialzer(serializers.ModelSerializer):
    """
    Сериализатор рецептов
    """

    author = SlugRelatedField(slug_field='username', read_only=True)
    tags = TagSerialzer(many=True, read_only=True)
    image = serializers.CharField(read_only=True)
    ingredients = IngredienSerialzer(many=True,
                                     read_only=True,
                                     source='recipe_ingredient_related')

    class Meta:
        model = Recipe
        fields = '__all__'
