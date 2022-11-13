from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from recipes.models import Recipe
from recipes.serializers import RecipeSerialzer


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет рецептов"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerialzer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
