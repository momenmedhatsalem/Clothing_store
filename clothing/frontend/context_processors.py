from .models import Cart





def base_url(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)
    else:
        cart = Cart.objects.get_anonymous_cart(request.session)
    return {'user_cart': Cart}