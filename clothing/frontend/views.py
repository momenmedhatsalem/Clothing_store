from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import reverse
from frontend.models import Product, MyUser, Cart, CartItem, Order, PromoCode
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms

# Create your views here.
from django.contrib.auth import get_user_model
# User = get_user_model()


from django.shortcuts import render, redirect
from django.forms import Form, CharField, EmailField, PasswordInput
from django.contrib.auth.models import User
from django.contrib.auth import login


from django.utils.crypto import get_random_string


from django.views.decorators.http import require_http_methods
import json
def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products':products})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "login.html",
                {"message": "Invalid email/phone and/or password."},
            )
    else:
        return render(request, "login.html")

# A form class that takes the username, email, and password of the user
class RegisterForm(Form):
    first_name = CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = EmailField(label="Email", max_length=200, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    address = CharField(label="Address", max_length=500, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    # A phone number field that allows the user to choose a country code from a tab
    # and sets the default to +20 Egypt
    phone_number = PhoneNumberField(label="Phone Number", initial="",
                                     widget=PhoneNumberPrefixWidget(initial="EG", 
                                                                    attrs={'class': 'form-control'}))

# A view function that displays the register form and handles the registration
def register_view(request):
    # If the request is a GET request, create a blank RegisterForm and render it
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "register.html", {"form": form})
    # If the request is a POST request, get the data from the form and validate it
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        # If the form is valid, create a new user and log them in
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            # Generate a unique username from the email address
            username = email.split('@')[0]
            while MyUser.objects.filter(username=username).exists():
                username = f"{username}_{get_random_string()}"



            phone_number = form.cleaned_data["phone_number"]
            user = MyUser.objects.create_user(first_name=first_name, phone=phone_number, username=username, last_name=last_name, email=email, password=password)
            login(request, user)
            # Redirect to the ecommerce website builder or another page
            return HttpResponseRedirect(reverse("index"))
        
        # If the form is not valid, render it again with the errors
        else:
            return render(request, "register.html", {"form": form})
        
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            # Handle the case where the product does not exist
            pass
        if request.user.is_authenticated:
            # Handle authenticated user
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                # Handle the case where the cart does not exist
                cart = Cart.objects.create(user=request.user)
            CartItem.objects.create(cart=cart, product=product)
        else:
            # Handle anonymous user
            cart = request.session.get('cart', [])
            products = Product.objects.filter(pk__in=[item['product_id'] for item in cart])
            context = {'cart': [{'product': product, 'quantity': next(item['quantity'] for item in cart if item['product_id'] == product.pk)} for product in products]}
        return render(request, 'cart.html', context)
    else:
        existing_options = [
        {'value': 1, 'label': '1'},
        {'value': 2, 'label': '2'},
        {'value': 3, 'label': '3'},
        {'value': 4, 'label': '4'},
        {'value': 5, 'label': '5'},
        {'value': 6, 'label': '6'},
        {'value': 7, 'label': '7'},
        {'value': 8, 'label': '8'},
        {'value': 9, 'label': '9'},
        {'value': 10, 'label': '10'},
        ]

        
        if request.user.is_authenticated:
            # Handle authenticated user
            try:
                cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                # Handle the case where the cart does not exist
                cart = Cart.objects.create(user=request.user)
            CartItems = CartItem.objects.filter(cart=cart)
            discount = cart.discount

            # check if authenticated user has applied a promo code
            if cart.coupon:
                promo_code = cart.coupon.code
            else:
                promo_code = False
            context = {'promocode': promo_code, 'existing_options': existing_options,
                       'cart': CartItems, 'user_cart': cart, 'discount': discount}
        else:
            # Handle anonymous user
            # Check if user has applied a promo code
            if 'applied_promo_code' in request.session:
                promo_code = request.session['applied_promo_code']
            else:
                promo_code = False

            cart = Cart.objects.get_anonymous_cart(request.session)
            price_before = cart['total_price_before_discount']
            total_price = cart['total_price']
            discount = float(cart['discount'])
            context = {'promocode': promo_code, 'existing_options': existing_options,
                       'cart': cart['cart_items'], 'user_cart': {'total_price': total_price, 'total_price_before_discount': price_before}, 'discount': "{:.2f}".format(discount)}
        return render(request, 'cart.html', context )

def checkout(request):
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.get(user=user)
        order = Order.objects.create(user=user, cart=cart)
        # Redirect to the order confirmation page
        return render(request, 'orderconfirm.html', {"order_number": order.order_number})
    else:
        if request.user.is_authenticated:
            # Handle authenticated user
            cart = Cart.objects.get(user=request.user)
            CartItems = CartItem.objects.filter(cart=cart)
            context = {'cart': CartItems, 'user_cart': cart}
        else:
            # Handle anonymous user
            cart = request.session.get('cart', [])
            products = Product.objects.filter(pk__in=[item['product_id'] for item in cart])
            context = {'cart':  [{'product': product,
                                   'quantity': next(item['quantity'] for item in cart
                                                     if item['product_id'] == product.pk),
                                                       'total': product.price * next(item['quantity']
                                                                                      for item in cart if item['product_id'] == product.pk)}
                                                                                        for product in products], 'user_cart': {'total_price': sum(product.price * next(item['quantity'] for item in cart if item['product_id'] == product.pk) for product in products)}}

        return render(request, 'checkout.html', context)
        
def product(request, product_id):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(pk=product_id)
        request.session['product'] = product
        return HttpResponseRedirect(reverse('product'))
    else:
        product = request.session.get('product')
        return render(request, 'product.html', {'product':product})
    
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_item, created = cart_item.objects.get_or_create(
            cart=request.cart,
            product=product,
        )
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()
        return redirect('cart_detail')
    context = {
        'product': product,
    }
    return render(request, 'product_detail.html', context)



#@require_http_methods(["POST", "PUT"])
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'GET':
        quantity = int(request.POST.get('quantity', 1))
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            a_cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if not created:
                a_cart_item.quantity += quantity
            else:
                a_cart_item.quantity = quantity
            a_cart_item.save()
            
        else:
            # Handle anonymous user
            cart = request.session.get('cart', [])
            cart_item = next((item for item in cart if item['product_id'] == product_id), None)
            if cart_item:
                cart_item['quantity'] += quantity
            else:
                cart.append({'product_id': product_id, 'quantity': quantity})
            request.session['cart'] = cart
    elif request.method == 'PUT':
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            a_cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            a_cart_item.quantity = quantity
            a_cart_item.save()
            total = a_cart_item.total
            total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount
        else:
            # Handle anonymous user

            product = Product.objects.get(pk=product_id)
            cart = request.session.get('cart', [])
            cart_item = next((item for item in cart if item['product_id'] == product_id), None)

            if cart_item:
                cart_item['quantity'] = quantity
            else:
                cart.append({'product_id': product_id, 'quantity': quantity})

            request.session['cart'] = cart
            total = product.price * int(quantity)

            anonymous_cart = Cart.objects.get_anonymous_cart(request.session)
            total_price = anonymous_cart['total_price']
            total_price_before_discount = anonymous_cart['total_price_before_discount']
        # calculate discount
        discount = float(total_price_before_discount) - float(total_price)
        return JsonResponse({'success': True,'cart_total': total_price, 'total': total, 'discount': "{:.2f}".format(discount), 'cart_total_before_discount': total_price_before_discount})
    return redirect('cart')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

@csrf_exempt

def toggle_night_mode(request, mode):
    if request.method == 'PUT':
        if mode == 'True':
            request.session['darkmode'] = True
        else:
            request.session['darkmode'] = False
        return JsonResponse({'night_mode':  request.session.get('darkmode')})
    else:
        night_mode = request.session.get('darkmode')
        
        return JsonResponse({'night_mode':  night_mode})


def profile(request):
    return render(request, 'profile.html')


#Unmaitained

def remove_from_cart(request, product_id):
    if request.method == 'PUT':
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            cart = Cart.objects.get(user=request.user)
            CartItem.objects.filter(cart=cart, product=product).delete()
            cart_total_price = cart.total_price
        else:
            # Handle anonymous user
            cart = request.session.get('cart', [])
            # check if the product is already in the cart
            cart_item = next((item for item in cart if item['product_id'] == product_id), None)
            if cart_item:
                # update the quantity if the product is already in the cart
                cart.remove(cart_item)
            request.session['cart'] = cart
        # Return a JSON response with the updated cart total
            anonymous_cart = Cart.objects.get_anonymous_cart(request.session)
            cart_total_price = anonymous_cart['total_price']
        return JsonResponse({'cart_total': cart_total_price})
    else:
        # Handle other request methods (e.g. GET) as before
        ...

#Unmaintained
def edit_profile(request):
    return render(request, 'edit_profile.html')

def change_password(request):
    return render(request, 'change_password.html')




@require_http_methods(["PUT"])
def apply_coupon(request):
    data = json.loads(request.body)
    promo_code = data.get('promo_code')
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        anonymous_cart = Cart.objects.get_anonymous_cart(request.session)
        cart_total_price = anonymous_cart['total_price']
    
    promo = PromoCode.objects.filter(code=promo_code).first()
    if promo:
        if request.user.is_authenticated:
            # check if code is already applied
            if cart.coupon and cart.coupon.code == promo_code:
                return JsonResponse({'error': 'Code already applied'}, status=400)
            
            # remove old coupon if applied
            if cart.coupon:
                cart.coupon = None
            
            # apply the new promo code
            cart.coupon = promo
            cart.save()
            
            # recalculate cart total with discount applied
            total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount
        else:
            # check if code is already applied
            if 'applied_promo_code' in request.session and request.session['applied_promo_code'] == promo_code:
                return JsonResponse({'error': 'Code already applied'}, status=400)
            
            # remove old coupon if applied
            if 'applied_promo_code' in request.session:
                del request.session['applied_promo_code']
            
            # apply the new promo code
            request.session['applied_promo_code'] = promo.code
            
            # recalculate anonymous cart total with discount applied
            anonymous_cart = Cart.objects.get_anonymous_cart(request.session)
            total_price = anonymous_cart['total_price']
            total_price_before_discount = anonymous_cart['total_price_before_discount']
        
        # calculate discount
        discount = float(total_price_before_discount) - float(total_price)

        return JsonResponse({'error': False, 'cart_total': total_price, 'discount': "{:.2f}".format(discount)})
    else:
        return JsonResponse({'error': 'Invalid promo code'}, status=400)
    
@require_http_methods(["PUT"])
def remove_coupon(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        anonymous_cart = Cart.objects.get_anonymous_cart(request.session)
        cart_total_price = anonymous_cart['total_price']
    
    if request.user.is_authenticated:
        # remove coupon if applied
        if cart.coupon:
            cart.coupon = None
            cart.save()
            
            # recalculate cart total with discount removed
            total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount
    else:
        # remove coupon if applied
        if 'applied_promo_code' in request.session:
            del request.session['applied_promo_code']
            
        # recalculate anonymous cart total with discount removed
        anonymous_cart = Cart.objects.get_anonymous_cart(request.session)
        total_price = anonymous_cart['total_price']
        total_price_before_discount = anonymous_cart['total_price_before_discount']
    
    return JsonResponse({'error': False, 'cart_total': total_price})