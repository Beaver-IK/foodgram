from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.permissions import AllowAny
from rest_framework import filters

from ingredient.models import Ingredient
from api.filters import StartsWithIngredientFilter
from api.ingredient.serializers import IngredientSerializer


class IngredientViewSet(GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin):
    """Вьюсет для ингредиентов.
    Показывает список всех доступных ингредиентов.
    Показывает ингредиент по id.
    """
    
    queryset = Ingredient.objects.all()
    permission_classes = [AllowAny]
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = [StartsWithIngredientFilter]
    