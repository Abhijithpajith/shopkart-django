from .models import *
from .views import _cart_id

def counter(request):
    cart_count=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            carts=cart.objects.filter(cart_id=_cart_id(request))
            cart_items=cartitem.objects.all().filter(cart=carts[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)
