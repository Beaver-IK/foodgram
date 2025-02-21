from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from recipe import constants as c


class Recipe(models.Model):
    """Модель рецептов."""
    
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipes'
    
    name = models.CharField(
        max_length=c.LEN_RECIPE_NAME,
        blank=False,
        null=False,
        help_text='Не более 254 символов',
        verbose_name='Назание'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=False,
        blank=False,
        verbose_name='Автор рецепта'
    )
    ingredients = models.ManyToManyField(
        'ingredient.Ingredient',
        null=False,
        blank=False,
        verbose_name='Ингредиенты'
    )
    tags = models.ForeignKey(
        'Tag',
        null=False,
        blank=False,
        verbose_name='Хештег'
    )
    image = models.ImageField(
        upload_to='recipes/foto/',
        blank=False,
        null=False,
        verbose_name='Фото рецепта'
    )
    text = models.TextField(
        null=False,
        blank=False,
        help_text='Опишите последовательность приготовления.',
        verbose_name='Описание'
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        blank=False,
        null=False,
        help_text='Время приготовления в минутах.',
        verbose_name='Время приготовления'
    )
    is_active = models.BooleanField(
        default=False,
        help_text='Прохождение модерации',
        verbose_name='Активен'
    )

    def __str__(self):
        return self.name

    @property
    def short_link(self):
        """Метод возвращает ссылку на рецепт."""

    @property
    def rating(self):
        """Расчет рейтинга исходя из количества добавлений в избранное."""


class Tag(models.Model):
    """Модель тега."""

    class Meta:
        
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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
