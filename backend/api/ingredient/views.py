from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.filters import StartsWithIngredientFilter
from api.ingredient.serializers import IngredientSerializer
from ingredient.models import Ingredient


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для ингредиентов.
    Показывает список всех доступных ингредиентов.
    Показывает ингредиент по id.
    """

    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = StartsWithIngredientFilter
