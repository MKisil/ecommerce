from django.contrib import admin

from order.models import PaymentMethod, ShippingMethod, Address, PersonalDetails, Order, OrderItem

admin.site.register(PaymentMethod)
admin.site.register(ShippingMethod)
admin.site.register(Order)