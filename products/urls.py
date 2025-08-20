# products/urls.py
# Configuration des URLs pour l'application de gestion des produits
# Cette application gère l'affichage des médicaments, catégories et l'ajout au panier

from django.urls import path
from . import views

# Définition du namespace de l'application pour éviter les conflits d'URLs
app_name = 'products'

# Configuration des patterns d'URLs pour l'application products
urlpatterns = [
    # Route principale : liste de tous les médicaments disponibles
    path('', views.medicine_list, name='medicine_list'),
    
    # Route pour afficher les détails d'un médicament spécifique
    # <int:pk> capture l'ID numérique du médicament
    path('medicine/<int:pk>/', views.medicine_detail, name='medicine_detail'),
    
    # Route pour ajouter un médicament au panier
    # <int:medicine_id> capture l'ID du médicament à ajouter
    path('add-to-cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    
    # Route pour filtrer les médicaments par catégorie
    # <int:category_id> capture l'ID de la catégorie sélectionnée
    path('category/<int:category_id>/', views.medicine_list, name='medicine_by_category'),
]
