from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор пользователей
    """

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
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


class ReadRecipeIngredienSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения ингредиентов рецепта
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


class WriteRecipeIngredienSerializer(serializers.ModelSerializer):
    """
    Сериализатор для определения ингредиентов рецепта
    """

    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class ReadRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения рецептов
    """

    author = UserSerializer()
    tags = TagSerializer(many=True, read_only=True)
    image = serializers.CharField(read_only=True)
    ingredients = ReadRecipeIngredienSerializer(
        many=True,
        read_only=True,
        source='recipe_ingredient_related'
    )

    class Meta:
        model = Recipe
        fields = '__all__'


class WriteRecipeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для определения рецептов
    """

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    ingredients = WriteRecipeIngredienSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image',
            'name', 'text', 'cooking_time'
        )

    def create(self, validated_data):
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            name=validated_data.pop('name'),
            image=validated_data.pop('image'),
            text=validated_data.pop('text'),
            cooking_time=validated_data.pop('cooking_time'),
        )
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe.tags.set(tags)
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                ingredient_id=ingredient['id'],
                amount=ingredient['amount'],
                recipe=recipe
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('image', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).all().delete()
        for ingredient in ingredients:
            amount = ingredient['amount']
            RecipeIngredient.objects.create(
                ingredient_id=ingredient['id'],
                amount=amount,
                recipe=instance
            )
        instance.save()
        return instance
