import django_filters

from ingredient.models import Ingredient
from recipe.models import Recipe, Tag


class StartsWithIngredientFilter(django_filters.FilterSet):
    """
    Фильтр для модели Ingredient, который позволяет фильтровать
    ингредиенты по имени, начинающемуся с заданной подстроки.
    """
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='startswith',
        label='Name starts with'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):
    """Фильтр для рецептов."""

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
        fields = ('author', 'tags',)

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
