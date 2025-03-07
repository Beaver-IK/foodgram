from django.contrib.auth.models import UserManager
from django.db import transaction

from cart.models import Cart


class CustomManager(UserManager):
    """Менеджер с переопределением метода create."""

    @transaction.atomic
    def create_user(self, username, email, password, **extra_fields):
        user = super().create_user(username, email, password, **extra_fields)
        Cart.objects.create(owner=user)
        return user

    def create(self, **kwargs):
        return self.create_user(**kwargs)
