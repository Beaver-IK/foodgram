from django.contrib.auth import get_user_model
from rest_framework import filters, status, pagination
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from djoser.serializers import SetPasswordSerializer

from api.permissions import IsAuthenticated, IsProfileOwner
from api.users.serializers import UserSerializer, AvatarSerializer

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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'is_registration': True}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def get_user(self, request):
        serializer = self.serializer_class(request.user)
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