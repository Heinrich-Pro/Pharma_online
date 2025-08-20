# accounts/urls.py
# Configuration des URLs pour l'application de gestion des comptes utilisateurs
# Cette application gère l'inscription, la connexion et les profils des utilisateurs

from django.urls import path
from . import views

# Définition du namespace de l'application pour éviter les conflits d'URLs
app_name = 'accounts'

# Configuration des patterns d'URLs pour l'application accounts
urlpatterns = [
    # Route pour l'inscription d'un nouvel utilisateur
    path('register/', views.register, name='register'),
    # Route pour afficher et modifier le profil utilisateur (nécessite une connexion)
    path('profile/', views.profile, name='profile'),
]