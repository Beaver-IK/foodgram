from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins

from api.filters import RecipeFilter
from api.models import RecipeShortLink
from api.paginators import LimitSizePagination
from api.permissions import IsAuthOrOwnerOrRead
from api.recipe.serializers import RecipeSerializer, TagSerializer
from api.utils import OrderGenerator, ResponseGenerator
from recipe.models import Recipe, Tag


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
    pagination_class = LimitSizePagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(
        methods=['get'],
        detail=True,
        permission_classes=[AllowAny],
        url_path='get-link'
    )
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        original_url = (
            f'{request.scheme}'
            f'://{request.get_host()}/recipes/{recipe.id}'
        )
        link, create = RecipeShortLink.objects.get_or_create(
            recipe=recipe,
            original_url=original_url
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
        permission_classes=[IsAuthenticated],
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
        permission_classes=[IsAuthenticated],
        url_path='shopping_cart'
    )
    def add_delete_cart_recipes(self, request, pk=None):
        response = ResponseGenerator(
            obj=self.get_object(),
            srh_obj=request.user.cart,
            queryset=request.user.cart.recipes.all(),
            req_method=request.method,
        ).get_response()
        return response

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path='favorite'
    )
    def favorites(self, request, pk=None):
        response = ResponseGenerator(
            obj=self.get_object(),
            srh_obj=request.user,
            queryset=self.request.user.favourites.all(),
            req_method=request.method,
        ).get_response()
        return response
