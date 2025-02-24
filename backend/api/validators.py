from django.utils.deconstruct import deconstructible
from rest_framework.serializers import ValidationError
from rest_framework import status
from api import constants as c


@deconstructible
class PhotoValidator:
    """Валидация поля фотографии."""
    
    def __init__(self, size, ext_s: tuple):
        self.size = size
        self.ext_s = ext_s
    
    def __call__(self, value):
        if value is None:
            print(value)
            raise ValidationError(
                detail={'avatar': 'Обязатльное поле'},
                code=status.HTTP_400_BAD_REQUEST
            )
        if value.size > c.MAX_FILE_SIZE:
            raise ValidationError(
                detail={f'Максимальный размер файла '
                        f'{c.MAX_FILE_SIZE / (1024 * 1024)} Мб'
                },
            )