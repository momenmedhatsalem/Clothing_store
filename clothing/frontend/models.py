from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random
# Create your models here.
from django.db import models
import os
from django.urls import reverse

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
    customized = models.BooleanField(default=False)
    product_name = models.CharField(max_length=50)
    category = models.ManyToManyField('Category', through='ProductCategory')
    label = models.CharField(choices=LABEL_CHOICES, max_length=11, default="")
    subcategory = models.CharField(choices= SUB_CATEGORY_CHOICES ,max_length=50, default="")
    price = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="static", default="", blank=True, null=True)
    material = models.CharField(max_length=50, default="Coton 100%")
    description = models.TextField(default="Are you looking for a t shirt that is comfortable, stylish and affordable? Look no further than our new collection of t shirts, designed to suit any occasion and personality. Whether you want to express your creativity, show your support for a cause, or simply enjoy a casual day out, we have the perfect t shirt for you. Our t shirts are made from high-quality cotton, which is soft, breathable and durable. They come in a variety of colors, sizes and designs, so you can find the one that matches your style and mood.  Our t shirts are easy to wash and care for, and they will not fade or shrink over time. They are also eco-friendly and ethically produced, so you can wear them with confidence and pride. Order your t shirt today and enjoy free shipping for orders over EGP 500. You will love how you look and feel in our t shirts, and so will everyone else. Don't miss this opportunity to get the best t shirt ever.")
    path = models.CharField(max_length=50, default="")
    # Add a reference to the associated design
    FrontCanva = models.OneToOneField('FrontCanva', on_delete=models.CASCADE, null=True, blank=True)
    BackCanva = models.OneToOneField('BackCanva', on_delete=models.CASCADE, null=True, blank=True)
    def get_absolute_url(self):
        if self.customized:
            return reverse('customized_view', args=[str(self.id)])
        else:
            return f"/product_detail/{self.id}/"


class FrontCanva(models.Model):
    # Fields to store the properties of an object
    image = models.ImageField(upload_to="static/designs", null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)
    
class BackCanva(models.Model):
    # Fields to store the properties of an object
    image = models.ImageField(upload_to="static/designs", null=True, blank=True)
    url = models.URLField(max_length=200, null=True, blank=True)




class Category(models.Model):
    name = models.CharField(choices=Product.CATEGORY_CHOICES, max_length=2)

class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to="static", default="", blank=True, null=True)
    path = models.CharField(max_length=50, default="")   
    color = models.CharField(max_length=50, default="")
    def __str__(self):
        return self.product.product_name
    
class MyUser(AbstractUser):
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=10, default="")
    country_code = models.CharField(max_length=10, default="")
    favorites = models.ManyToManyField(Product)
    



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
            return "{:.2f}".format(500 - float(self.total_price))
        else:
            return "{:.2f}".format(0)
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
    
GOVERNORATE_CHOICES = (
    ('Ad Daqahliyah', 'Ad Daqahliyah'),
    ('Al Bahr al Ahmar', 'Al Bahr al Ahmar'),
    ('Al Buhayrah', 'Al Buhayrah'),
    ('Al Fayyum', 'Al Fayyum'),
    ('Al Gharbiyah', 'Al Gharbiyah'),
    ('Al Iskandariyah', 'Al Iskandariyah'),
    ('Al Isma\'iliyah', 'Al Isma\'iliyah'),
    ('Al Jizah', 'Al Jizah'),
    ('Al Minufiyah', 'Al Minufiyah'),
    ('Al Minya', 'Al Minya'),
    ('Al Qahirah', 'Al Qahirah'),
    ('Al Qalyubiyah', 'Al Qalyubiyah'),
    ('Al Wadi al Jadid', 'Al Wadi al Jadid'),
    ('Ash Sharqiyah', 'Ash Sharqiyah'),
    ('As Suways', 'As Suways'),
    ('Aswan', 'Aswan'),
    ('Asyut', 'Asyut'),
    ('Bani Suwayf', 'Bani Suwayf'),
    ('Bur Sa\'id', 'Bur Sa\'id'),
    ('Dumyat', 'Dumyat'),
    ('Janub Sina\'', 'Janub Sina\''),
    ('Kafr ash Shaykh', 'Kafr ash Shaykh'),
    ('Matruh', 'Matruh'),
    ('Qina', 'Qina'),
    ('Shamal Sina\'', 'Shamal Sina\''),
    ('Suhaj', 'Suhaj')
    )

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
    governorate = models.CharField(max_length=100, choices=GOVERNORATE_CHOICES)
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

