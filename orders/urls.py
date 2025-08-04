from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/confirm/', views.confirm_order, name='confirm_order'),
    path('order/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]