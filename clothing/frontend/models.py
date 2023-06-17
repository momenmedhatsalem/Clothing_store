from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
# Create your models here.
class MyUser(AbstractUser):
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
    address = models.CharField(max_length=50, default="")
    phone = models.CharField(max_length=10, default="")
    country_code = models.CharField(max_length=10, default="")
    pass 

class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="static/images", default="")

    def __str__(self):
        return self.product_name




class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total for item in self.items.all())

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'
    
    @property
    def total(self):
        return self.product.price * self.quantity
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('PR', 'Processing'),
        ('S', 'Shipped'),
        ('D', 'Delivered'),
    )

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

    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered_at = models.DateTimeField(auto_now=True)
    
    order_number = models.CharField(max_length=32, null=False, editable=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='P')
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHOD_CHOICES)

    # other fields ...

    def _generate_order_number(self):
        """ Generate a random, unique order number using UUID """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """ Override the original save method to set the order number if it hasn't been set already. """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order of {self.user.username}"