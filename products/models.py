# products/models.py
# Modèles de données pour la gestion des produits pharmaceutiques
# Définit la structure des catégories et médicaments dans la base de données

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """
    Modèle pour les catégories de médicaments
    
    Permet d'organiser les médicaments par type (ex: Antidouleurs, Antibiotiques, etc.)
    Chaque catégorie peut contenir plusieurs médicaments
    """
    
    # Nom de la catégorie (ex: "Antidouleurs", "Vitamines")
    name = models.CharField(max_length=100, unique=True)
    
    # Description détaillée de la catégorie (optionnel)
    description = models.TextField(blank=True, null=True)
    
    # Date et heure de création automatique
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Nom au pluriel dans l'interface d'administration
        verbose_name_plural = "Categories"
        # Tri par défaut par nom alphabétique
        ordering = ['name']

    def __str__(self):
        """Représentation textuelle de la catégorie"""
        return self.name


class Medicine(models.Model):
    """
    Modèle principal pour les médicaments
    
    Contient toutes les informations nécessaires pour la vente et la gestion
    des stocks de médicaments
    """
    
    # ===== INFORMATIONS DE BASE =====
    
    # Nom commercial du médicament
    name = models.CharField(max_length=200)
    
    # Description détaillée du médicament
    description = models.TextField()
    
    # Catégorie à laquelle appartient le médicament
    # Relation many-to-one : plusieurs médicaments peuvent appartenir à une catégorie
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE,           # Supprime le médicament si la catégorie est supprimée
        related_name='medicines'            # Nom de la relation inverse (category.medicines.all())
    )
    
    # Prix de vente en euros (10 chiffres, 2 décimales)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Image du médicament (optionnel)
    # upload_to='medicines/' : stocke les images dans le dossier media/medicines/
    image = models.ImageField(upload_to='medicines/', blank=True, null=True)
    
    # ===== INFORMATIONS MÉDICALES =====
    
    # Indique si le médicament nécessite une ordonnance
    requires_prescription = models.BooleanField(default=False)
    
    # Principe actif principal du médicament
    active_ingredient = models.CharField(max_length=200, blank=True)
    
    # Posologie recommandée (ex: "1 comprimé 3 fois par jour")
    dosage = models.CharField(max_length=100, blank=True)
    
    # Laboratoire pharmaceutique fabricant
    manufacturer = models.CharField(max_length=100, blank=True)
    
    # Date d'expiration du médicament
    expiry_date = models.DateField()
    
    # ===== GESTION DES STOCKS =====
    
    # Quantité actuellement en stock
    stock_quantity = models.PositiveIntegerField(default=0)
    
    # Seuil d'alerte pour les stocks faibles
    # Déclenche une alerte quand stock_quantity <= minimum_stock
    minimum_stock = models.PositiveIntegerField(default=10)
    
    # Indique si le médicament est disponible à la vente
    # Peut être False même si stock_quantity > 0 (ex: retrait temporaire)
    is_available = models.BooleanField(default=True)
    
    # ===== TIMESTAMPS =====
    
    # Date et heure de création du médicament en base
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Date et heure de dernière modification
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Tri par défaut par nom alphabétique
        ordering = ['name']

    def __str__(self):
        """Représentation textuelle du médicament"""
        return self.name

    def get_absolute_url(self):
        """
        Retourne l'URL pour afficher les détails de ce médicament
        
        Utilisé par Django pour les redirections et les liens automatiques
        """
        return reverse('products:medicine_detail', kwargs={'pk': self.pk})

    # ===== PROPRIÉTÉS CALCULÉES =====
    
    @property
    def is_low_stock(self):
        """
        Indique si le stock est faible (≤ seuil minimum)
        
        Returns:
            bool: True si le stock est faible, False sinon
        """
        return self.stock_quantity <= self.minimum_stock

    @property
    def is_in_stock(self):
        """
        Indique si le médicament est en stock
        
        Returns:
            bool: True si stock > 0, False sinon
        """
        return self.stock_quantity > 0