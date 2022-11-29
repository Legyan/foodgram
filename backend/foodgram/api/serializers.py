from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (Favorites, Ingredient, Recipe,
                            RecipeIngredient, ShoppingCart, Tag)
from users.models import Subscription, User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            following = user.follower.all().values_list(
                'following_id', flat=True
            )
            return obj.pk in following
        return False


class RecipeInListSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов в списке"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeInShoppingCarttSerializer(RecipeInListSerializer):
    """Сериализатор рецептов в списке"""

    def validate(self, data):
        user = self.context['request'].user
        if ShoppingCart.objects.filter(recipe_id=id, user=user):
            raise serializers.ValidationError(
                'Рецепт уже в списке для покупок')
        return data


class RecipeInfavoritesSerializer(RecipeInListSerializer):
    """Сериализатор рецептов в списке"""

    def validate(self, data):
        user = self.context['request'].user
        if Favorites.objects.filter(recipe_id=id, user=user):
            raise serializers.ValidationError(
                'Рецепт уже в избранном')
        return data


class UserSubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя в подписках"""

    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    class Meta:
        model = Subscription
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return obj.user == self.context['request'].user

    def get_recipes(self, obj):
        request = self.context['request']
        recipes_limit = request.query_params.get('recipes_limit')
        if not recipes_limit:
            recipes = obj.following.recipes.all()
        else:
            recipes = obj.following.recipes.all()[:int(recipes_limit)]
        return RecipeInListSerializer(
            recipes, many=True, read_only=True
        ).data

    def get_recipes_count(self, obj):
        try:
            return obj.recipes_count
        except AttributeError:
            return Recipe.objects.filter(
                author=obj.following
            ).count()

    def validate(self, data):

        return data


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписок"""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    following = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )

    class Meta:
        model = Subscription
        fields = ['user', 'following']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'following'],
                message='Вы уже подписаны на этого пользователя'
            )
        ]

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Невозможно подписаться на самого себя')
        return data

    def to_representation(self, value):
        serializer = UserSubscriptionSerializer(value, context=self.context)
        return serializer.data


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class ReadRecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения ингредиентов рецепта"""

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


class WriteRecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для определения ингредиентов рецепта"""

    id = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class ReadRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения рецептов"""

    author = UserSerializer()
    tags = TagSerializer(many=True, read_only=True)
    ingredients = ReadRecipeIngredientSerializer(
        many=True,
        read_only=True,
        source='recipe_ingredient_related'
    )
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                return obj.is_in_shopping_cart
            except AttributeError:
                return ShoppingCart.objects.filter(
                    recipe=obj, user=user
                ).exists()
        return False

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            try:
                return obj.is_favorited
            except AttributeError:
                return Favorites.objects.filter(
                    recipe=obj, user=user
                ).exists()
        return False

    class Meta:
        model = Recipe
        fields = '__all__'


class WriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для определения рецептов"""

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField(use_url=True)
    ingredients = WriteRecipeIngredientSerializer(many=True)

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
            ingredient_id = ingredient['id']
            RecipeIngredient.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient_id),
                amount=amount,
                recipe=instance
            )
        instance.save()
        return instance
