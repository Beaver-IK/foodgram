from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from recipe import constants as c
from recipe.managers import RecipeManager


class Recipe(models.Model):
    """Модель рецептов."""

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'
        ordering = ['-pub_date', 'name']

    name = models.CharField(
        max_length=c.LEN_RECIPE_NAME,
        unique=False,
        blank=False,
        null=False,
        help_text='Не более 254 символов',
        verbose_name='Назание'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        'ingredient.Ingredient',
        through='ingredient.RecipeIngredient',
        blank=True,
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        verbose_name='Теги'
    )
    image = models.ImageField(
        upload_to='recipes/foto/',
        blank=False,
        null=True,
        verbose_name='Фото рецепта'
    )
    text = models.TextField(
        null=False,
        blank=False,
        help_text='Опишите последовательность приготовления.',
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(c.MIN_COOKING_TIME)],
        blank=False,
        null=False,
        help_text='Время приготовления в минутах.',
        verbose_name='Время приготовления'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Модерация',
        verbose_name='Активен'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления',
    )

    objects = RecipeManager()

    def __str__(self):
        return f'{self.name}'


class Tag(models.Model):
    """Модель тега."""

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        default_related_name = 'tags'

    name = models.CharField(
        max_length=c.LEN_TAG_NAME,
        unique=True,
        blank=False,
        null=False,
        verbose_name='Тег'
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        null=False,
        verbose_name='Слаг'
    )

    def __str__(self):
        return f'{self.name}'
