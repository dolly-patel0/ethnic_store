from .models import Cart

def cart_total(request):
    print("=== CONTEXT PROCESSOR ===")
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total_items = cart.total_items
            total_price = cart.total_price
            print(f"Context - User: {request.user}, Cart Items: {total_items}")
            return {
                'cart_total_items': total_items,
                'cart_total_price': total_price,
                'user_cart': cart  # Add this for debugging
            }
        except Cart.DoesNotExist:
            print("Context - No cart found")
            return {'cart_total_items': 0, 'cart_total_price': 0, 'user_cart': None}
    else:
        print("Context - User not authenticated")
        return {'cart_total_items': 0, 'cart_total_price': 0, 'user_cart': None}