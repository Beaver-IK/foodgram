from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from recipe.models import Tag, Recipe
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination

from api.filters import RecipeFilter
from api.permissions import IsAuthOrOwnerOrRead
from api.recipe.serializers import TagSerializer, RecipeSerializer


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
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthOrOwnerOrRead]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    @action(
        methods=['get'],
        detail=False,
        permission_classes=[AllowAny],
        url_path='get-link'
    )
    def get_link(self):
        pass