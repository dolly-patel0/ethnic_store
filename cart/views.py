from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product

# Temporarily @login_required comment karein
@login_required
def cart_view(request):
    print(f"DEBUG: Cart view called for user {request.user}")  # Debug line
    
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()
        print(f"DEBUG: Cart found with {cart_items.count()} items")  # Debug line
        
        for item in cart_items:
            print(f"DEBUG: Item - {item.product.name}, Qty: {item.quantity}")  # Debug line
            
    except Cart.DoesNotExist:
        print("DEBUG: Cart does not exist")  # Debug line
        cart = None
        cart_items = []
    
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'cart/cart.html', context)

# @login_required
@login_required
def add_to_cart(request, product_id):
    print(f"DEBUG: Add to cart called for product {product_id} by user {request.user}")  # Debug line
    
    try:
        product = get_object_or_404(Product, id=product_id)
        print(f"DEBUG: Product found - {product.name}")  # Debug line
        
        # Get or create cart for user
        cart, created = Cart.objects.get_or_create(user=request.user)
        print(f"DEBUG: Cart - {cart}, Created - {created}")  # Debug line
        
        # Get quantity from form
        quantity = int(request.POST.get('quantity', 1))
        print(f"DEBUG: Quantity - {quantity}")  # Debug line
        
        # Check if product already in cart
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            print(f"DEBUG: Item exists, updating quantity")  # Debug line
            cart_item.quantity += quantity
            cart_item.save()
            message = f'Updated {product.name} quantity to {cart_item.quantity}'
        except CartItem.DoesNotExist:
            print(f"DEBUG: Creating new cart item")  # Debug line
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
            message = f'{product.name} added to cart!'
        
        print(f"DEBUG: Cart item created/updated - {cart_item}")  # Debug line
        
        # Check cart items after adding
        cart_items_count = cart.items.count()
        print(f"DEBUG: Total items in cart - {cart_items_count}")  # Debug line
        
        messages.success(request, message)
        
        # Redirect to cart page
        return redirect('cart:cart_view')
            
    except Exception as e:
        print(f"DEBUG: Error - {str(e)}")  # Debug line
        messages.error(request, f'Error adding product to cart: {str(e)}')
        return redirect('products:product_list')

# @login_required
@require_POST
def update_cart_item(request, item_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to update cart.')
        return redirect('users:signin')
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        action = request.POST.get('action')
        
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, 'Quantity increased!')
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
                messages.success(request, 'Quantity decreased!')
            else:
                cart_item.delete()
                messages.success(request, 'Item removed from cart!')
        elif action == 'remove':
            product_name = cart_item.product.name
            cart_item.delete()
            messages.success(request, f'{product_name} removed from cart!')
            
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart!')
    
    return redirect('cart:cart_view')

# @login_required
@require_POST
def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to remove items from cart.')
        return redirect('users:signin')
    
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f'{product_name} removed from cart!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart!')
    
    return redirect('cart:cart_view')

# @login_required
def checkout_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to checkout.')
        return redirect('users:signin')
    
    try:
        cart = Cart.objects.get(user=request.user)
        if cart.total_items == 0:
            messages.warning(request, 'Your cart is empty!')
            return redirect('cart:cart_view')
    except Cart.DoesNotExist:
        messages.warning(request, 'Your cart is empty!')
        return redirect('cart:cart_view')
    
    return render(request, 'cart/checkout.html', {'cart': cart})

def order_success(request, order_number):
    return render(request, 'cart/order_success.html', {'order_number': order_number})

def order_history(request):
    if not request.user.is_authenticated:
        return redirect('users:signin')
    return render(request, 'cart/order_history.html')