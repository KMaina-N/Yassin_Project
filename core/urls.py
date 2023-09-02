from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_product/', views.upload_product, name='upload_product'),
    path('upload_promoitems/', views.upload_promoitems, name='upload_promoitems'),
    path('product-category/<str:product_category>', views.product_category, name='product_category'),
    path('product/<int:product_id>', views.product, name='product'),
    # add to cart url with product id and amount as parameters with the structure: /add-to-cart/?product_id=1&amount=2
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('quantity_in_cart/', views.quantity_in_cart, name='quantity_in_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('view_orders/', views.view_orders, name='view_orders'),
    # path('test/', views.post_test, name='test'),
    
    path('view-cart/', views.view_cart, name='view_cart'),
    # upload excel file
    path('upload_products/', views.upload_products, name='upload_products'),
    # view products
    path('product-image/<int:pk>', views.product_image, name='view_products'),
]