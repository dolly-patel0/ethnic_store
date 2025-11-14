from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Cart

@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.get_or_create(user=instance)
        print(f"Cart created for user: {instance.username}")

@receiver(post_save, sender=User)
def save_user_cart(sender, instance, **kwargs):
    # Ensure cart exists
    Cart.objects.get_or_create(user=instance)