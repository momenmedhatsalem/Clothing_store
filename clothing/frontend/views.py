from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import reverse
from frontend.models import Product, MyUser, Cart, CartItem, Order
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



def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products':products})



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "login.html",
                {"message": "Invalid username and/or password."},
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
        product = Product.objects.get(pk=product_id)
        if request.user.is_authenticated:
            # Handle authenticated user
            cart = Cart.objects.get(user=request.user)
            CartItem.objects.create(cart=cart, product=product)
        else:
            # Handle anonymous user
            cart = request.session.get('cart', [])
            products = Product.objects.filter(pk__in=[item['product_id'] for item in cart])
            context = {'cart': [{'product': product, 'quantity': next(item['quantity'] for item in cart if item['product_id'] == product.pk)} for product in products]}
        return render(request, 'cart.html', context)
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
            context = {'cart':  [{'product': product, 'quantity': next(item['quantity'] for item in cart if item['product_id'] == product.pk), 'total': product.price * next(item['quantity'] for item in cart if item['product_id'] == product.pk)} for product in products], 'user_cart': {'total_price': sum(product.price * next(item['quantity'] for item in cart if item['product_id'] == product.pk) for product in products)}}
        return render(request, 'cart.html', context)

def checkout(request):
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.get(user=user)
        order = Order.objects.create(user=user, cart=cart)
        # Redirect to the order confirmation page
        return render(request, 'orderconfirm.html', {"order_number": order.order_number})
    else:
        user = MyUser.objects.get(id=request.user.id)
        context = {
            'user': user
        }
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

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # get the quantity from the form data or default to 1
        # add the product to the cart with the given quantity or update the existing quantity if it already exists
        a_cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            a_cart_item.quantity += quantity
        else:
            a_cart_item.quantity = quantity
        a_cart_item.save()
    else:
        # Handle anonymous user
        cart = request.session.get('cart', [])
        # check if the product is already in the cart
        cart_item = next((item for item in cart if item['product_id'] == product_id), None)
        if cart_item:
            # update the quantity if the product is already in the cart
            cart_item['quantity'] += quantity
        else:
            # add a new cart item if the product is not in the cart
            cart.append({'product_id': product_id, 'quantity': quantity})
        request.session['cart'] = cart
    return redirect('cart')
