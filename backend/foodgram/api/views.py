from django.db.models import Sum
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
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

from api.filters import IngredientSearchFilter, RecipeFilter
from api.permissions import IsAuthorOrReadOnly
from api.serializers import (IngredientSerializer,
                             ReadRecipeSerializer,
                             RecipeInSubscriptionSerializer,
                             SubscriptionSerializer,
                             TagSerializer, UserSubscriptionSerializer,
                             WriteRecipeSerializer)
from recipes.models import Favorites, Ingredient, Recipe, ShoppingCart, Tag
from users.models import Subscription, User


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов"""

    queryset = Recipe.objects.all().order_by('-id')
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

    def add_to_list(self, model, user, recipe_id):
        model.objects.create(
            user=user,
            recipe_id=recipe_id
        )
        recipe = Recipe.objects.get(pk=recipe_id)
        serializer = RecipeInSubscriptionSerializer(instance=recipe)
        return response.Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def remove_from_list(self, model, user, recipe_id):
        model.objects.get(user=user, recipe_id=recipe_id).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def shopping_cart(self, request, pk):
        """Метод добавления/удаления рецепта из списка покупок"""

        if request.method == 'POST':
            if ShoppingCart.objects.filter(recipe_id=pk, user=request.user):
                return response.Response(
                    {"errors": 'Рецепт уже в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return self.add_to_list(ShoppingCart, request.user, pk)
        try:
            return self.remove_from_list(ShoppingCart, request.user, pk)
        except ObjectDoesNotExist:
            return response.Response(
                {"errors": 'Удаляемого рецепта нет в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        """Метод добавления/удаления рецепта из избранного"""

        if request.method == 'POST':
            if Favorites.objects.filter(recipe_id=pk, user=request.user):
                return response.Response(
                    {"errors": 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return self.add_to_list(Favorites, request.user, pk)
        try:
            return self.remove_from_list(Favorites, request.user, pk)
        except ObjectDoesNotExist:
            return response.Response(
                {"errors": 'Удаляемого рецепта нет в избранном'},
                status=status.HTTP_400_BAD_REQUEST
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
        file = open('shopping_cart.txt', 'w')
        file.write('Список покупок:\n\n')
        count = 1
        for line in shopping_list:
            name, measurement_unit, amount = list(line.values())
            file.write(f'{count}. {name} ({measurement_unit}) — {amount}\n')
            count += 1
        file.close()
        return HttpResponse(shopping_list, content_type='text/plain')


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
