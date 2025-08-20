<<<<<<< HEAD
from django.db import models
from accounts.models import CustomUser
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'En attente'),
        ('confirmed', 'Confirmée'),
        ('delivered', 'Livrée'),
    ], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Commande {self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total(self):
        return self.quantity * self.price
=======
# orders/models.py
# Modèles de données pour la gestion des commandes et du panier
# Définit la structure des commandes, articles et panier d'achat

from django.db import models
from django.contrib.auth.models import User
from products.models import Medicine
import uuid


class Order(models.Model):
    """
    Modèle principal pour les commandes de médicaments
    
    Représente une commande complète d'un utilisateur avec son statut
    et son suivi tout au long du processus de traitement
    """
    
    # ===== CHOIX DE STATUTS =====
    
    # Définition des statuts possibles pour une commande
    STATUS_CHOICES = [
        ('pending', 'En attente'),           # Commande créée, en attente de confirmation
        ('confirmed', 'Confirmée'),          # Commande validée par le personnel
        ('ready', 'Prête à récupérer'),      # Médicaments préparés et disponibles
        ('completed', 'Terminée'),           # Commande récupérée par le client
        ('cancelled', 'Annulée'),            # Commande annulée (client ou personnel)
    ]

    # ===== INFORMATIONS DE BASE =====
    
    # Numéro unique de commande généré automatiquement
    # Format: PH + 8 caractères hexadécimaux (ex: PH1A2B3C4D)
    order_number = models.CharField(max_length=100, unique=True, editable=False)
    
    # Utilisateur qui a passé la commande
    # Relation many-to-one : un utilisateur peut avoir plusieurs commandes
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,           # Supprime la commande si l'utilisateur est supprimé
        related_name='orders'               # Nom de la relation inverse (user.orders.all())
    )
    
    # Statut actuel de la commande
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,            # Limite les valeurs possibles
        default='pending'                   # Statut par défaut à la création
    )
    
    # Montant total de la commande en euros
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Notes additionnelles (ex: instructions spéciales, allergies)
    notes = models.TextField(blank=True, null=True)
    
    # ===== TIMESTAMPS =====
    
    # Date et heure de création de la commande
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Date et heure de dernière modification
    updated_at = models.DateTimeField(auto_now=True)
    
    # Date et heure de retrait prévue ou effective
    pickup_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        # Tri par défaut : commandes les plus récentes en premier
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        """
        Surcharge de la méthode save pour générer automatiquement le numéro de commande
        
        Génère un numéro unique si la commande est nouvelle (pas encore de numéro)
        """
        if not self.order_number:
            # Génération d'un numéro unique : PH + 8 caractères hexadécimaux
            self.order_number = f"PH{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        """Représentation textuelle de la commande"""
        return f"Commande {self.order_number}"

    def get_absolute_url(self):
        """
        Retourne l'URL pour afficher les détails de cette commande
        
        Utilisé par Django pour les redirections et les liens automatiques
        """
        return reverse('orders:order_detail', kwargs={'pk': self.pk})


class OrderItem(models.Model):
    """
    Modèle pour les articles individuels d'une commande
    
    Représente un médicament spécifique avec sa quantité et son prix
    dans le contexte d'une commande particulière
    """
    
    # Commande à laquelle appartient cet article
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE,           # Supprime l'article si la commande est supprimée
        related_name='items'                # Nom de la relation inverse (order.items.all())
    )
    
    # Médicament commandé
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    
    # Quantité commandée (minimum 1)
    quantity = models.PositiveIntegerField(default=1)
    
    # Prix unitaire au moment de la commande (peut différer du prix actuel)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        """Représentation textuelle de l'article de commande"""
        return f"{self.quantity}x {self.medicine.name}"

    @property
    def total_price(self):
        """
        Calcule le prix total pour cet article (quantité × prix unitaire)
        
        Returns:
            Decimal: Prix total de l'article
        """
        return self.quantity * self.price


class Cart(models.Model):
    """
    Modèle pour le panier d'achat d'un utilisateur
    
    Chaque utilisateur a un seul panier qui contient ses articles
    avant la finalisation de la commande
    """
    
    # Utilisateur propriétaire du panier
    # Relation one-to-one : un utilisateur = un panier
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE           # Supprime le panier si l'utilisateur est supprimé
    )
    
    # ===== TIMESTAMPS =====
    
    # Date et heure de création du panier
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Date et heure de dernière modification
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Représentation textuelle du panier"""
        return f"Panier de {self.user.username}"

    # ===== PROPRIÉTÉS CALCULÉES =====
    
    @property
    def total_amount(self):
        """
        Calcule le montant total du panier
        
        Returns:
            Decimal: Montant total de tous les articles du panier
        """
        return sum(item.total_price for item in self.items.all())

    @property
    def item_count(self):
        """
        Calcule le nombre total d'articles dans le panier
        
        Returns:
            int: Nombre total d'articles (somme des quantités)
        """
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """
    Modèle pour les articles individuels du panier
    
    Représente un médicament avec sa quantité dans le panier d'achat
    """
    
    # Panier auquel appartient cet article
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE,          # Supprime l'article si le panier est supprimé
        related_name='items'               # Nom de la relation inverse (cart.items.all())
    )
    
    # Médicament ajouté au panier
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    
    # Quantité dans le panier (minimum 1)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # Contrainte d'unicité : un médicament ne peut apparaître qu'une fois par panier
        # La quantité est modifiée si on ajoute le même médicament
        unique_together = ['cart', 'medicine']

    def __str__(self):
        """Représentation textuelle de l'article du panier"""
        return f"{self.quantity}x {self.medicine.name}"

    @property
    def total_price(self):
        """
        Calcule le prix total pour cet article du panier
        
        Returns:
            Decimal: Prix total de l'article (quantité × prix unitaire)
        """
        return self.quantity * self.medicine.price
>>>>>>> develop
