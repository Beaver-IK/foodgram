import base64
from django.core.files.base import ContentFile
from rest_framework import serializers

class Base64ImageField(serializers.ImageField):
    """Поле для обработки Base64-изображений."""
    
    def __init__(self, name='None', *args, **kwargs):
        self.default_error_messages['required'] = 'Обязательное поле'
        self.default_error_messages['invalid'] = 'Пустое значение'
        self.name = name
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, image_str = data.split(';base64,')
            ext = format.split('/')[-1]
            try:
                decoded_image = base64.b64decode(image_str)
            except Exception as e:
                raise serializers.ValidationError(
                    f'Ошибка декодирования Base64: {e}')
            file_name = f'_{self.name}.{ext}'
            data = ContentFile(decoded_image, name=file_name)
        return super().to_internal_value(data)