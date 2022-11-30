from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import response, status
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet

from api.filters import IngredientSearchFilter, RecipeFilter
from api.mixins import BaseListRetrieveViewSet
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (FavoritesSerializer, IngredientSerializer,
                             ReadRecipeSerializer, RecipeInListSerializer,
                             ShoppingCartSerializer, SubscriptionSerializer,
                             TagSerializer, UserSubscriptionSerializer,
                             WriteRecipeSerializer)
from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов"""
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadRecipeSerializer
        return WriteRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_to_list(self, user, recipe, serializer):
        serializer = serializer(
            data={'user': user.id, 'recipe': recipe.id},
            context={'action': 'add'}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(recipe=recipe, user=user)
        response_serializer = RecipeInListSerializer(recipe)
        return response.Response(
            data=response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def remove_from_list(self, user, recipe, serializer):
        serializer = serializer(
            data={'user': user.id, 'recipe': recipe.id},
            context={'action': 'remove'}
        )
        serializer.is_valid(raise_exception=True)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Метод добавления/удаления рецепта из списка покупок"""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.add_to_list(
                request.user,
                recipe,
                ShoppingCartSerializer
            )
        return self.remove_from_list(
            request.user,
            recipe,
            ShoppingCartSerializer
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        """Метод добавления/удаления рецепта из избранного"""
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            return self.add_to_list(
                request.user,
                recipe,
                FavoritesSerializer
            )
        return self.remove_from_list(
            request.user,
            recipe,
            FavoritesSerializer
        )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        """Метод скачивания списка покупок в формате txt"""
        user = request.user
        shopping_list = user.shoppingcart_related.values(
            'recipe__ingredients__name',
            'recipe__ingredients__measurement_unit',
        ).annotate(
            amount=Sum(
                'recipe__recipe_ingredient_related__amount',
                distinct=True
            )
        )
        count = 1
        text = 'Список покупок:\n'
        for line in shopping_list:
            name, unit, amount = list(line.values())
            text += f'{count}. {name} ({unit}) — {amount}\n'
            count += 1
        return HttpResponse(text, content_type='text/plain')


class TagViewSet(BaseListRetrieveViewSet):
    """Вьюсет ингредиентов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(BaseListRetrieveViewSet):
    """Вьюсет ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientSearchFilter


class SubscriptionViewSet(UserViewSet):
    """Вьюсет подписок"""
    @action(
        methods=['GET'],
        detail=False,
        filter_backends=[DjangoFilterBackend],
        permission_classes=[IsAuthenticated]
    )
    def subscriptions(self, request):
        """Метод получения списка авторов в подписках"""
        follower_queryset = request.user.follower.all()
        paginated_queryset = self.paginate_queryset(follower_queryset)
        serializer = UserSubscriptionSerializer(
            paginated_queryset,
            many=True,
            context={'request': self.request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Метод подписки на автора"""
        serializer = SubscriptionSerializer(
            data={'following': id, 'user': request.user.id},
            context={'request': self.request, 'action': 'subscribe'}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id):
        """Метод отписки от автора"""
        get_object_or_404(User, pk=id)
        serializer = SubscriptionSerializer(
            data={'following': id, 'user': request.user.id},
            context={'request': self.request, 'action': 'unsubscribe'}
        )
        serializer.is_valid(raise_exception=True)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
