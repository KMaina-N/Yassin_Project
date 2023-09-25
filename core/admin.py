from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Products)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(OrderItem)
# admin.site.register(Order)
admin.site.register(Contact)
admin.site.register(PromoItems)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(AnonymousCart)
admin.site.register(AnonymousCartItem)
admin.site.register(ProductTestUpload)
admin.site.register(BuyerDeliveryDetails)
admin.site.register(Sale)