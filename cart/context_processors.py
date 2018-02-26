from .cart import Cart
from .utils import get_cart_from_request

def cart(request):
    """Expose the number of items in cart."""
    cart = get_cart_from_request(request)
    return {'cart_counter': cart.quantity}


# return {'cart': Cart(request)}







# A context processor is a Python function that takes the request object as an
# argument and returns a dictionary that gets added to the request context