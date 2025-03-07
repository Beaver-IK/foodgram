import django_filters
from rest_framework import filters

from recipe.models import Recipe, Tag
from users.models import User


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
    is_in_shopping_cart = django_filters.NumberFilter(
        method='in_cart_filter'
    )
    is_favorited = django_filters.NumberFilter(
        method='in_favorited_filter')
    
    class Meta:
        model = Recipe
        fields = ['author', 'tags']
    
    def in_cart_filter(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        
        try:
            value = int(value)
        except Exception:
            return queryset
        
        if value:
            return queryset.filter(cart__owner=user)
        return queryset
    
    def in_favorited_filter(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        try:
            value = int(value)
        except Exception:
            return queryset
        
        if value:
            return queryset.filter(favorited_by=user)
        return queryset