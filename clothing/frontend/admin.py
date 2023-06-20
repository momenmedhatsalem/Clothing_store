from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from frontend.models import Product, MyUser,PromoCode, Cart
# Register your models here.
admin.site.register(Product)

admin.site.register(MyUser)
admin.site.register(PromoCode)
admin.site.register(Cart)
