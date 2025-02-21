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
        choices=Units.choices,
        default=Units.GRAM
    )
