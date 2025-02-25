from django.contrib.auth import get_user_model
from rest_framework.serializers import ValidationError


User = get_user_model()

def already_use(data):
    """Функция проверки занятости username и email."""
    already_use = User.already_use(data)
    if already_use:
        raise ValidationError(already_use)
    return data