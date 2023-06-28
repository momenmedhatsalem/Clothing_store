from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    Http404,
    HttpResponseBadRequest,
)
from django.shortcuts import render
from django.urls import reverse
from frontend.models import Product, ProductImage, ProductSize, MyUser, Cart, CartItem, Order, PromoCode, Address, OrderItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms
from django.contrib import messages

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


from django.core.mail import send_mail

import base64
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Design
from django.core.paginator import Paginator



def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message') 
        message = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        subject = 'Contact Form'
        from_email = 'vosmos.net@gmail.com'
        recipient_list = ['vosmos.net@gmail.com']
        
        send_mail(subject, message, from_email, recipient_list)
        # Send confirmation email to user
        subject = 'Thanks for contacting us'
        message = f'Dear {name},\n\nThank you for contacting us. We have received your inquiry and will get back to you as soon as possible.\n\nBest regards,\nVosMos Team'
        from_email = 'vosmos.net@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')
    else:
        
        return render(request, 'contact.html')

def Return(request):
    return render(request, 'Return.html')
def show_products(request, category=None, subcategory=None):
    products = Product.objects.all()
    if category:
        products = products.filter(category=category)
    if subcategory:
        products = products.filter(subcategory=subcategory)

    paginator = Paginator(products, 15) # Show 15 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj, 'categories': Product.CATEGORY_CHOICES,}
    return render(request, 'products.html', context)


@csrf_exempt
def design_save(request):
    if request.method == 'POST':
        # Get the image data from the request body
        data = json.loads(request.body)
        image_data = data.get('image')
        product_id = data.get('product_id')
        # Decode the image data and create a new Image object
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        product = Product.objects.get(id=product_id)
        image = Design.objects.create(image=data, user=request.user, product=product )
        image.save()
        # Return a JSON response
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})

def send_order_confirmation_email(first_name, email, order):
    subject = 'Order Confirmation'
    message = f'Thank you for your order, {first_name}! Your order number is {order.id}.'
    from_email = 'your_email@example.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def index(request):
    # Get the list of recently viewed product IDs from the session
    recently_viewed_product_ids = request.session.get('recently_viewed_products', [])

    # Get the Product objects for the recently viewed products
    recently_viewed_products = Product.objects.filter(id__in=recently_viewed_product_ids)

    # Get all products
    products = Product.objects.all()

    # Render the template with the products and recently viewed products
    return render(request, 'index.html', {
        'products': products,
        'recently_viewed_products': recently_viewed_products,
    })


def product_detail(request, product_id):
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
    # Get the product
    else:
        product = get_object_or_404(Product, id=product_id)

        # Add the product ID to the list of recently viewed products in the session
        recently_viewed_product_ids = request.session.get('recently_viewed_products', [])
        if product_id not in recently_viewed_product_ids:
            recently_viewed_product_ids.append(product_id)
            request.session['recently_viewed_products'] = recently_viewed_product_ids
        images = ProductImage.objects.filter(product=product)
        sizes = ProductSize.objects.filter(product=product)
    

    # Render the template with the product
    return render(request, 'product_detail.html', {'product': product, 'images': images, 'sizes': sizes})


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:

            # User has successfully logged in
            # Retrieve session cart
            session_cart = request.session.get('cart', [])
            # Get or create user's Cart object
            cart, created = Cart.objects.get_or_create(user=user)
            # Iterate over session cart items
            for item in session_cart:
                product_id = item['product_id']
                quantity = item['quantity']
                product = Product.objects.get(pk=product_id)
                # Check if CartItem already exists for given product and cart
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if created:
                    # CartItem did not exist, set its quantity
                    cart_item.quantity = int(quantity)
                    cart_item.save()
                else:
                    # CartItem already exists, check if it has been customized
                    if not cart_item.customized:
                        # Increase its quantity
                        cart_item.quantity += int(quantity)
                        cart_item.save()
            # Clear session cart
            request.session['cart'] = []
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
        if user is not None:
            # User has successfully logged in
            # Retrieve session cart
            session_cart = request.session.get('cart', [])
            # Get or create user's Cart object
            cart, created = Cart.objects.get_or_create(user=user)
            # Iterate over session cart items
            for item in session_cart:
                product_id = item['product_id']
                quantity = item['quantity']
                product = Product.objects.get(pk=product_id)
                # Check if CartItem already exists for given product and cart
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if created:
                    # CartItem did not exist, set its quantity
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    # CartItem already exists, check if it has been customized
                    if not cart_item.customized:
                        # Increase its quantity
                        cart_item.quantity += quantity
                        cart_item.save()
            # Clear session cart
            request.session['cart'] = []
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
        # Get the form data
        email = request.POST['email']
        payment_method = request.POST['payment_method']
        address_id = request.POST.get('address')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        if payment_method == "COD":
            fees = 12
        else:
            fees = 0
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Get the user and cart information
            user = request.user
            cart = Cart.objects.get(user=user, ordered=False)

            # Create a new Order instance for the authenticated user
            order = Order.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                coupon = cart.coupon,
                address=request.POST['address'],
                city=request.POST['city'],
                payment_method=payment_method,
                shipping_cost=cart.shipping_cost,
                final_price=cart.final_price + fees  # Set the final price of the order to the final price of the cart
            )

            # Create OrderItem instances for each item in the cart
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    price=item.product.price,
                    quantity=item.quantity,
                    customized=item.customized,
                )

            # Save the order
            order.save()

            # Clear the cart for authenticated users
            cart.items.all().delete()
            cart.coupon = None
            cart.save()
        else:
            # Get or create a cart for the guest user using the CartManager model
            cart = Cart.objects.get_anonymous_cart(request.session)

            # Create a new Order instance for the anonymous user without setting the user field
            order = Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                address=request.POST['address'],
                phone=phone,
                city=request.POST['city'],
                
                payment_method=payment_method,
                shipping_cost=cart['shipping_cost'],
                final_price=cart['final_price'] + fees # Set the final price of the order to the final price of the anonymous cart
            )

            # Create OrderItem instances for each item in the anonymous cart
            for item in cart['cart_items']:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity'],
                    
                    # customized=item['customized']
                )

            # Save the order
            order.save()

            # Clear the cart for anonymous users
            request.session['cart'] = []

        # Redirect to the order confirmation page
        send_order_confirmation_email(first_name, email, order)
        return render(request, 'orderconfirm.html', {"order_number": order.order_number})
    else:
        if request.user.is_authenticated:
            # Handle authenticated user
            cart = Cart.objects.get(user=request.user)
            CartItems = CartItem.objects.filter(cart=cart)
            if float(cart.total_price) > 1000:
                cart.shipping_cost = 0
                cart.save()
            context = {'cart': CartItems, 'user_cart': cart}
        else:
            # Handle anonymous user
            anonymous_cart = Cart.objects.get_anonymous_cart(request.session)
            
            context = {'cart': anonymous_cart['cart_items'], 'user_cart': anonymous_cart}
    
        return render(request, 'checkout.html', context)
        

    




#@require_http_methods(["POST", "PUT"])
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'GET' or request.method == 'POST':
        quantity = int(request.POST.get('cloth_quantity', 1))
        color = request.POST.get('color')
        size = request.POST.get('size')
        
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            a_cart_item, created = CartItem.objects.get_or_create(cart=cart,
                                                                product=product, color=color,
                                                                    size=size)

            if not created:
                a_cart_item.quantity += quantity
            else:
                a_cart_item.quantity = quantity
            a_cart_item.save()
            
        else:
            # Handle anonymous user
            cart = request.session.get('cart', [])
            cart_item = next((item for item in cart if item['product_id'] == product_id and item['color'] == color and item['size'] == size), None)
            if cart_item:
                cart_item['quantity'] += quantity
                print("found")
            else:
                print("Not")
                cart.append({'product_id': product_id, 'quantity': quantity, 'color': color, 'size': size})
            request.session['cart'] = cart
        return redirect('cart')
    elif request.method == 'PUT':
        data = json.loads(request.body)
        quantity = data.get('quantity', 1)
        Product_detail = ProductSize.objects.filter(product=product)
        color = Product_detail[0].color
        size = Product_detail[0].size


        print(color)
        print(size)
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            a_cart_item, created = CartItem.objects.get_or_create(cart=cart,
                                                                product=product, color=color,
                                                                    size=size)

            if created:
                # if the cart item was created (i.e. the product was not already in the cart), set the quantity to 1
                a_cart_item.quantity = 1
            else:
                if quantity == 0:
                    a_cart_item.quantity += 1
                # if the cart item was not created (i.e. the product was already in the cart), update the quantity
                else:
                    a_cart_item.quantity = quantity
            a_cart_item.save()
            total = a_cart_item.total
            total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount
        else:
            # Handle anonymous user

            product = Product.objects.get(pk=product_id)
            cart = request.session.get('cart', [])
            cart_item = next((item for item in cart if item['product_id'] == product_id and item['color'] == color and item['size'] == size), None)

            if cart_item:
                if quantity == 0:
                    cart_item['quantity'] += 1
                # if the product is already in the cart, update the quantity
                else:
                    cart_item['quantity'] = quantity
            else:
                # if the product is not in the cart, add it with a quantity of 1
                cart.append({'product_id': product_id, 'quantity': 1, 'color': color, 'size': size})

            request.session['cart'] = cart
            total = product.price * int(quantity)

            anonymous_cart = Cart.objects.get_anonymous_cart(request.session)
            total_price = anonymous_cart['total_price']
            total_price_before_discount = anonymous_cart['total_price_before_discount']
        # calculate discount
        discount = float(total_price_before_discount) - float(total_price)
        return JsonResponse({'success': True,'cart_total': total_price, 'total': "{:.2f}".format(total),
                              'discount': "{:.2f}".format(discount), 'cart_total_before_discount': total_price_before_discount, 'product_name': product.product_name})


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
            total_price_before_discount = cart.total_price_before_discount
            discount = float(total_price_before_discount) - float(cart_total_price)
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
            total_price_before_discount = anonymous_cart['total_price_before_discount']
            discount = float(total_price_before_discount) - float(cart_total_price)
        return JsonResponse({'cart_total': cart_total_price,'discount': "{:.2f}".format(discount), 'cart_total_before_discount': total_price_before_discount})
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
            if cart.applied_coupons.filter(code=promo_code).exists():
                return JsonResponse({'error': 'You have already applied this code before'}, status=400)
            if cart.coupon and cart.coupon.code == promo_code:
                return JsonResponse({'error': 'Code already applied'}, status=400)
            
            # remove old coupon if applied
            if cart.coupon:
                cart.coupon = None
            
            # apply the new promo code
            cart.coupon = promo
            cart.applied_coupons.add(promo)
            cart.save()
            
            # recalculate cart total with discount applied
            total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount

        
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
            cart.applied_coupons.remove(cart.coupon)

            cart.coupon = None

            cart.save()
            
            # recalculate cart total with discount removed
            total_price = cart.total_price
            total_price_before_discount = cart.total_price_before_discount
    
    return JsonResponse({'error': False, 'cart_total': total_price})


def orders(request):
    if request.GET.get('order_number'):
        # User is looking up an order using an order number
        order_number = request.GET.get('order_number')
        try:
            # Try to get the order with the given order number
            order = Order.objects.get(order_number=order_number)
            # Return the order details page
            # Calculate the width of each progress bar segment
            segment_width = 100 / order.items.count()
            return render(request, 'order.html', {'order': order, 'segment_width': segment_width})
        except Order.DoesNotExist:
            # Order with the given order number does not exist
            # Display an error message
            messages.error(request, 'Order not found.')
    # User is viewing their order history
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order.html', {'orders': orders})



def customize(request):
    return render(request, 'customize.html')


@csrf_exempt
@require_http_methods(["PUT"])
def add_to_favorites(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    product = Product.objects.get(pk=product_id)
    if request.user.is_authenticated:
        # Add the product to the authenticated user's favorites
        profile = MyUser.objects.get(email =request.user.email)
        profile.favorites.add(product)
    else:
        # Add the product to the anonymous user's session-based favorites
        favorites = request.session.get('favorites', [])
        favorites.append(product_id)
        request.session['favorites'] = favorites
    return JsonResponse({'status': 'success'})


@require_http_methods(["PUT"])
def remove_from_favorites(request):
    data = json.loads(request.body)
    product_id = data.get('product_id')
    if request.user.is_authenticated:
        # Remove the product from the authenticated user's favorites
        profile = MyUser.objects.get(email =request.user.email)
        profile.favorites.remove(product_id)
    else:
        # Remove the product from the anonymous user's session-based favorites
        favorites = request.session.get('favorites', [])
        if product_id in favorites:
            favorites.remove(product_id)
            request.session['favorites'] = favorites
    return JsonResponse({'status': 'success'})

def favorites(request):
    if request.user.is_authenticated:
        # Get the favorite products for the authenticated user
        profile = MyUser.objects.get(email =request.user.email)
        
        favorite_products = profile.favorites.all()
    else:
        # Get the favorite products for the anonymous user
        favorite_product_ids = request.session.get('favorites', [])
        favorite_products = Product.objects.filter(pk__in=favorite_product_ids)

    context = {'favorites': favorite_products}
    return render(request, 'favorites.html', context)