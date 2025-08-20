<<<<<<< HEAD
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})
=======
# accounts/views.py
# Vues pour la gestion des comptes utilisateurs
# Gère l'inscription, la connexion et la modification des profils

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm


def register(request):
    """
    Vue pour l'inscription d'un nouvel utilisateur
    
    Cette fonction :
    1. Affiche le formulaire d'inscription en GET
    2. Traite le formulaire soumis en POST
    3. Crée automatiquement un profil utilisateur associé
    4. Connecte l'utilisateur après inscription
    5. Redirige vers la liste des médicaments
    """
    if request.method == 'POST':
        # Traitement du formulaire soumis
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Création de l'utilisateur
            user = form.save()
            # Création automatique d'un profil utilisateur vide
            UserProfile.objects.create(user=user)
            # Connexion automatique de l'utilisateur
            login(request, user)
            # Message de succès
            messages.success(request, 'Compte créé avec succès!')
            # Redirection vers la page d'accueil des produits
            return redirect('products:medicine_list')
    else:
        # Affichage du formulaire vide en GET
        form = UserCreationForm()

    # Rendu du template avec le formulaire
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    """
    Vue pour afficher et modifier le profil utilisateur
    
    Cette fonction :
    1. Nécessite une connexion (@login_required)
    2. Récupère ou crée le profil utilisateur
    3. Affiche le formulaire de modification en GET
    4. Traite les modifications soumises en POST
    5. Met à jour le profil et affiche un message de succès
    
    Décorateur @login_required : redirige vers la page de connexion si non connecté
    """
    # Récupération du profil existant ou création d'un nouveau
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Traitement du formulaire de modification
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Sauvegarde des modifications
            form.save()
            messages.success(request, 'Profil mis à jour avec succès!')
            # Redirection vers la même page pour afficher les changements
            return redirect('accounts:profile')
    else:
        # Affichage du formulaire pré-rempli avec les données existantes
        form = UserProfileForm(instance=profile)

    # Rendu du template avec le formulaire et le profil
    return render(request, 'accounts/profile.html', {'form': form})


# NOTE: La fonction home a été déplacée vers products/views.py
# où elle a accès aux modèles Medicine et Category
>>>>>>> develop
