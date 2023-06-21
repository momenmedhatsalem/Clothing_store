from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import uuid
# Create your models here.
class MyUser(AbstractUser):
    country = models.CharField(max_length=50, default="")
    city = models.CharField(max_length=50, default="")
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
        # calculate shipping cost for anonymous user
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

        # default shipping cost
        shipping_cost = 25.99  
        if float(total_price) > 1000:
            shipping_cost = 0
        if shipping_cost > 0:
            shipping_remainder = 1000 - total_price
        else:
            shipping_remainder = 0
        return {
            'cart_items': cart_items,
            'total_price_before_discount': "{:.2f}".format(total_price_before_discount),
            'total_price': "{:.2f}".format(total_price),
            'discount': "{:.2f}".format(discount_amount),
            'shipping_cost': "{:.2f}".format(shipping_cost),
            'final_price': "{:.2f}".format(float(total_price) + float(shipping_cost)),
            'shipping_remainder': "{:.2f}".format(shipping_remainder)
        }
        


class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ordered = models.BooleanField(default=False)
    coupon = models.ForeignKey(
        PromoCode, on_delete=models.SET_NULL, blank=True, null=True)
    objects = CartManager()
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=25.99)
    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def shipping_remainder(self):
        if self.shipping_cost > 0:
            return 1000 - self.total_price
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
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2)


    class Meta:
        ordering = ('-created',)

    def _generate_order_number(self):
        """ Generate a random, unique order number using UUID """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """ Override the original save method to set the order number if it hasn't been set already. """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)
    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    customized = models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity

