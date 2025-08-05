# inventory/utils.py
from .models import StockMovement
from products.models import Medicine


def update_stock(medicine, quantity, movement_type, reason, user):
    """
    Met à jour le stock d'un médicament et enregistre le mouvement
    """
    old_quantity = medicine.stock_quantity

    if movement_type == 'in':
        medicine.stock_quantity += quantity
    elif movement_type == 'out':
        medicine.stock_quantity = max(0, medicine.stock_quantity - quantity)
    elif movement_type == 'adjustment':
        medicine.stock_quantity = quantity

    medicine.save()

    # Enregistrer le mouvement de stock
    StockMovement.objects.create(
        medicine=medicine,
        movement_type=movement_type,
        quantity=quantity if movement_type != 'adjustment' else quantity - old_quantity,
        reason=reason,
        created_by=user
    )

    return medicine


def get_low_stock_medicines():
    """
    Retourne les médicaments avec un stock faible
    """
    return Medicine.objects.filter(stock_quantity__lte=models.F('minimum_stock'))


def get_out_of_stock_medicines():
    """
    Retourne les médicaments en rupture de stock
    """
    return Medicine.objects.filter(stock_quantity=0)