from django.contrib import admin

from core.models import Order, OrderItem, Product, User


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
