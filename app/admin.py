from django.contrib import admin
from .models import Customer,Cart,OrderPlaced,Product,Payment
from django.urls import reverse
from django.utils.html import format_html
# Register your models here.

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','name','locality','city','zipcode','state']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_id' , 'customer_name', 'product', 'quantity', 'order_date', 'status']
    def payment_id(self, obj):
        link=reverse("admin:app_payment_change", args=[obj.payment.id]) #model name has to be lowercase
        return format_html('<a href="{link}">{name}</a>' ,link=link,name=obj.payment.razorpay_payment_id)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image']

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['user','razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature_id', 'paid']
