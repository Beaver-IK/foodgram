from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from users.models import User as CustomUser
from cart.models import Cart


@receiver(post_save, sender=User)
def create_cart_for_user(sender, instance, created, **kwargs):
    if created:
        cart = Cart.objects.create()
        CustomUser.objects.create(user=instance, cart=cart)