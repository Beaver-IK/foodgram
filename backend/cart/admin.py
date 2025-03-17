from django.contrib import admin

from cart.models import Cart
from recipe.models import Recipe


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'get_recipes_count',
    )
    search_fields = ('owner__username', 'recipes__name')
    filter_horizontal = ('recipes',)
    readonly_fields = ('owner',)
    save_on_top = True
    list_per_page = 20

    fieldsets = (
        (None, {
            'fields': ('owner',)
        }),
        ('Рецепты', {
            'fields': ('recipes',)
        })
    )

    @admin.display(description='Количество рецептов')
    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'recipes':
            kwargs['queryset'] = Recipe.objects.order_by('name')
        return super().formfield_for_manytomany(db_field, request, **kwargs)
