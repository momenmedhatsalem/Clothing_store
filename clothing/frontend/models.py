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
    id = models.AutoField(primary_key=True, auto_created=True)

    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="static/images", default="")

    def get_absolute_url(self):
        return f"/product/{self.id}/"

    def __str__(self):
        return self.product_name

class PromoCode(models.Model):
    code = models.CharField(max_length=15)
    discount = models.FloatField()
    max_discount = models.FloatField(default=100)

    
class CartManager(models.Manager):
    def get_anonymous_cart(self, session):
        cart = session.get('cart', [])
        products = Product.objects.filter(pk__in=[item['product_id'] for item in cart])
        cart_items = [{'product': product, 'quantity': int(next(item['quantity'] for item in cart if item['product_id'] == product.pk)), 'total': "{:.2f}".format(product.price * int(next(item['quantity'] for item in cart if item['product_id'] == product.pk)))} for product in products]
        
        # calculate total price before discount
        total_price_before_discount = sum(float(item['total']) for item in cart_items)
        
        # apply promo code discount if available
        promo_code = session.get('applied_promo_code')
        if promo_code:
            promo = PromoCode.objects.filter(code=promo_code).first()
            if promo:
                discount = promo.discount
                max_discount = promo.max_discount
                cart_total = total_price_before_discount
                discount_amount = cart_total * discount
                discount_amount = min(discount_amount, max_discount)
                # calculate total price after discount
                total_price = sum(float(item['total']) for item in cart_items) - discount_amount 
        else:
            total_price = total_price_before_discount
            discount_amount = 0.00
        return {
            'cart_items': cart_items,
            'total_price_before_discount': "{:.2f}".format(total_price_before_discount),
            'total_price': "{:.2f}".format(total_price),
            'discount': "{:.2f}".format(discount_amount)
        }


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        PromoCode, on_delete=models.SET_NULL, blank=True, null=True)
    objects = CartManager()

    def __str__(self):
        return f"Cart of {self.user.username}"

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
    
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'
    
    @property
    def total(self):
        total = float(self.product.price) * int(self.quantity)
        return float("{:.2f}".format(total))
    
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