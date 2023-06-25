from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from frontend.models import Product, ProductSize, MyUser, PromoCode, Cart, Order, CartItem, OrderItem, Design
from django.utils.html import format_html

# Register your models here.
admin.site.register(CartItem)
admin.site.register(MyUser)
admin.site.register(PromoCode)
admin.site.register(Cart)
admin.site.register(Design)

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline]

admin.site.register(Product, ProductAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    readonly_fields = ['product_image']

    def product_image(self, obj):
        return format_html('<img src="{}" width="150" height="150" />', obj.product.image.url)
    product_image.short_description = 'Product Image'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('order_number',)
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'city', 'paid', 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [OrderItemInline]
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Address information', {
            'fields': ('address', 'city')
        }),
        ('Payment information', {
            'fields': ('paid', 'payment_method')
        }),
        ('Order information', {
            'fields': ('final_price',)
        }),
        ('Coupon information', {
            'fields': ('coupon',)
        }),
        ('Payment and Shipping information', {
            'fields': ('shipping_cost', 'status')
        }),
 
    )