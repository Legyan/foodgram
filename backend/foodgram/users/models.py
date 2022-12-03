from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    email = models.EmailField(
        max_length=254,
        unique=True,
    )
    password = models.CharField(
        max_length=150,
    )

    REQUIRED_FIELDS = ('email', 'first_name', 'last_name')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    """Модель подписки"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'following'),
                name='unique subscribtion'
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class BaseRecipeUser(models.Model):
    """Базовая модель списка рецептов пользователя"""
    recipe = models.ForeignKey(
        'recipes.Recipe',
        on_delete=models.CASCADE,
        related_name='%(class)s_related',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_related',
        verbose_name='Пользователь'
    )

    class Meta:
        abstract = True


class ShoppingCart(BaseRecipeUser):
    """Модель списка покупок пользователя"""
    class Meta:
        verbose_name = 'Список покупок'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique recipe in user shoppingcart'
            )
        ]
        verbose_name = 'Рецепт в списке покупок пользователя'
        verbose_name_plural = 'Рецепты в списке покупок пользователей'


class Favorites(BaseRecipeUser):
    """Модель избранного пользователя"""
    class Meta:
        verbose_name = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique recipe in user favorites'
            )
        ]
        verbose_name = 'Рецепт в избранном пользователя'
        verbose_name_plural = 'Рецепты в избранном пользователей'
