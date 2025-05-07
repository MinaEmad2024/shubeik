from django.contrib import admin
from .models import shippingAddress, Order, OrderItem
from django.contrib.auth.models import User 


# Register your models here.
admin.site.register(shippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# create order inline 
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


#Extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]
    readonly_fields = ["date_ordered"]
    #fields = ["user", "full_name", "email"]

# Unregister Order Model
admin.site.unregister(Order)


# Re-Register our Order AND OrderAdmin
admin.site.register(Order, OrderAdmin)