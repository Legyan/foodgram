from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer,
                             RecipeSerialzer,
                             TagSerialzer)
from recipes.models import Ingredient, Recipe, Tag


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет рецептов
    """

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = RecipeSerialzer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

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
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination
