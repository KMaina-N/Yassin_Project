# a context processor for displaying all the categories
# in the navbar
from .models import ProductCategory
from .models import*
from django.contrib.auth import get_user_model
user = get_user_model()
def categories(request):
    return {
        'categories': ProductCategory.objects.all()
    }

def cart(request):
    if request.user.is_authenticated:
        # cart is the number of cartitems in the cart
        # cart = Cart.objects.filter(user=request.user).count()
        print(request.user)
        try: 
            cart = Cart.objects.get(user=request.user)
            print(cart.cartitem_set)
            cart = cart.cartitem_set.count()
            return {
                'cart': cart
            }
        except:
            return {
                'cart': 0
            }
    else:
        cart_id = request.session.get('cart_id')
        print(cart_id)
        if cart_id:
            try:
                cart = AnonymousCart.objects.get(id=cart_id)
                cart = cart.anonymouscartitem_set.count()
                return {
                    'cart': cart
                }
            except:
                return {
                    'cart': 0
                }
        else:
            return {
                'cart': 0
            }
