from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet


class BaseListRetrieveViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet
):
    """Базовый вьюсет для отображения списка объектов и конкретного объекта"""
    pass
