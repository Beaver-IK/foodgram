from django.contrib.auth import get_user_model
from rest_framework import filters, status, pagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from djoser.serializers import SetPasswordSerializer

from api.permissions import IsAuthenticated, IsProfileOwner
from api.users.serializers import UserSerializer, AvatarSerializer
from api.users.serializers import ExtendUserSerializer

Users = get_user_model()

class UsersViewSet(ModelViewSet):
    """Вьюсет для презентации и регистрации пользователей.
    Показывает список пользователей. [AllowAny]
    Показывает пользователя по id. [AllowAny]
    Регистрирует нового пользователя. [AllowAny]
    Показывает собственный профиль. [IsAuthenticated]
    Добавляет и удаляет собственный аватар пользователя. [IsAuthenticated]
    """

    queryset = Users.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$username',)
    http_method_name = ['get', 'post']
    pagination_class = pagination.LimitOffsetPagination
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {'request': self.request}
        return super().get_serializer(*args, **kwargs)
    
    def perform_create(self, serializer: UserSerializer):
        serializer.context.update({'is_registration': True})
        return super().perform_create(serializer)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def get_user(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['put', 'delete'],
        detail=False,
        permission_classes=[
            IsAuthenticated,
            IsProfileOwner],
        url_path='me/avatar'
    )
    def get_avatar(self, request):
        user = request.user
        if request.method == 'DELETE':
            user.avatar = None
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = AvatarSerializer(user, data=request.data, partial=False)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                data={'avatar': f'{user.avatar}'},
                status=status.HTTP_200_OK
            )
    
    @action(
        methods=['post'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='set_password')
    def set_password(self, request):
        serializer = SetPasswordSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        self.request.user.set_password(serializer.data['new_password'])
        self.request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        """Вывод водписок."""
        recipes_limit = request.query_params.get('recipes_limit', None)
        queryset = request.user.subscriptions.all()
        page = self.paginate_queryset(queryset)
        serializer = ExtendUserSerializer(
                page,
                context={'recipes_limit': recipes_limit,
                         'request': self.request},
                many=True
            )
        return self.get_paginated_response(serializer.data)
    
    @action(
        methods=['post','delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path='subscribe'
    )
    def subscribe(self, request, pk=None):
        """Создание и удаление подписок."""
        user = self.get_object()
        current_user = request.user
        recipes_limit = request.query_params.get('recipes_limit', None)
        exists = current_user.subscriptions.all().filter(id=user.id).exists()
        if user == current_user:
            return Response('Нельзя подписаться на самого себя',
                                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            if not exists:
                current_user.subscriptions.add(user)
                serializer = ExtendUserSerializer(
                    user,
                    context={'recipes_limit': recipes_limit,
                             'request': request}
                )
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED)
            else:
                return Response('Пользователь уже добавлен',
                                status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'DELETE':
            if exists:
                current_user.subscriptions.remove(user)
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response('Вы не подписаны на пользователя',
                                status=status.HTTP_400_BAD_REQUEST)


