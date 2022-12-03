import re
from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


class Recipe(models.Model):
    """Модель рецептов"""
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
        blank=True,
        verbose_name='Изображение'
    )
    text = models.TextField(
        max_length=4000,
        verbose_name='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        'Ingredient', through='RecipeIngredient',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    """Модель ингредиентов рецепта"""
    recipe = models.ForeignKey(
        Recipe,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="recipe_ingredient_related"
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient in recipe'
            )
        ]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'


class Tag(models.Model):
    """Модель тегов"""
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Имя тега'
    )
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name

    def clean(self):
        if not re.fullmatch(r'#[0-9A-Fa-f]{6}', self.color):
            raise ValidationError(
                'Цвет должен быть в HEX формате (#[0-9A-Fa-f]{6})'
            )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """Модель ингредиентов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единицы измерения'
    )
    amount = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Количество'
    )

    def __str__(self):
        return self.name + ', ' + self.measurement_unit

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique set of name and measurment_unit'
            )
        ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
