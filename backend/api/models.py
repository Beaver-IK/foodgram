import random
import string

from django.db import models


class RecipeShortLink(models.Model):
    """Модель для генерации и хранения коротких ссылок."""
    
    class Meta:
        verbose_name = 'Короткая ссылка на рецепт'
        verbose_name_plural = 'Короткие ссылки на рецепты'
        default_related_name = 'short_link'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['original_url', 'short_code'],
                name='unique_short_link',
            )
        ]
    
    original_url = models.URLField(max_length=2000,
                                   unique=True)
    recipe = models.ForeignKey(
        'recipe.Recipe',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='Рецепт',
    )
    short_code = models.CharField(max_length=10,
                                  unique=True,
                                  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = self.generate_short_code()
        super(RecipeShortLink, self).save(*args, **kwargs)
            
    def generate_short_code(self, length=3):
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(characters) for _ in range(length))
            if not RecipeShortLink.objects.filter(short_code=code).exists():
                return code
    
    def get_short_url(self, request):
        return f"{request.scheme}://{request.get_host()}/s/{self.short_code}"

    def __str__(self):
        return f'{self.original_url} -> {self.short_code}'