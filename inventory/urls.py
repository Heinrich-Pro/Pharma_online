<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('inventory/', views.manage_inventory, name='manage_inventory'),
=======
# inventory/urls.py
# Configuration des URLs pour l'application de gestion des stocks
# Cette application gère l'inventaire, les mouvements de stock et les rapports

from django.urls import path
from . import views

# Définition du namespace de l'application pour éviter les conflits d'URLs
app_name = 'inventory'

# Configuration des patterns d'URLs pour l'application inventory
urlpatterns = [
    # Route principale : tableau de bord de l'inventaire avec statistiques
    path('', views.inventory_dashboard, name='dashboard'),
    
    # Route pour consulter l'historique des mouvements de stock
    # Affiche tous les entrées/sorties/ajustements de stock
    path('stock-movements/', views.stock_movements, name='stock_movements'),
    
    # Route pour afficher le rapport des stocks faibles et ruptures
    # Permet d'identifier rapidement les produits nécessitant une commande
    path('low-stock/', views.low_stock_report, name='low_stock_report'),
    
    # Route pour modifier manuellement le stock d'un médicament
    # <int:medicine_id> capture l'ID du médicament à modifier
    path('update-stock/<int:medicine_id>/', views.update_stock_view, name='update_stock'),
>>>>>>> develop
]