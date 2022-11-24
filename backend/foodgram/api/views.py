from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import response, status
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet

from api.filters import RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer,
                             ReadRecipeSerializer, SubscriptionSerializer,
                             TagSerializer, UserSubscriptionSerializer,
                             WriteRecipeSerializer)
from recipes.models import Ingredient, Recipe, Tag
from users.models import Subscription, User


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов"""
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadRecipeSerializer
        return WriteRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BaseListRetrieveViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    """Базовый вьюсет для отображения списка объектов и конкретного объекта"""
    pass


class TagViewSet(BaseListRetrieveViewSet):
    """Вьюсет ингредиентов"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = LimitOffsetPagination


class IngredientViewSet(BaseListRetrieveViewSet):
    """Вьюсет ингредиентов"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = LimitOffsetPagination


class SubscriptionViewSet(UserViewSet):
    """Вьюсет подписок"""
    @action(
        methods=['get'],
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
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        """Метод подписки на автора"""
        serializer = SubscriptionSerializer(
            data={'following': id},
            context={'request': self.request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return response.Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id):
        """Метод отписки от автора"""
        following = get_object_or_404(User, pk=id)
        instance = Subscription.objects.filter(
            user=request.user,
            following=following
        )
        if instance.exists():
            instance.delete()
            return response.Response(status=status.HTTP_204_NO_CONTENT)
        return response.Response(
            {"errors": "Вы не подписаны на этого пользователя"},
            status=status.HTTP_400_BAD_REQUEST
        )
