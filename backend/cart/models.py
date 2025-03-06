from django.db import models
from django.conf import settings



class Cart(models.Model):
    """Модель покупательской корзины."""
    
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='cart',
        verbose_name='Владелец корзины'
    )
    
    recipes = models.ManyToManyField(
        'recipe.Recipe',
        blank=True,
    )