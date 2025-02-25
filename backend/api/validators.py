from django.utils.deconstruct import deconstructible
from rest_framework.serializers import ValidationError
from rest_framework import status
from users.constants import MAX_FILE_SIZE


@deconstructible
class PhotoValidator:
    """Валидация поля фотографии."""
    
    def __init__(self, size):
        self.size = size
    
    def __call__(self, value):
        if value is None:
            print(value)
            raise ValidationError(
                detail={'avatar': 'Обязатльное поле'},
                code=status.HTTP_400_BAD_REQUEST
            )
        if value.size > MAX_FILE_SIZE:
            raise ValidationError(
                detail={f'Максимальный размер файла '
                        f'{MAX_FILE_SIZE / (1024 * 1024)} Мб'
                },
            )