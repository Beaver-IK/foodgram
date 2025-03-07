from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from api.models import RecipeShortLink
from recipe.models import Recipe


@admin.register(RecipeShortLink)
class RecipeShortLinkAdmin(admin.ModelAdmin):
    list_display = (
        'recipe_link',
        'short_url_display',
        'original_url_truncated',
        'created_at'
    )
    search_fields = ('recipe__name', 'original_url', 'short_code')
    list_filter = ('created_at',)
    readonly_fields = ('short_code', 'created_at', 'short_url_display')
    fields = (
        'recipe',
        'original_url',
        'short_code',
        'created_at',
        'short_url_display'
    )
    ordering = ('-created_at',)
    list_per_page = 20
    save_on_top = True

    def get_queryset(self, request):
        self.request = request
        return super().get_queryset(request)

    def recipe_link(self, obj):
        """Ссылка на связанный рецепт"""
        url = reverse('admin:recipe_recipe_change', args=[obj.recipe.id])
        return format_html('<a href="{}">{}</a>', url, obj.recipe.name)
    recipe_link.short_description = 'Рецепт'
    recipe_link.admin_order_field = 'recipe__name'

    def short_url_display(self, obj):
        """Отображение полной короткой ссылки"""
        if obj.short_code:
            full_url = self.request.build_absolute_uri(f'/s/{obj.short_code}')
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                full_url,
                obj.short_code
            )
        return '-'
    short_url_display.short_description = 'Короткая ссылка'

    def original_url_truncated(self, obj):
        """Сокращенный URL для отображения"""
        max_length = 50
        if len(obj.original_url) > max_length:
            return f'{obj.original_url[:max_length]}...'
        return obj.original_url
    original_url_truncated.short_description = 'Оригинальный URL'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Оптимизация выбора рецепта"""
        if db_field.name == 'recipe':
            kwargs['queryset'] = Recipe.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)