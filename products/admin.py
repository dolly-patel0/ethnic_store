from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'featured', 'created_at']  # in_stock hata diya
    list_filter = ['category', 'featured', 'created_at']  # in_stock hata diya
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['price', 'featured']  # in_stock hata diya