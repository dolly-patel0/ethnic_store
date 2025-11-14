from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from products.models import Product

@login_required
def add_to_cart(request, product_id):
    print("=== ADD TO CART STARTED ===")
    
    try:
        # Get product
        product = get_object_or_404(Product, id=product_id)
        print(f"Product: {product.name}")
        
        # Get or create cart - force creation
        cart, created = Cart.objects.get_or_create(user=request.user)
        print(f"Cart: {cart}, Created: {created}")
        
        # Get quantity
        quantity = int(request.POST.get('quantity', 1))
        print(f"Quantity: {quantity}")
        
        # Check if item exists
        try:
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            message = f'Updated {product.name} quantity to {cart_item.quantity}'
            print(f"Updated existing item: {cart_item}")
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                cart=cart,
                product=product,
                quantity=quantity
            )
            message = f'{product.name} added to cart!'
            print(f"Created new item: {cart_item}")
        
        # Force refresh and verify
        cart = Cart.objects.get(user=request.user)
        item_count = cart.items.count()
        print(f"Verification - Cart items: {item_count}")
        
        if item_count > 0:
            messages.success(request, message)
            print("SUCCESS: Item added to cart")
        else:
            messages.error(request, "Failed to add item to cart")
            print("ERROR: Item not saved")
        
        return redirect('cart:cart_view')
        
    except Exception as e:
        print(f"EXCEPTION: {str(e)}")
        messages.error(request, f'Error adding to cart: {str(e)}')
        return redirect('products:product_list')

@login_required
def cart_view(request):
    print("=== CART VIEW ===")
    print(f"User: {request.user}")
    
    try:
        # Force get cart
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.select_related('product').all()
        
        print(f"Cart found: {cart}")
        print(f"Cart items: {cart_items.count()}")
        
        for item in cart_items:
            print(f" - {item.product.name} (Qty: {item.quantity})")
            
    except Cart.DoesNotExist:
        print("Cart does not exist - creating now")
        # Create cart if doesn't exist
        cart = Cart.objects.create(user=request.user)
        cart_items = []
        print(f"New cart created: {cart}")
    
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'cart/cart.html', context)

@login_required
@require_POST
def update_cart_item(request, item_id):
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
                
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart!')
    
    return redirect('cart:cart_view')

@login_required
@require_POST
def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f'{product_name} removed from cart!')
    except CartItem.DoesNotExist:
        messages.error(request, 'Item not found in cart!')
    
    return redirect('cart:cart_view')

# Other views remain same...
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