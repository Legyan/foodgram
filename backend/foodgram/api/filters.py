import django_filters.rest_framework as filters

from recipes.models import Ingredient, Recipe
from users.models import User


class RecipeFilter(filters.FilterSet):
    """Фильтр для вьюсета рецептов"""
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart'
    )

    def filter_is_favorited(self, queryset, name, value):
        return queryset.filter(favorites_related__user=self.request.user)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(shoppingcart_related__user=self.request.user)

    class Meta:
        model = Recipe
        fields = ('author', 'tags')


class IngredientSearchFilter(filters.FilterSet):
    """Фильтр для ингредиентов"""
    name = filters.CharFilter(
        field_name="name", lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
