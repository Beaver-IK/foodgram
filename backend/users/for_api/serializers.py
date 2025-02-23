from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator

from users.constants import LEN_USERNAME
from users.validators import NotMeValidator
from users.for_api.utils import already_use


User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(
        max_length=LEN_USERNAME,
        validators=[NotMeValidator, UnicodeUsernameValidator]
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password')
    
    def validate(self, attrs):
        return already_use(attrs)
        

class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания профиля."""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password')


class UserSerializer(BaseUserSerializer):
    """Сериализатор профиля."""
    
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password')


class CurrentUserSerializer(BaseUserSerializer):
    """Сериализатор для своего профиля."""
    
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password')