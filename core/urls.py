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

    # shop urls
    path('dashboard/', views.dashboard, name='dashboard'),
    path('search-inventory/', views.search_inventory, name='inventory_search'),
    path('products/', views.products_admin, name='products'),
    path('add-products-page/', views.add_products_page, name='add_product'),
    path('edit-product/<int:pk>', views.edit_product, name='edit_product'),
    path('delete-product/<int:pk>', views.delete_product, name='delete_product'),
    path('orders/', views.admin_orders, name='orders'),
    path('order-details/<int:pk>', views.admin_order_details, name='order_details'),
    path('deliver_order/<int:pk>', views.deliver_order, name='deliver_order'),
    path('dangling_carts/', views.admin_carts, name='dangling_carts'),
    path('cart_details/<int:pk>', views.view_admin_cart, name='cart_details'),
    path('sales/', views.sales, name='sales'),
    path('sale_details/<int:pk>', views.sales_details, name='sales_details'),
    path('admin_login/', views.admin_login, name='admin_login'),
    # path('test/', views.post_test, name='test'),
    
    path('view-cart/', views.view_cart, name='view_cart'),
    # upload excel file
    path('upload_products/', views.upload_products, name='upload_products'),
    # view products
    path('product-image/<int:pk>', views.product_image, name='view_products'),
]