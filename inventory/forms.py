# inventory/forms.py
from django import forms
from .models import StockMovement
from products.models import Medicine


class StockUpdateForm(forms.Form):
    MOVEMENT_CHOICES = [
        ('in', 'Entrée de stock'),
        ('out', 'Sortie de stock'),
        ('adjustment', 'Ajustement'),
    ]

    movement_type = forms.ChoiceField(
        choices=MOVEMENT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    reason = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Motif de la modification"
    )


class StockMovementFilterForm(forms.Form):
    medicine = forms.ModelChoiceField(
        queryset=Medicine.objects.all(),
        required=False,
        empty_label="Tous les médicaments",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    movement_type = forms.ChoiceField(
        choices=[('', 'Tous les types')] + StockMovement.MOVEMENT_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )


# NOTE: Les vues ont été déplacées vers inventory/views.py
# Ce fichier ne contient que les formulaires