from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from recipe.models import Tag, Recipe
from rest_framework.permissions import AllowAny

from api.recipe.serializers import TagSerializer


class TagViewSet(GenericViewSet, 
                 mixins.ListModelMixin, 
                 mixins.RetrieveModelMixin):
    """Вьюсет для Тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None

class RecipeVievSet(ModelViewSet):
    """Вьюсет для рецептов"""
    
    queryset = Recipe.objects.all()
    