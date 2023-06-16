from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path("logout", views.logout_view, name="logout"),
    path('register',  views.register_view, name='register'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('product/<int:id>', views.product, name='product'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('toggle-night-mode/', views.toggle_night_mode, name='toggle_night_mode'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)