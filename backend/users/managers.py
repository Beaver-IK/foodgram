from django.contrib.auth.models import UserManager
from django.db import transaction

from cart.models import Cart


class CustomManager(UserManager):
    """Менеджер с переопределением метода create."""
    
    @transaction.atomic
    def create_user(self, username, email, password, **extra_fields):
        cart = Cart.objects.create()
        extra_fields.setdefault('cart', cart)
        return super().create_user(username, email, password, **extra_fields)
    
    def create(self, **kwargs):
        return self.create_user(**kwargs)