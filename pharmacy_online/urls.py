"""
URL configuration for pharmacy_online project.

The `urlpatterns` list routes URLs to views. For more information please see:
<<<<<<< HEAD
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
=======
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
>>>>>>> develop
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
<<<<<<< HEAD
=======

# pharmacy_online/urls.py (URLs principales)
# Configuration des routes principales du projet
# Ce fichier définit la structure générale de navigation de l'application

>>>>>>> develop
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
<<<<<<< HEAD

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('inventory/', include('inventory.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
=======
from products.views import home

# ===== CONFIGURATION DES PATTERNS D'URLS PRINCIPAUX =====

urlpatterns = [
    # Route d'administration Django (interface de gestion)
    path('admin/', admin.site.urls),
    
    # Route d'accueil principale : affiche la page d'accueil avec les produits en vedette
    path('', home, name='home'),
    
    # ===== INCLUSION DES URLS DES APPLICATIONS =====
    
    # Application products : gestion des médicaments et catégories
    # Toutes les URLs commençant par /products/ sont gérées par products.urls
    path('products/', include('products.urls')),
    
    # Application orders : gestion des commandes et panier
    # Toutes les URLs commençant par /orders/ sont gérées par orders.urls
    path('orders/', include('orders.urls')),
    
    # Application accounts : gestion des comptes utilisateurs
    # Toutes les URLs commençant par /accounts/ sont gérées par accounts.urls
    path('accounts/', include('accounts.urls')),
    
    # Application inventory : gestion des stocks et inventaires
    # Toutes les URLs commençant par /inventory/ sont gérées par inventory.urls
    path('inventory/', include('inventory.urls')),
    
    # URLs d'authentification Django par défaut
    # Inclut login/, logout/, password_change/, etc.
    path('auth/', include('django.contrib.auth.urls')),
]

# ===== CONFIGURATION DES FICHIERS MÉDIA (DÉVELOPPEMENT) =====

# Servir les fichiers media en développement uniquement
# En production, ces fichiers doivent être servis par le serveur web (nginx, etc.)
if settings.DEBUG:
    # Ajoute les routes pour servir les fichiers uploadés (images, etc.)
    # MEDIA_URL : URL de base pour accéder aux fichiers media
    # MEDIA_ROOT : répertoire physique où sont stockés les fichiers
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> develop
