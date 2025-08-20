<<<<<<< HEAD
from django.contrib import admin
from .models import Order, OrderItem
=======
# orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

>>>>>>> develop

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
<<<<<<< HEAD

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username',)
    inlines = [OrderItemInline]
=======
    readonly_fields = ['medicine', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

    fieldsets = (
        ('Informations de commande', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Détails', {
            'fields': ('notes', 'pickup_date')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'item_count', 'total_amount', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
>>>>>>> develop
