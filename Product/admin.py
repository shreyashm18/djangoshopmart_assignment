from django.contrib import admin
from .models import Category, Products, Tags, Cart, Cartitems
# Register your models here.

admin.site.register(Category)
admin.site.register(Tags)
admin.site.register(Products)
admin.site.register(Cart)
admin.site.register(Cartitems)