<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/confirm/', views.confirm_order, name='confirm_order'),
    path('order/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
=======
# orders/urls.py
# Configuration des URLs pour l'application de gestion des commandes
# Cette application gère le panier, le checkout et l'administration des commandes

from django.urls import path
from . import views

# Définition du namespace de l'application pour éviter les conflits d'URLs
app_name = 'orders'

# Configuration des patterns d'URLs pour l'application orders
urlpatterns = [
    # Route pour afficher le contenu du panier de l'utilisateur
    path('cart/', views.cart_view, name='cart'),
    
    # Route pour modifier les quantités ou supprimer des articles du panier
    # <int:item_id> capture l'ID de l'article à modifier
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    
    # Route pour finaliser la commande (checkout)
    path('checkout/', views.checkout, name='checkout'),
    
    # Route principale : liste de toutes les commandes de l'utilisateur
    path('', views.order_list, name='order_list'),
    
    # Route pour afficher les détails d'une commande spécifique
    # <int:pk> capture l'ID de la commande
    path('<int:pk>/', views.order_detail, name='order_detail'),
    
    # Route pour générer et télécharger la facture PDF d'une commande
    # <int:order_id> capture l'ID de la commande pour la facture
    path('invoice/<int:order_id>/', views.generate_invoice, name='generate_invoice'),

    # ===== ROUTES D'ADMINISTRATION (réservées au personnel) =====
    
    # Route pour la gestion administrative de toutes les commandes
    path('admin/', views.admin_orders, name='admin_orders'),
    
    # Route pour modifier le statut d'une commande (ex: confirmer, préparer, etc.)
    # <int:order_id> capture l'ID de la commande à modifier
    path('admin/update/<int:order_id>/', views.update_order_status, name='update_order_status'),
>>>>>>> develop
]