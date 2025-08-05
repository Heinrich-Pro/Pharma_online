# inventory/urls.py
from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_dashboard, name='dashboard'),
    path('stock-movements/', views.stock_movements, name='stock_movements'),
    path('low-stock/', views.low_stock_report, name='low_stock_report'),
    path('update-stock/<int:medicine_id>/', views.update_stock_view, name='update_stock'),
]