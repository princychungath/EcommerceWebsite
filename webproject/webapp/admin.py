from django.contrib import admin
from .models import Product,Cart,CartItem,OrderItems,Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description','price','quantity','image']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['user']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['product','quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','total_price','orderd_at']

@admin.register(OrderItems)
class CartItemAdmin(admin.ModelAdmin):
    list_display=['order','product','quantity']

