# accounts/forms.py
from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'date_of_birth', 'emergency_contact', 'emergency_phone']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'emergency_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'emergency_phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'phone_number': 'Numéro de téléphone',
            'address': 'Adresse',
            'date_of_birth': 'Date de naissance',
            'emergency_contact': 'Contact d\'urgence',
            'emergency_phone': 'Téléphone d\'urgence',
        }