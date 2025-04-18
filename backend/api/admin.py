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
        'created_at'
    )
    search_fields = ('recipe__name', 'short_code')
    list_filter = ('created_at',)
    readonly_fields = ('short_code', 'created_at', 'short_url_display')
    fields = (
        'recipe',
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

    @admin.display(description='Рецепт', ordering='recipe__name')
    def recipe_link(self, obj):
        """Ссылка на связанный рецепт"""
        url = reverse('admin:recipe_recipe_change', args=[obj.recipe.id])
        return format_html('<a href="{}">{}</a>', url, obj.recipe.name)

    @admin.display(description='Короткая ссылка')
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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Оптимизация выбора рецепта"""
        if db_field.name == 'recipe':
            kwargs['queryset'] = Recipe.objects.order_by('name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
