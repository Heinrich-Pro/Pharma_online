# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),

    # Administration des commandes
    path('admin/', views.admin_orders, name='admin_orders'),
    path('admin/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
]