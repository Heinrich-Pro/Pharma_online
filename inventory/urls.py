from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.manage_inventory, name='manage_inventory'),
]