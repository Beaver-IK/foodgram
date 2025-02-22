from django.db import models


class Cart(models.Model):
    """Модель покупательской корзины."""
    
    recipes = models.ManyToManyField(
        'recipe.Recipe',
        null=True,
        blank=True
    )