from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from recipes.models import Ingredient, Recipe, Tag
from recipes.serializers import (IngredienSerialzer,
                                 RecipeSerialzer,
                                 TagSerialzer)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет рецептов
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerialzer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    """
    Вьюсет ингредиентов
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerialzer
    pagination_class = LimitOffsetPagination


class IngredientViewSet(viewsets.ModelViewSet):
    """
    Вьюсет ингредиентов
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredienSerialzer
    pagination_class = LimitOffsetPagination
