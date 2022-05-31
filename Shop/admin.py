from django.contrib import admin
from .models import Product, OrderItem, Order, Adress, Message

# Register your models here.

admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Adress)
admin.site.register(Message)
