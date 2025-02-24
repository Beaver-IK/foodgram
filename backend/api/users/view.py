from django.contrib.auth import get_user_model
from rest_framework import filters, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework import generics, viewsets
from rest_framework.response import Response
from djoser.serializers import SetPasswordSerializer

from api.permissions import IsAuthenticated
from api.users.serializers import UserSerializer, AvatarSerializer

Users = get_user_model()

class UsersViewSet(viewsets.ModelViewSet,
                generics.ListAPIView,
                generics.RetrieveAPIView,
                generics.CreateAPIView):
    """Вьюсет для презентации и регистрации пользователей.
    Отдает:
    Список пользователей.
    Пользователя по id.
    Регистрирует пользователя.
    """

    queryset = Users.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('$username',)
    http_method_name = ['get', 'post']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'is_registration': True}
        )
        if serializer.is_valid(raise_exception=True):
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
        permission_classes=[IsAuthenticated],
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