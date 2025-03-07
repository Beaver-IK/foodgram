from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator, RegexValidator
from rest_framework import serializers

from api import constants as c
from api.fields import Base64ImageField
from api.users.utils import already_use
from api.validators import PhotoValidator
from users.constants import LEN_USERNAME
from users.validators import NotMeValidator

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый сериализатор пользователей."""

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        """Метод получения атрибута подписки."""

        request = self.context.get('request')
        current_user = request.user
        if not current_user.is_anonymous and current_user != obj:
            return obj in current_user.subscriptions.all()
        return False


class UserSerializer(BaseUserSerializer):
    """Сериализатор пользователей."""
    username = serializers.CharField(
        max_length=LEN_USERNAME,
        validators=[NotMeValidator,
                    RegexValidator(
                        regex=r'^[\w.@+-]+\Z',
                        message='Некорректный username',
                        code='invalid_username',
                    ),
                    ]
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'avatar',
            'password',
            'email',)
        read_only_fields = ('id',)

    def validate(self, attrs):
        return already_use(attrs)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        print(self.context)
        if self.context.get('is_registration'):
            data.pop('is_subscribed', None)
            data.pop('avatar', None)
        return data


class AvatarSerializer(serializers.ModelSerializer):
    """Сериализатор добавления аватара."""
    avatar = Base64ImageField(
        name='avatar',
        required=True,
        validators=[
            PhotoValidator(size=c.MAX_FILE_SIZE),
            FileExtensionValidator(allowed_extensions=c.ALLOW_EXT)
        ]
    )

    def update(self, instance, validated_data):
        username = instance.username
        print(instance)
        avatar = validated_data.get('avatar')

        if avatar:
            instance.avatar = self.fields['avatar'].run_validation(avatar)
        instance.avatar.name = f'{username}{instance.avatar.name}'
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('avatar',)


class ExtendUserSerializer(BaseUserSerializer):
    """Расширенный сериализатор пользователя.
    Дополнительные поля recipes и recipes_count.
    """

    recipes_count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'is_subscribed',
                  'avatar',
                  'recipes_count',
                  'recipes')
        read_only_fields = ('__all__',)

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()

    def get_recipes(self, obj):
        from api.recipe.serializers import RecipeStripSerializer
        recipes_limit = self.context.get('recipes_limit', None)
        if recipes_limit:
            recipes_limit = int(recipes_limit)
        queryset = obj.recipes.all()[:recipes_limit]
        return RecipeStripSerializer(queryset, many=True).data
