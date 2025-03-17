from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.filters import RecipeFilter
from api.models import RecipeShortLink
from api.paginators import LimitSizePagination
from api.permissions import IsAuthorOrReadOnly
from api.recipe.serializers import (RecipeCreateUpdateSerializer,
                                    RecipeReadSerializer, TagSerializer)
from api.utils import (CartResponseGenerator, FavoriteResponseGenerator,
                       OrderGenerator)
from recipe.models import Recipe, Tag


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для Тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    pagination_class = None


class RecipeVievSet(ModelViewSet):
    """Вьюсет для рецептов"""

    queryset = Recipe.objects.all()
    pagination_class = LimitSizePagination
    serializer_class = RecipeReadSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
    permissions_actions = {
        'create': [IsAuthenticated],
        'update': [IsAuthenticated, IsAuthorOrReadOnly],
        'partial_update': [IsAuthenticated, IsAuthorOrReadOnly],
        'destroy': [IsAuthenticated, IsAuthorOrReadOnly],
        'add_delete_cart_recipes': [IsAuthenticated],
        'get_order': [IsAuthenticated],
        'favorites': [IsAuthenticated],
    }

    def get_permissions(self):
        if self.action in self.permissions_actions:
            permission_classes = self.permissions_actions[self.action]
        else:
            permission_classes = [AllowAny]
        return [permissions() for permissions in permission_classes]

    def get_queryset(self):
        return Recipe.objects.all().select_related(
            'author').prefetch_related('tags', 'ingredients')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeReadSerializer
        return RecipeCreateUpdateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['get'],
        detail=True,
        url_path='get-link'
    )
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        link, create = RecipeShortLink.objects.get_or_create(
            recipe=recipe,
        )
        if create:
            link.save()
        short_link = link.get_short_url(request)
        return Response(
            {'short-link': f'{short_link}'}, status=status.HTTP_200_OK
        )

    @action(
        methods=['get'],
        detail=False,
        url_path='download_shopping_cart'
    )
    def get_order(self, request):
        file_format = request.query_params.get('file_format', 'pdf').lower()
        cart = request.user.cart
        if request.method == 'GET':
            order = OrderGenerator(cart=cart, file_format=file_format)
            response = order.run_generator()
            return response

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='shopping_cart'
    )
    def add_delete_cart_recipes(self, request, pk=None):
        response = CartResponseGenerator(
            target_item=self.get_object(),
            container=request.user.cart,
            queryset=request.user.cart.recipes.all(),
            req_method=request.method,
        ).get_response()
        return response

    @action(
        methods=['post', 'delete'],
        detail=True,
        url_path='favorite'
    )
    def favorites(self, request, pk=None):
        response = FavoriteResponseGenerator(
            target_item=self.get_object(),
            container=request.user,
            queryset=self.request.user.favourites.all(),
            req_method=request.method,
        ).get_response()
        return response
