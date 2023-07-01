from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random
# Create your models here.
from django.db import models
import os
def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    name = filename.split('_')[0]
    filename = f'{name}.{ext}'
    return os.path.join('static/images', filename)

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('M', 'Men'),
        ('W', 'Women'),
        ('K', 'Kids'),
        ('A', 'Accessories'),  
    )

    SUB_CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('SW', 'Sport wear'),
    ('OW', 'Outwear')
    )

    LABEL_CHOICES = (
        ('NEW', 'primary'),
        ('BEST Seller', 'secondary'),
        ('N', '')
    )
    
    product_id = models.AutoField
    id = models.AutoField(primary_key=True, auto_created=True)

    product_name = models.CharField(max_length=50)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=11, default="")
    subcategory = models.CharField(choices= SUB_CATEGORY_CHOICES ,max_length=50, default="")
    price = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to=rename_image, default="", blank=True, null=True)
    material = models.CharField(max_length=50, default="Coton 100%")
    description = models.TextField(default="Description")
    
    def get_absolute_url(self):
        return f"/product_detail/{self.id}/"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=rename_image, default="", blank=True, null=True)


    def __str__(self):
        return self.product.product_name
    
class MyUser(AbstractUser):
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=10, default="")
    country_code = models.CharField(max_length=10, default="")
    favorites = models.ManyToManyField(Product)
    pass 



class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="psize")
    size = models.CharField(max_length=10 , blank=True, null=True)
    quantity = models.PositiveIntegerField( blank=True, null=True)

    class Meta:
        unique_together = ('product', 'size')

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="pcolor")
    color = models.CharField(max_length=10 , blank=True, null=True)
    color_id = models.CharField(max_length=10 , blank=True, null=True)
    quantity = models.PositiveIntegerField( blank=True, null=True)

    class Meta:
        unique_together = ('product', 'color')

class Design(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='designs/')

    def __str__(self):
        return f'Design by {self.user} for {self.product}'
    
class PromoCode(models.Model):
    code = models.CharField(max_length=15)
    discount = models.FloatField()
    max_discount = models.FloatField(default=100)

    

        


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null= True, blank = True)
    applied_coupons = models.ManyToManyField(PromoCode, blank=True,related_name="Applied_Coupons")
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        PromoCode, on_delete=models.SET_NULL, blank=True, null=True)

    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=25.99)
    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def shipping_remainder(self):
        if self.shipping_cost > 0:
            return 500 - float(self.total_price)
        else:
            return 0
    @property
    def discount(self):
        if self.coupon:
            total_price = sum(item.total for item in self.items.all())
            discount_amount = total_price * self.coupon.discount
            max_discount = self.coupon.max_discount
            return min(discount_amount, max_discount)
        else:
            return 0
    
    @property
    def total_price_before_discount(self):
        total_price = sum(item.total for item in self.items.all())
        return "{:.2f}".format(total_price)
    
    @property
    def total_price(self):
        total_price = sum(item.total for item in self.items.all())
        total_price -= self.discount
        return "{:.2f}".format(total_price)
    
    @property
    def final_price(self):
        return float(self.total_price) + float(self.shipping_cost)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", null=True)
    customized = models.BooleanField(default=False)
    size = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)
    def __str__(self):
        return f'{self.product.product_name} ({self.quantity})'
    
    @property
    def total(self):
        total = float(self.product.price) * int(self.quantity)
        return float("{:.2f}".format(total))
    

class Address(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=True)
    country = models.CharField(max_length=100, default='Egypt')
    address = models.CharField(max_length=100)
    street_name = models.CharField(max_length=200)
    building = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    governorate = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    Nearest_landmark = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Address of {self.user.first_name}"
    
class Order(models.Model):

    STATUS_CHOICES = [
        ('P', 'Placed'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
    ]

    PAYMENT_METHOD_CHOICES = (
        ('CC', 'Credit Card'),
        ('VS', 'Visa'),
        ('MC', 'Master Card'),
        ('COD', 'Cash On Delivery'),
        ('VF', 'Vodafone'),
        ('OG', 'Orange'),
        ('WE', 'Wepay'),
        ('PP', 'Paypal'),
        ('BT', 'Bank Transfer'),
    )

    user = models.ForeignKey(MyUser, on_delete=models.SET_NULL, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    phone = models.CharField(max_length=100)
    coupon = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=32, null=False, editable=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='Credit Card')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=25.99)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')

    @property
    def get_payment_method_display(self):
        payment_methods = dict(self.PAYMENT_METHOD_CHOICES)
        return payment_methods[self.payment_method]
    
    class Meta:
        ordering = ('-created',)

    def _generate_order_number(self):
        """ Generate a random, unique 12-digit order number """
        order_number = str(random.randint(10**11, 10**12 - 1))
        while Order.objects.filter(order_number=order_number).exists():
            order_number = str(random.randint(10**11, 10**12 - 1))
        return order_number

    def save(self, *args, **kwargs):
        """ Override the original save method to set the order number if it hasn't been set already. """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.order_number}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    customized = models.BooleanField(default=False)
    size = models.CharField(max_length=10, blank=True, null=True)
    color = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

