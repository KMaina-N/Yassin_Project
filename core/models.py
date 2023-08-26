from django.db import models

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

class Order(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return 'Order {}'.format(self.id)
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return '{}'.format(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    
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