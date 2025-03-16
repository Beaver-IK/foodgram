from django.conf import settings
from django.db import models


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

    def __str__(self):
        return f'Козина пользователя {self.owner}'

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
