from django.core.validators import MinValueValidator
from django.db import models

from ingredient import constants as c


class Ingredient(models.Model):
    """Модель ингредиента."""

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    class Units(models.TextChoices):
        HANDFUL = 'горсть', 'Горсти'
        DROP = 'капля', 'Капли'
        BRANCH = 'веточка', 'Веточки'
        ML = 'мл', 'мл'
        TEASPOON = 'ч. л.', 'Чайные ложки'
        PIECE = 'кусок', 'Куски'
        POT = 'банка', 'Банки'
        GRAM = 'г', 'г'
        GLASS = 'стакан', 'Стаканы'
        PINCH = 'щепотка', 'Щепотки'
        LOAF = 'батон', 'Батоны'
        TABLESPOON = 'ст. л.', 'Столовые ложки'
        ONE = 'шт.', 'Штуки'

    name = models.CharField(
        max_length=c.LEN_INGREDIENT_NAME,
        null=False,
        blank=False,
        unique=True
    )

    measurement_unit = models.CharField(
        max_length=c.LEN_UNIT_NAME,
        choices=Units.choices,
        default=Units.GRAM
    )

    def __str__(self):
        return f'{self.name}'


class RecipeIngredient(models.Model):
    """Промежуточная модель между рецептом
    и ингридиентами с количеством ингридиентов.
    """

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient',
            )
        ]
        default_related_name = 'recipe_ingredients'

    recipe = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        'ingredient.Ingredient',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Укажите количество',
        verbose_name='Общее количество')
