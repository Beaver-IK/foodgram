import random
import string

from django.db import models
from django.urls import reverse

from api.constants import MAX_LENGTH_SHORT_CODE


class RecipeShortLink(models.Model):
    """Модель для генерации и хранения коротких ссылок."""

    recipe = models.OneToOneField(
        'recipe.Recipe',
        unique=True,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Рецепт',
    )
    short_code = models.CharField(max_length=MAX_LENGTH_SHORT_CODE,
                                  unique=True,
                                  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super(RecipeShortLink, self).save(*args, **kwargs)

    def generate_short_code(self, length=MAX_LENGTH_SHORT_CODE):
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(characters) for _ in range(length))
            if not RecipeShortLink.objects.filter(short_code=code).exists():
                return code

    def get_short_url(self, request):
        return request.build_absolute_uri(f'/s/{self.short_code}')

    def get_original_url(self, request):
        url = reverse('recipes-detail', kwargs={'pk': self.recipe.id})
        return request.build_absolute_uri(url)

    def __str__(self):
        return f'{self.get_short_url}'

    class Meta:
        verbose_name = 'Короткая ссылка на рецепт'
        verbose_name_plural = 'Короткие ссылки на рецепты'
        default_related_name = 'short_link'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'short_code'],
                name='unique_short_link',
            )
        ]
