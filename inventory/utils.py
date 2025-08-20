# inventory/utils.py
# Fonctions utilitaires pour la gestion des stocks et inventaires
# Contient la logique métier pour les mouvements de stock et les rapports

from .models import StockMovement
from products.models import Medicine


def update_stock(medicine, quantity, movement_type, reason, user):
    """
    Met à jour le stock d'un médicament et enregistre le mouvement
    
    Cette fonction est le cœur de la gestion des stocks. Elle :
    1. Modifie la quantité en stock selon le type de mouvement
    2. Enregistre automatiquement le mouvement dans l'historique
    3. Assure la traçabilité complète des modifications
    
    Args:
        medicine (Medicine): L'objet médicament à modifier
        quantity (int): La quantité à ajouter/soustraire/ajuster
        movement_type (str): Type de mouvement ('in', 'out', 'adjustment')
        reason (str): Motif de la modification (ex: "Commande client", "Livraison fournisseur")
        user (User): Utilisateur effectuant la modification
    
    Returns:
        Medicine: Le médicament modifié avec le nouveau stock
    
    Types de mouvements :
    - 'in' : Entrée de stock (ajoute la quantité)
    - 'out' : Sortie de stock (soustrait la quantité, minimum 0)
    - 'adjustment' : Ajustement direct (remplace la quantité)
    """
    # Sauvegarde de l'ancienne quantité pour le calcul des différences
    old_quantity = medicine.stock_quantity

    # Application de la modification selon le type de mouvement
    if movement_type == 'in':
        # Entrée de stock : ajout de la quantité
        medicine.stock_quantity += quantity
    elif movement_type == 'out':
        # Sortie de stock : soustraction avec protection contre les stocks négatifs
        medicine.stock_quantity = max(0, medicine.stock_quantity - quantity)
    elif movement_type == 'adjustment':
        # Ajustement direct : remplacement de la quantité
        medicine.stock_quantity = quantity

    # Sauvegarde des modifications en base de données
    medicine.save()

    # Enregistrement du mouvement de stock pour la traçabilité
    # Pour les ajustements, on calcule la différence avec l'ancienne quantité
    movement_quantity = quantity if movement_type != 'adjustment' else quantity - old_quantity
    
    StockMovement.objects.create(
        medicine=medicine,
        movement_type=movement_type,
        quantity=movement_quantity,
        reason=reason,
        created_by=user
    )

    return medicine


def get_low_stock_medicines():
    """
    Retourne les médicaments avec un stock faible
    
    Un médicament est considéré en stock faible quand :
    stock_quantity <= minimum_stock (seuil défini dans le modèle)
    
    Returns:
        QuerySet: Liste des médicaments en stock faible
        
    Utilisation typique :
    - Génération de rapports d'alerte
    - Notifications au personnel
    - Planification des commandes fournisseurs
    """
    return Medicine.objects.filter(stock_quantity__lte=models.F('minimum_stock'))


def get_out_of_stock_medicines():
    """
    Retourne les médicaments en rupture de stock
    
    Un médicament est en rupture quand stock_quantity = 0
    
    Returns:
        QuerySet: Liste des médicaments en rupture de stock
        
    Utilisation typique :
    - Affichage des produits indisponibles
    - Rapports de gestion
    - Alertes urgentes pour le personnel
    """
    return Medicine.objects.filter(stock_quantity=0)