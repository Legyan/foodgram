from django.urls import path, include
from rest_framework import routers

from api.views import (RecipeViewSet, IngredientViewSet,
                       SubscriptionViewSet, TagViewSet)

router = routers.DefaultRouter()

router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
