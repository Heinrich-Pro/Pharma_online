<<<<<<< HEAD
from django.shortcuts import render
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')

    if category_id:
        products = products.filter(category_id=category_id)
    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
    })
=======
# products/views.py
# Vues pour la gestion des produits pharmaceutiques
# Gère l'affichage des médicaments, la recherche, le filtrage et l'ajout au panier

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Medicine, Category
from orders.models import Cart, CartItem


def home(request):
    """
    Vue d'accueil principale du site
    
    Affiche :
    - Les médicaments en vedette (disponibles et en stock)
    - Les catégories principales
    - Une interface d'accueil attrayante
    
    Args:
        request: Objet HttpRequest
        
    Returns:
        HttpResponse: Rendu du template d'accueil avec le contexte
    """
    
    # Récupération des médicaments en vedette (limités à 8)
    featured_medicines = Medicine.objects.filter(
        is_available=True,
        stock_quantity__gt=0
    ).order_by('-created_at')[:8]  # Les plus récents en premier
    
    # Récupération des catégories principales (limitées à 6)
    categories = Category.objects.all()[:6]
    
    # Préparation du contexte
    context = {
        'featured_medicines': featured_medicines,
        'categories': categories,
    }
    
    return render(request, 'home.html', context)


def medicine_list(request):
    """
    Vue principale pour afficher la liste des médicaments disponibles
    
    Cette vue implémente :
    1. Affichage de tous les médicaments en stock
    2. Filtrage par catégorie
    3. Recherche textuelle multi-champs
    4. Pagination des résultats
    5. Affichage des catégories pour la navigation
    
    Args:
        request: Objet HttpRequest contenant les paramètres de la requête
        
    Returns:
        HttpResponse: Rendu du template avec le contexte des médicaments
    """
    
    # ===== RÉCUPÉRATION DES DONNÉES DE BASE =====
    
    # Récupération des médicaments disponibles et en stock
    medicines = Medicine.objects.filter(
        is_available=True,           # Seulement les médicaments disponibles
        stock_quantity__gt=0        # Seulement ceux avec du stock
    )
    
    # Récupération de toutes les catégories pour le menu de filtrage
    categories = Category.objects.all()

    # ===== FILTRAGE PAR CATÉGORIE =====
    
    # Récupération du paramètre de catégorie depuis l'URL
    category_id = request.GET.get('category')
    if category_id:
        # Application du filtre par catégorie
        medicines = medicines.filter(category_id=category_id)

    # ===== RECHERCHE TEXTUELLE =====
    
    # Récupération du terme de recherche depuis l'URL
    search_query = request.GET.get('search')
    if search_query:
        # Recherche dans plusieurs champs avec Q objects (requêtes complexes)
        medicines = medicines.filter(
            Q(name__icontains=search_query) |                    # Nom du médicament
            Q(active_ingredient__icontains=search_query) |       # Principe actif
            Q(description__icontains=search_query)               # Description
        )
        # icontains : recherche insensible à la casse

    # ===== PAGINATION =====
    
    # Configuration de la pagination : 12 médicaments par page
    paginator = Paginator(medicines, 12)
    
    # Récupération du numéro de page depuis l'URL
    page_number = request.GET.get('page')
    
    # Récupération de la page demandée
    medicines = paginator.get_page(page_number)

    # ===== PRÉPARATION DU CONTEXTE =====
    
    context = {
        'medicines': medicines,              # Médicaments de la page courante
        'categories': categories,            # Toutes les catégories
        'search_query': search_query,        # Terme de recherche pour pré-remplir le formulaire
        'selected_category': category_id,    # Catégorie sélectionnée pour le menu
    }
    
    return render(request, 'products/medicine_list.html', context)


def medicine_detail(request, pk):
    """
    Vue pour afficher les détails d'un médicament spécifique
    
    Args:
        request: Objet HttpRequest
        pk: Identifiant unique du médicament (Primary Key)
        
    Returns:
        HttpResponse: Rendu du template avec les détails du médicament
        
    Raises:
        404: Si le médicament n'existe pas ou n'est pas disponible
    """
    
    # Récupération du médicament ou erreur 404 si inexistant
    # Vérifie aussi que le médicament est disponible
    medicine = get_object_or_404(Medicine, pk=pk, is_available=True)
    
    # Rendu du template avec le médicament
    return render(request, 'products/medicine_detail.html', {'medicine': medicine})


@login_required
def add_to_cart(request, medicine_id):
    """
    Vue pour ajouter un médicament au panier d'achat
    
    Cette vue :
    1. Vérifie que l'utilisateur est connecté (@login_required)
    2. Vérifie la disponibilité du stock
    3. Ajoute ou met à jour la quantité dans le panier
    4. Affiche des messages de confirmation ou d'erreur
    
    Args:
        request: Objet HttpRequest (utilisateur connecté)
        medicine_id: Identifiant du médicament à ajouter
        
    Returns:
        HttpResponseRedirect: Redirection vers la page du médicament
        
    Raises:
        404: Si le médicament n'existe pas
    """
    
    # Récupération du médicament ou erreur 404
    # Vérifie aussi que le médicament est disponible
    medicine = get_object_or_404(Medicine, id=medicine_id, is_available=True)

    # ===== VÉRIFICATION DU STOCK =====
    
    # Vérification que le médicament est en stock
    if medicine.stock_quantity <= 0:
        messages.error(request, "Ce médicament n'est plus en stock.")
        return redirect('products:medicine_detail', pk=medicine_id)

    # ===== GESTION DU PANIER =====
    
    # Récupération ou création du panier de l'utilisateur
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Récupération ou création de l'article dans le panier
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        medicine=medicine,
        defaults={'quantity': 1}  # Quantité par défaut si nouvel article
    )

    if not created:
        # Article déjà dans le panier : augmentation de la quantité
        if cart_item.quantity < medicine.stock_quantity:
            # Vérification que l'augmentation est possible
            cart_item.quantity += 1
            cart_item.save()
            messages.success(request, f"{medicine.name} ajouté au panier.")
        else:
            # Stock insuffisant pour augmenter
            messages.warning(request, "Stock insuffisant pour augmenter la quantité.")
    else:
        # Nouvel article ajouté
        messages.success(request, f"{medicine.name} ajouté au panier.")

    # Redirection vers la page du médicament
    return redirect('products:medicine_detail', pk=medicine_id)
>>>>>>> develop
