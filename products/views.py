from django.shortcuts import render, get_object_or_404
from .models import Product

def product_list_view(request, category=None):
    products = Product.objects.all()
    
    if category and category != 'all':
        products = products.filter(category=category)
        category_display = dict(Product.CATEGORY_CHOICES).get(category, category)
    else:
        category_display = "All Products"
    
    context = {
        'products': products,
        'category': category,
        'category_display': category_display,
        'categories': Product.CATEGORY_CHOICES,
    }
    return render(request, 'products/product_list.html', context)

def product_detail_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)