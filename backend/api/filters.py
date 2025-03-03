from rest_framework import filters
import django_filters

from recipe.models import Recipe, Tag


class StartsWithIngredientFilter(filters.BaseFilterBackend):
    """Фильтр, для фильтрации в запросе по имени ингредиента.
    Фильтрует все значения, которые начинаются с заданной подстроки.
    """

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name', None)
        if name:
            return queryset.filter(name__startswith=name)
        return queryset

class RecipeFilter(django_filters.FilterSet):
    """Фильтр для рецептов."""
    author = django_filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
        distinct=True
    )
    
    class Meta:
        model = Recipe
        fields = ['author', 'tags']