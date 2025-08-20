# accounts/forms.py
# Formulaires pour la gestion des profils utilisateurs
# Définit les champs et widgets pour la modification des informations personnelles

from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Formulaire pour la modification du profil utilisateur
    
    Ce formulaire permet aux utilisateurs de modifier :
    - Leur numéro de téléphone
    - Leur adresse
    - Leur date de naissance
    - Leur contact d'urgence
    - Leur téléphone d'urgence
    
    Hérite de ModelForm pour une intégration automatique avec le modèle UserProfile
    """
    
    class Meta:
        # Modèle associé au formulaire
        model = UserProfile
        
        # Champs à inclure dans le formulaire
        fields = [
            'phone_number',      # Numéro de téléphone principal
            'address',           # Adresse complète
            'date_of_birth',     # Date de naissance
            'emergency_contact', # Nom du contact d'urgence
            'emergency_phone',   # Téléphone du contact d'urgence
        ]
        
        # Configuration des widgets pour une interface utilisateur moderne
        widgets = {
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control',  # Classe Bootstrap pour le style
                    'placeholder': 'Ex: 06 12 34 56 78'
                }
            ),
            'address': forms.Textarea(
                attrs={
                    'class': 'form-control',  # Classe Bootstrap
                    'rows': 3,                # Hauteur du champ texte
                    'placeholder': 'Votre adresse complète'
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'class': 'form-control',  # Classe Bootstrap
                    'type': 'date'            # Sélecteur de date HTML5
                }
            ),
            'emergency_contact': forms.TextInput(
                attrs={
                    'class': 'form-control',  # Classe Bootstrap
                    'placeholder': 'Nom et prénom du contact d\'urgence'
                }
            ),
            'emergency_phone': forms.TextInput(
                attrs={
                    'class': 'form-control',  # Classe Bootstrap
                    'placeholder': 'Téléphone du contact d\'urgence'
                }
            ),
        }
        
        # Labels en français pour une meilleure expérience utilisateur
        labels = {
            'phone_number': 'Numéro de téléphone',
            'address': 'Adresse',
            'date_of_birth': 'Date de naissance',
            'emergency_contact': 'Contact d\'urgence',
            'emergency_phone': 'Téléphone d\'urgence',
        }