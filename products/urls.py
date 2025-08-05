# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('medicine/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    path('add-to-cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('category/<int:category_id>/', views.medicine_list, name='medicine_by_category'),
]
