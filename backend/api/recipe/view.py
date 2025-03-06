from rest_framework.viewsets import GenericViewSet, mixins, ModelViewSet
from recipe.models import Tag, Recipe
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from api.filters import RecipeFilter
from api.permissions import IsAuthOrOwnerOrRead
from api.recipe.serializers import (TagSerializer,
                                    RecipeSerializer,
                                    RecipeStripSerializer)
from api.models import RecipeShortLink
from api.utils import OrderGenerator

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
        detail=True,
        permission_classes=[AllowAny],
        url_path='get-link'
    )
    def get_link(self, request, pk=None):
        recipe = self.get_object()
        original_url = (
            f'{request.scheme}'
            f'://{request.get_host()}/api/recipes/{recipe.id}'
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
        recipe = self.get_object()
        cart = request.user.cart
        exists = cart.recipes.all().filter(id=recipe.id).exists()
        if request.method == 'POST':
            if not exists:
                cart.recipes.add(recipe)
                serializer = RecipeStripSerializer(recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(
                    'Рецепт уже добавлен', status=status.HTTP_400_BAD_REQUEST
                )
        else:
            if exists:
                cart.recipes.remove(recipe)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    'Нет такого рецепта в корзине',
                    status=status.HTTP_400_BAD_REQUEST
                )
    
    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path='favorite'
    )
    def favorites(self, request, pk=None):
        recipe = self.get_object()
        user = request.user
        exists = user.favourites.all().filter(id=recipe.id).exists()
        if request.method == 'POST':
            if not exists:
                user.favourites.add(recipe)
                serializer = RecipeStripSerializer(recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response(
                    'Рецепт уже в избранном',
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            if exists:
                if exists:
                    user.favourites.remove(recipe)
                    return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    'Нет такого рецепта в избранном',
                    status=status.HTTP_400_BAD_REQUEST
                )