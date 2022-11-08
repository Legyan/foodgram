from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Recipe(models.Model):
    """
    Модель рецептов
    """

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/',
        null=True,
        blank=True
    )
    text = models.TextField(
        max_length=4000,
        verbose_name='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField()


class Tag(models.Model):
    """
    Модель тегов
    """

    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Имя тега'
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        unique=True
    )


class Ingredient(models.Model):
    """
    Модель ингредиентов
    """

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )
    amount = models.PositiveSmallIntegerField()
