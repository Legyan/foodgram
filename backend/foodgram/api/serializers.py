from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import User


class TagSerialzer(serializers.ModelSerializer):
    """
    Сериализатор тегов
    """

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиентов
    """

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredienSerializer(serializers.ModelSerializer):
    """
    Сериализатор ингредиентов рецепта
    """

    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователей
    """

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class RecipeSerialzer(serializers.ModelSerializer):
    """
    Сериализатор рецептов
    """

    author = UserSerializer()
    tags = TagSerialzer(many=True, read_only=True)
    image = serializers.CharField(read_only=True)
    ingredients = RecipeIngredienSerializer(
        many=True,
        read_only=True,
        source='recipe_ingredient_related'
    )

    class Meta:
        model = Recipe
        fields = '__all__'
