from django import template
import base64

register = template.Library()

@register.filter
def to_base64(value):
    return base64.b64encode(value).decode('utf-8')
