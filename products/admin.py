# products/admin.py
from django.contrib import admin
from .models import Category, Medicine


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_available', 'expiry_date']
    list_filter = ['category', 'is_available', 'requires_prescription', 'created_at']
    search_fields = ['name', 'active_ingredient', 'manufacturer']
    list_editable = ['price', 'stock_quantity', 'is_available']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Informations générales', {
            'fields': ('name', 'description', 'category', 'image', 'is_available')
        }),
        ('Détails médicamenteux', {
            'fields': ('active_ingredient', 'dosage', 'manufacturer', 'requires_prescription')
        }),
        ('Prix et stock', {
            'fields': ('price', 'stock_quantity', 'minimum_stock', 'expiry_date')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )