from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart ({self.user.username})"

    @property
    def total_price(self):
        try:
            return sum(item.total_price for item in self.items.all())
        except:
            return 0

    @property
    def total_items(self):
        try:
            return sum(item.quantity for item in self.items.all())
        except:
            return 0

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    @property
    def total_price(self):
        try:
            return self.product.price * self.quantity
        except:
            return 0

# Signal to create cart when user is created
@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_cart(sender, instance, **kwargs):
    instance.user_cart.save()