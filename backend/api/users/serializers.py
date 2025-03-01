from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator


from users.constants import LEN_USERNAME
from django.core.validators import RegexValidator
from users.validators import NotMeValidator
from api.validators import PhotoValidator
from api.users.utils import already_use
from api.fields import Base64ImageField
from api import constants as c

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    
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
    is_subscribed = serializers.SerializerMethodField()

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
    
    def get_is_subscribed(self, obj):

        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            current_user = request.user
            if not current_user.is_anonymous:
                return obj in current_user.subscriptions.all()
        return False
    
    def validate(self, attrs):
        return already_use(attrs)
        
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context.get('is_registration'):
            data.pop('is_subscribed', None)
            data.pop('avatar', None)
        return data
    
class AvatarSerializer(serializers.ModelSerializer):
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

        if avatar: # is not None:
            instance.avatar = self.fields['avatar'].run_validation(avatar)
        instance.avatar.name = f'{username}{instance.avatar.name}'
        instance.save()
        return instance
    
    class Meta:
        model = User
        fields = ('avatar',)