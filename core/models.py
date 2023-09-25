from django.db import models
from django.contrib.auth.models import User, AnonymousUser
import random
# Create your models here.
class Products(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    discount = models.BooleanField(default=False)
    discount_percentage = models.IntegerField()
    
    # image as binary data
    image = models.BinaryField(null=True, blank=1, editable=False)
    category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE)

    # count number of items sold based on orders placed and use it in the field sold
    sold = models.IntegerField(default=0)

    # get the number of items sold based on number of orders placed on it and update the field sold

    def get_sold(self):
        orders = OrderItem.objects.filter(product=self)
        sold = 0
        for order in orders:
            sold += order.quantity
        return sold

    def __str__(self):
        return self.item_name

    class Meta:
        ordering = ('item_name',)
        verbose_name_plural = 'Products'
    

# product category as a separate model taking advantage of the relationship between the two models
class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Product Categories'

class CartItem(models.Model):
    # Allow the cart to be nullable to support anonymous users
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"{self.quantity} x {self.product.item_name}"

    # get total cost of the cart item and save it in the total_cost field
    def save(self, *args, **kwargs):
        self.sub_total = self.quantity * self.product.price
        super(CartItem, self).save(*args, **kwargs)
        if self.cart:
            self.cart.calculate_total() 

    def delete(self, *args, **kwargs):
        super(CartItem, self).delete(*args, **kwargs)
        if self.cart:
            self.cart.calculate_total()
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Products, through='CartItem')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_of_creation = models.DateTimeField(auto_now_add=True)
  
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        else:
            return "Anonymous Cart"
    def calculate_total(self):
        cart_items = self.cartitem_set.all()
        total_cost = sum(item.sub_total for item in cart_items)
        self.total = total_cost
        self.save()
        
    # def save(self, *args, **kwargs):
    #     # Update total when adding a new cart item
    #     self.total = sum([item.sub_total for item in self.cartitem_set.all()])
    #     super(Cart, self).save(*args, **kwargs)

# Allow the anonymous user to have a cart
AnonymousUser.cart = property(lambda u: Cart.objects.get_or_create(user=None)[0])

class AnonymousCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Products, through='AnonymousCartItem')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # cart_ready = models.BooleanField(default=False)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        else:
            return "Anonymous Cart"
    def calculate_total(self):
        cart_items = self.anonymouscartitem_set.all()
        total_cost = sum(item.sub_total for item in cart_items)
        self.total = total_cost
        self.save()

class AnonymousCartItem(models.Model):
    cart = models.ForeignKey('AnonymousCart', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"{self.quantity} x {self.product.item_name}"

    # get total cost of the cart item and save it in the total_cost field
    def save(self, *args, **kwargs):
        self.sub_total = self.quantity * self.product.price
        super(AnonymousCartItem, self).save(*args, **kwargs)
        if self.cart:
            self.cart.calculate_total() 

    def delete(self, *args, **kwargs):
        super(AnonymousCartItem, self).delete(*args, **kwargs)
        if self.cart:
            self.cart.calculate_total()

class BuyerDeliveryDetails(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    email = models.EmailField()
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Croatia')
    payment_method = models.CharField(max_length=100)
    
    username = models.CharField(max_length=100, null=True, blank=True)

    # def __str__(self):
    #     return self.first_name + ' ' + self.last_name
    
    def save(self, *args, **kwargs):
        # create username by concatenating first name and last name and adding a random number at the end
        self.username = self.first_name + self.last_name + str(random.randint(1, 1000))
        super(BuyerDeliveryDetails, self).save(*args, **kwargs)

# order based on the cart include the details of the buyer entered in the checkout form
class Order(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_cart = models.ForeignKey(AnonymousCart, on_delete=models.CASCADE, null=True, blank=True)
    # buyer from the buyer delivery details
    buyer = models.ForeignKey(BuyerDeliveryDetails, on_delete=models.CASCADE, null=True, blank=True)
    buyer_id_order = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    # cost_of_order = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        cart = Cart.objects.filter(buyer=self.buyer, ordered=False)
        total_cost = 0
        for item in cart:
            total_cost += item.product.price
        return total_cost

    def get_total_quantity(self):
        cart = Cart.objects.filter(buyer=self.buyer, ordered=False)
        total_quantity = 0
        for item in cart:
            total_quantity += item.quantity

        return total_quantity
    def get_all_items(self):
        cart = Cart.objects.filter(buyer=self.buyer, ordered=False)
        return cart
    
    # def save(self, *args, **kwargs):
    #     # create username by concatenating first name and last name and adding a random number at the end
    #     self.cost_of_order = self.get_total_cost()
    #     super(Order, self).save(*args, **kwargs)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return '{}'.format(self.id)
    
    def get_cost(self):
        return self.product.price * self.quantity
    
    def save(self, *args, **kwargs):
        self.sub_total = self.product.price * self.quantity
        self.total = self.sub_total
        super(OrderItem, self).save(*args, **kwargs)
    
    
    # get the products

# when admin delivers the order, the order is make it as a sale
class Sale(models.Model):
    date_of_sale = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    # quantity = models.IntegerField()
    # product = models.CharField(max_length=100)
    # total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # buyer = models.ForeignKey(BuyerDeliveryDetails, on_dele
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Contact Us'

class PromoItems(models.Model):
    promo_image = models.BinaryField(null=True, blank=1, editable=True)
    promo_name = models.CharField(max_length=100)
    promo_description = models.TextField()

    def __str__(self):
        return self.promo_name
    
    class Meta:
        verbose_name_plural = 'Promo Items'


class ProductTestUpload(models.Model):
    product_name = models.CharField(max_length=100)
    image_binary = models.BinaryField(null=True, blank=1, editable=False)

    class Meta:
        verbose_name_plural = 'Product Test Upload'


# app config variables
class ConfigVariables(models.Model):
    store_email = models.EmailField()
    store_phone = models.CharField(max_length=20, blank=True, null=True)
    store_address = models.CharField(max_length=200, blank=True, null=True)
    store_postal_code = models.CharField(max_length=20, blank=True, null=True)
    store_city = models.CharField(max_length=100, blank=True, null=True)
    store_country = models.CharField(max_length=100, default='Croatia')
    store_name = models.CharField(max_length=100, blank=True, null=True)
    store_description = models.TextField()
    store_logo = models.BinaryField(null=True, blank=1, editable=False)
    store_favicon = models.BinaryField(null=True, blank=1, editable=False)
    store_facebook = models.CharField(max_length=100, blank=True, null=True)
    store_instagram = models.CharField(max_length=100, blank=True, null=True)

class ExceptionLog(models.Model):
    name = models.CharField(max_length=100)
    exception_message = models.TextField()
    exception_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.exception_name