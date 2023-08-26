from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_product/', views.upload_product, name='upload_product'),
    path('upload_promoitems/', views.upload_promoitems, name='upload_promoitems'),
    path('product-category/<str:product_category>', views.product_category, name='product_category'),
    path('product/<int:product_id>', views.product, name='product'),
]