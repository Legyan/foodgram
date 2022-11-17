import re
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
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
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления'
    )

    def __str__(self):
        return self.name


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
        unique=True,
        verbose_name='Цветовой HEX-код'
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name

    def clean(self):
        if not re.fullmatch('#[0-9]{6}', self.color):
            raise ValidationError(
                'Цвет толжен быть представлен в HEX формате'
            )


class Ingredient(models.Model):
    """
    Модель ингредиентов
    """

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
        return self.name + ',' + self.measurement_unit

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique set of name and measurment_unit'
            )
        ]
