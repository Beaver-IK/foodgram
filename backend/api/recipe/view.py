from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from recipe.models import Tag, Recipe
from rest_framework.permissions import AllowAny

from api.permissions import IsAuthOrOwnerOrRead
from api.recipe.serializers import TagSerializer, RecipeReadSerializer, RecipeWriteSerializer


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
    # permission_classes = [IsAuthOrOwnerOrRead]
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeWriteSerializer