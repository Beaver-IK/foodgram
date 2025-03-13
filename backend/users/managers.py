from django.apps import apps
from django.contrib.auth.models import UserManager
from django.db import transaction
from django.contrib.auth.hashers import make_password

from cart.models import Cart


class CustomManager(UserManager):
    """Менеджер с переопределением метода create."""

    @transaction.atomic
    def _create_user(self, username, email, password, **extra_fields):
        """Создание пользователя и его привязка к покуавтельской корзине."""

        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(self.model._meta.app_label,
                                         self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        Cart.objects.create(owner=user)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create(self, **kwargs):
        return self.create_user(**kwargs)
