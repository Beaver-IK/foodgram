from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from cart.models import Cart

User = get_user_model()

@receiver(post_save, sender=User)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:  # Если пользователь только что создан
        Cart.objects.create(user=instance)  # Создаем корзину для этого пользователя