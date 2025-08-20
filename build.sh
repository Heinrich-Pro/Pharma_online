#!/usr/bin/env bash
# Script de déploiement pour l'application Django Pharma_online
# Ce script automatise le processus de déploiement sur un serveur de production

# ===== CONFIGURATION DE SÉCURITÉ =====

# Exit on error : arrête l'exécution si une commande échoue
# Évite de continuer avec des erreurs qui pourraient causer des problèmes
set -o errexit

# ===== INSTALLATION DES DÉPENDANCES =====

# Installation des packages Python requis depuis requirements.txt
# Utilise pip pour installer toutes les dépendances listées
echo "📦 Installation des dépendances Python..."
pip install -r requirements.txt

# ===== COLLECTE DES FICHIERS STATIQUES =====

# Collecte de tous les fichiers statiques dans un répertoire central
# Nécessaire pour le déploiement en production
# --no-input : exécution sans interaction utilisateur
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --no-input

# ===== MIGRATION DE LA BASE DE DONNÉES =====

# Application des migrations de base de données
# Met à jour le schéma de la base selon les modèles Django
# --no-input : exécution sans interaction utilisateur
echo "🗄️ Application des migrations de base de données..."
python manage.py migrate

echo "✅ Déploiement terminé avec succès !"