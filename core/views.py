from django.shortcuts import render, redirect, HttpResponse
from .models import *
import base64
from django.http import JsonResponse
# Create your views here.
# def home(request):
#     products = Products.objects.all()
#     if products:
#         # image_base64 = base64.b64encode(products.image).decode('utf-8')
#         image_s= products[0].image
#         image_base64 = base64.b64encode(image_s).decode('utf-8')
#         # store all the images in a list
#         images = []
#         for product in products:
#             images.append(base64.b64encode(product.image).decode('utf-8'))
            
#         return render(request, 'test.html', {'image_base64': images, 'products': products})
#     return HttpResponse('No image found')
def home(request):
    products = Products.objects.all()
    banner = PromoItems.objects.all().last()
    banner = base64.b64encode(banner.promo_image).decode('utf-8')
    # top 5 best offers
    best_offers = products[:5]
    context = {
        'products': products,
        'banner': banner,
        'best_offers': best_offers
    }
    
    return render(request, 'test.html', context)
def upload_product(request):
    if request.method == 'POST':
        item_name = request.POST['item_name']
        description = request.POST['description']
        price = request.POST['price']
        stock = request.POST['stock']
        # discount = request.POST.get('discount', False)
        discount = True 
        discount_percentage = request.POST['discount_percentage']
        image = request.FILES['image'].read() if 'image' in request.FILES else None
        category_id = request.POST['category']
        category = ProductCategory.objects.get(pk=category_id)
        
        Products.objects.create(
            item_name=item_name,
            description=description,
            price=price,
            stock=stock,
            discount=discount,
            discount_percentage=discount_percentage,
            image=image,
            category=category
        )
        return redirect('upload_product')

    categories = ProductCategory.objects.all()
    return render(request, 'upload_product.html', {'categories': categories})

def upload_promoitems(request):
    # upload to promoitems model
    if request.method == 'POST':
        promo_name = request.POST['promo_name']
        promo_image = request.FILES['promo_image'].read() if 'promo_image' in request.FILES else None
        promo_description = request.POST['promo_description']
        PromoItems.objects.create(
            promo_name=promo_name,
            promo_image=promo_image,
            promo_description=promo_description
        )
        return HttpResponse('Promo Item Uploaded')
    return render(request, 'upload_promo.html')


def product_category(request, product_category):
    if request.method == 'GET':
        # category_name = request.GET['category']
        category_name = product_category
        # in product category, find the id that matches the category name
        category_id = ProductCategory.objects.get(name=category_name)

        products = Products.objects.filter(category=category_id)
        print(products)
        return render(request, 'products_by_category.html', {'products': products, 'category_name': category_name})
    
def product(request, product_id):
    if request.method == 'GET':
        product = Products.objects.get(pk=product_id)
        print(product)
        return render(request, 'product.html', {'product': product})
def generate_unique_key():
    # generate a unique key
    import uuid
    return str(uuid.uuid4())
from django.shortcuts import get_object_or_404
# def add_to_cart(request, product_id):
#     if request.method == 'GET':
#         cart_key = request.session.get('cart_key', None)
#         if not cart_key:
#             cart_key = generate_unique_key()
#             request.session['cart_key'] = cart_key

#         product = get_object_or_404(Products, pk=product_id)
#         existing_cart = Cart.objects.filter(cart_key=cart_key, ordered=False).first()
#         if existing_cart:
#             # Update the existing cart item's quantity instead of creating a new one
#             existing_cart.quantity += 1
#             existing_cart.save()
#         else:
#             Cart.objects.create(cart_key=cart_key, buyer='example', ordered=False, quantity=1, product=product)
#         return HttpResponse('Cart created')
# def add_to_cart(request, product_id):
#     product = Products.objects.get(pk=product_id)
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
#     if not item_created:
#         cart_item.quantity += 1
#         cart_item.save()
    
#     return HttpResponse('Cart created')
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST['id']
        quantity = int(request.POST.get('quantity'))  # Default to 1 if quantity is not provided
        print('product id: ', product_id, 'quantity: ', quantity)
        product = Products.objects.get(pk=product_id)
        
        # if user is anonymous
        if not request.user.is_authenticated:
            # Check if the user has a cart in the session or create one
            if 'cart_id' not in request.session:
                cart = AnonymousCart.objects.create()
                request.session['cart_id'] = cart.pk
            else:
                cart_id = request.session['cart_id']
                cart = get_object_or_404(AnonymousCart, pk=cart_id)

            # Add the product to the cart
            cart_item, created = AnonymousCartItem.objects.get_or_create(cart=cart, product=product)
            print('cart item: ', cart_item)
            print('created: ', created)
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
                
            return JsonResponse({'success': True})
        # if user is authenticated
        else:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, quantity=quantity)
            
            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()
                
            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# quantity in cart
def quantity_in_cart(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart = cart.cartitem_set.count()
            return JsonResponse({'quantity': cart})
        else:
            cart_id = request.session.get('cart_id')
            if cart_id:
                cart = AnonymousCart.objects.get(id=cart_id)
                cart = cart.anonymouscartitem_set.count()
                return JsonResponse({'quantity': cart})
            else:
                return JsonResponse({'quantity': 0})
    return JsonResponse({'quantity': 0})

def view_cart(request):
    context = {}
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = AnonymousCart.objects.get(id=cart_id)
            cart_items = cart.anonymouscartitem_set.all()
        else:
            cart_items = []
    try:
        total_cost = cart.total
        context['cart_items'] = cart_items
        context['total_cost'] = total_cost
    except:
        print('No cart')
    # total_cost = cart.total if cart else 0
    
    return render(request, 'view_cart.html', context)
@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST['id']
        quantity = int(request.POST['quantity'])
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(pk=cart_item_id)
            cart_item.quantity = quantity
            cart_item.save()
            return JsonResponse({'success': True, 'sub_total': cart_item.sub_total, 'total_cost': cart_item.cart.total})
        else:
            cart_item = AnonymousCartItem.objects.get(pk=cart_item_id)
            cart_item.quantity = quantity
            cart_item.save()
        return JsonResponse({'success': True, 'sub_total': cart_item.sub_total, 'total_cost': cart_item.cart.total})
    return JsonResponse({'success': False})

@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        cart_item_id = request.POST['id']
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(pk=cart_item_id)
            # update the cart total
            cart = cart_item.cart
            cart.total -= cart_item.sub_total
            cart_item.delete()
            return JsonResponse({'success': True, 'total_cost': cart.total})
        else:
            cart_item = AnonymousCartItem.objects.get(pk=cart_item_id)
            cart_item.delete()
            return JsonResponse({'success': True, 'total_cost': cart.total})
    return JsonResponse({'success': False})

# to checkout, check if user is authenticated if not require login which is a modal on checkout
# move the cart to the order
# delete the cart
# create an order
# create order items
# delete the cart
def checkout(request):
    if request.method == 'POST':
        
        # get the data from the form to populate the order
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        postal_code = request.POST['postal_code']
        city = request.POST['city']
        country = request.POST['country']
        payment_method = request.POST['payment_method']
        # add the data to the buyer delivery details
        buyer = BuyerDeliveryDetails.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            address=address,
            phone_number=phone_number,
            postal_code=postal_code,
            city=city,
            country=country,
            payment_method=payment_method
        )

        # create an order and populate it with the cart items and the buyer delivery details
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.cartitem_set.all()
            order = Order.objects.create(buyer=buyer, buyer_id_order=request.user)
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            # delete the cart
            # cart.delete()
            return redirect('view_orders')
        else:
            cart = AnonymousCart.objects.get(id=request.session['cart_id'])
            cart_items = cart.anonymouscartitem_set.all()
            order = Order.objects.create(buyer=buyer)
            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
            print(first_name, last_name, email, address, phone_number, postal_code, city)
            # set order session
            request.session['order_id'] = order.id
        # create an order
        return redirect('view_orders')

def view_orders(request):
    if request.user.is_authenticated:
        # print(request.user.username)
        orders = Order.objects.filter(buyer_id_order=request.user)
        order_items = OrderItem.objects.filter(order=orders[0])
    else:
        print(request.session['order_id'])
        # return orders for anonymous user
        orders = Order.objects.filter(id= request.session['order_id'])
        order_items = OrderItem.objects.filter(order=orders[0])
    return render(request, 'view_orders.html', {'orders': orders, 'order_items': order_items})
    

# def checkout(request):
#     if request.method == 'GET':
#         if request.user.is_authenticated:
#             cart = Cart.objects.get(user=request.user)
#             cart_items = cart.cartitem_set.all()
#             # create an order
#             order = Order.objects.create(buyer=request.user.username)
#             for item in cart_items:
#                 OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
#             # delete the cart
#             cart.delete()
#             return redirect('view_cart')
#         else:
#             cart_id = request.session.get('cart_id')
#             if cart_id:
#                 cart = AnonymousCart.objects.get(id=cart_id)
#                 cart_items = cart.anonymouscartitem_set.all()
#                 # create an order
#                 order = Order.objects.create(buyer='Anonymous')
#                 for item in cart_items:
#                     OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
#                 # delete the cart
#                 cart.delete()
#                 return redirect('view_cart')
#             else:
#                 return redirect('view_cart')
#     return redirect('view_cart')

    
from django.core.files.base import ContentFile
# from .models import ProductTestUpload as Product

# loadworkbook
from openpyxl import load_workbook

def read_image_as_binary(image_path):
    with open(image_path, 'rb') as image_file:
        binary_data = image_file.read()
    return binary_data


def upload_products(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        wb = load_workbook(excel_file)
        sheet = wb.active

        for row in sheet.iter_rows(min_row=2, values_only=True):
            name, image_path = row
            product = Product(
                product_name=name,
            )

            # Process image_path and read the image as binary
            print(image_path)
            binary_image = read_image_as_binary(image_path)
            print(binary_image)
            
            # Set the binary image data
            product.image_binary = binary_image

            product.save()

        return HttpResponse('Products uploaded successfully')
    
    return render(request, 'upload_excel.html')

def product_image(request, pk):
    product = Product.objects.get(id=pk)
    image_data = product.image_binary
    return HttpResponse(image_data, content_type='image/jpeg') 
