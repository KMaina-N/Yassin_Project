from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Products)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Contact)
admin.site.register(PromoItems)