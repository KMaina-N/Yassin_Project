from django import template
import base64

register = template.Library()

@register.filter
def to_base64(value):
    return base64.b64encode(value).decode('utf-8')


# count the number of items in the cart associated with the user or session
@register.simple_tag
def cart_item_count(user):
    return 'hello'
    # if user.is_authenticated:
    #     return user.cart.items.count()
    # else:
    #     return 0
