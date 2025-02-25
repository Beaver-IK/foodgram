from rest_framework.viewsets import GenericViewSet, mixins
from recipe.models import Tag
from django.shortcuts import get_object_or_404
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
    
    def get_object(self):
        return get_object_or_404(Tag, pk=self.kwargs.get('pk'))