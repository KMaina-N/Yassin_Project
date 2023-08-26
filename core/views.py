from django.shortcuts import render, redirect, HttpResponse
from .models import *
import base64
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
    
    context = {
        'products': products,
        'banner': banner
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