from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('ethnic_wear', 'Ethnic Wear'),
        ('office_wear', 'Office Wear'),
        ('tops_tunics', 'Tops & Tunics'),
        ('collections', 'Collections'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    image_2 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='products/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # in_stock field hata diya
    featured = models.BooleanField(default=False)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})
    
    def get_category_display_name(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
    
    def get_additional_images(self):
        images = []
        if self.image_2:
            images.append(self.image_2)
        if self.image_3:
            images.append(self.image_3)
        if self.image_4:
            images.append(self.image_4)
        return images
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']