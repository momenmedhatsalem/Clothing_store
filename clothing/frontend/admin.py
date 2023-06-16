from django.contrib import admin
from django.db import models
from django.contrib.auth.admin import UserAdmin
from frontend.models import Product, MyUser
# Register your models here.
admin.site.register(Product)

admin.site.register(MyUser)
