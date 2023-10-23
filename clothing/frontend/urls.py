from django.urls import path, include
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
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>', views.add_to_cart, name='add_to_cart'),
    path('create_product/', views.create_product, name='create_product'),
    path('cart/remove/<int:product_id>', views.remove_from_cart, name='remove_from_cart'),
    path('profile', views.profile, name='profile'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('change_password', views.change_password, name='change_password'),
    path('apply_coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove_coupon/', views.remove_coupon, name='remove_coupon'),
    path('orders', views.orders, name='orders'),
    path('accounts/', include('allauth.urls')),
    path('customize/', views.customize, name='customize'),
    path('design_save', views.design_save, name='design_save'),
    path('products/', views.show_products, name='show_products'),
    path('products/<str:category>/', views.show_products, name='show_products'),
    path('products/<str:category>/<str:subcategory>/', views.show_products, name='show_products'),
    path('contact', views.contact, name='contact'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites', views.favorites, name='favorites'),
    path('Return', views.Return, name='Return'),
    path('images/<int:product_id>', views.update_images, name='update_images'),
    path('create_canvas_object/', views.create_canvas_object, name='create_canvas_object'),
    path('customized/<int:product_id>/', views.customized_view, name='customized_view'),
]