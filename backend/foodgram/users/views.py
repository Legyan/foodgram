from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from recipes.models import User
from users.serializers import CreateUserSerializer


class CreateUserViewSet(CreateModelMixin, GenericViewSet):
    """Вьюсет для создания пользователя"""
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
