from django.contrib import admin
from .models import OrderItem, Order, Profile

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Profile)