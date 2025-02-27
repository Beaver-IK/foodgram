from rest_framework import filters


class StartsWithIngredientFilter(filters.BaseFilterBackend):
    """Фильтр, для фильтрации в запросе по имени ингредиента.
    Фильтрует все значения, которые начинаются с заданной подстроки.
    """

    def filter_queryset(self, request, queryset, view):
        name = request.query_params.get('name', None)
        if name:
            return queryset.filter(name__startswith=name)
        return queryset
