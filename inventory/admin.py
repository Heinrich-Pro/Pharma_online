<<<<<<< HEAD
from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'low_stock_threshold')
    search_fields = ('product__name',)
=======
# inventory/admin.py
from django.contrib import admin
from .models import StockMovement

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'movement_type', 'quantity', 'reason', 'created_by', 'created_at']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['medicine__name', 'reason']
    readonly_fields = ['created_at']
>>>>>>> develop
