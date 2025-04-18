from django.contrib import admin
from django.utils.html import format_html

from recipe.models import Recipe, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    verbose_name = 'Ингредиент в рецепте'
    verbose_name_plural = 'Ингредиенты в рецепте'
    autocomplete_fields = ('ingredient',)  # Включаем автодополнение


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'get_tags',
        'cooking_time',
        'is_active',
        'pub_date',
        'image_thumbnail'
    )
    list_filter = ('is_active', 'tags', 'pub_date', 'author')
    search_fields = ('name', 'author__username', 'tags__name')
    date_hierarchy = 'pub_date'
    ordering = ('-pub_date',)
    readonly_fields = ('pub_date',)
    raw_id_fields = ('author',)
    filter_horizontal = ('tags',)
    inlines = (RecipeIngredientInline,)
    list_editable = ('is_active',)
    list_per_page = 20
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('name', 'author', 'text', 'image',
                       'cooking_time', 'is_active')
        }),
        ('Метаданные', {
            'fields': ('pub_date',),
            'classes': ('collapse',)
        }),
        ('Теги', {
            'fields': ('tags',)
        })
    )

    @admin.display(description='Теги')
    def get_tags(self, obj):
        return ', '.join([tag.name for tag in obj.tags.all()])

    @admin.display(description='Миниатюра')
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" />', obj.image.url)
        return '-'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags', 'author')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    save_on_top = True

    fieldsets = (
        (None, {
            'fields': ('name', 'slug')
        }),
    )
