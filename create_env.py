#!/usr/bin/env python3
"""
Script pour créer le fichier .env avec les variables d'environnement
Ce script génère automatiquement le fichier .env basé sur env_example.txt
"""

import os
import secrets
import string

def generate_secret_key(length=50):
    """Génère une clé secrète Django sécurisée"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_env_file():
    """Crée le fichier .env avec les vraies valeurs"""
    
    # Vérifier si le fichier .env existe déjà
    if os.path.exists('.env'):
        print("⚠️  Le fichier .env existe déjà !")
        response = input("Voulez-vous le remplacer ? (y/N): ")
        if response.lower() != 'y':
            print("❌ Création annulée.")
            return
    
    # Valeurs par défaut pour Render
    env_vars = {
        # Base de données locale (développement)
        'DB_ENGINE': 'django.db.backends.postgresql',
        'DB_NAME': 'pharmacy_db',
        'DB_USER': 'postgres',
        'DB_PASSWORD': 'votre_mot_de_passe_postgres',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        
        # Base de données Render (à remplacer par votre vraie URL)
        'DATABASE_URL': 'postgresql://username:password@host.render.com:5432/database_name',
        
        # Django
        'SECRET_KEY': generate_secret_key(),
        'DEBUG': 'False',  # False pour la production sur Render
        'ALLOWED_HOSTS': 'localhost,127.0.0.1,*.onrender.com,votre-app.onrender.com',
        
        # Fichiers statiques
        'STATIC_URL': '/static/',
        'STATIC_ROOT': 'staticfiles',
        'MEDIA_URL': '/media/',
        'MEDIA_ROOT': 'media',
        
        # Sécurité (True pour la production sur Render)
        'CSRF_COOKIE_SECURE': 'True',
        'SESSION_COOKIE_SECURE': 'True',
        
        # Email (optionnel)
        'EMAIL_HOST': 'smtp.gmail.com',
        'EMAIL_PORT': '587',
        'EMAIL_USE_TLS': 'True',
        'EMAIL_HOST_USER': 'votre_email@gmail.com',
        'EMAIL_HOST_PASSWORD': 'votre_mot_de_passe_app',
        
        # Cache (optionnel)
        'REDIS_URL': 'redis://localhost:6379/0'
    }
    
    # Créer le fichier .env
    with open('.env', 'w', encoding='utf-8') as f:
        f.write("# ===== CONFIGURATION DE LA BASE DE DONNÉES =====\n\n")
        f.write("# Configuration PostgreSQL locale (développement)\n")
        f.write(f"DB_ENGINE={env_vars['DB_ENGINE']}\n")
        f.write(f"DB_NAME={env_vars['DB_NAME']}\n")
        f.write(f"DB_USER={env_vars['DB_USER']}\n")
        f.write(f"DB_PASSWORD={env_vars['DB_PASSWORD']}\n")
        f.write(f"DB_HOST={env_vars['DB_HOST']}\n")
        f.write(f"DB_PORT={env_vars['DB_PORT']}\n\n")
        
        f.write("# Configuration PostgreSQL Render (PRODUCTION)\n")
        f.write("# Remplacez cette URL par celle fournie par Render\n")
        f.write(f"DATABASE_URL={env_vars['DATABASE_URL']}\n\n")
        
        f.write("# ===== CONFIGURATION DJANGO =====\n\n")
        f.write(f"SECRET_KEY={env_vars['SECRET_KEY']}\n")
        f.write(f"DEBUG={env_vars['DEBUG']}\n")
        f.write(f"ALLOWED_HOSTS={env_vars['ALLOWED_HOSTS']}\n\n")
        
        f.write("# ===== CONFIGURATION DES FICHIERS STATIQUES =====\n\n")
        f.write(f"STATIC_URL={env_vars['STATIC_URL']}\n")
        f.write(f"STATIC_ROOT={env_vars['STATIC_ROOT']}\n")
        f.write(f"MEDIA_URL={env_vars['MEDIA_URL']}\n")
        f.write(f"MEDIA_ROOT={env_vars['MEDIA_ROOT']}\n\n")
        
        f.write("# ===== CONFIGURATION DE SÉCURITÉ =====\n\n")
        f.write(f"CSRF_COOKIE_SECURE={env_vars['CSRF_COOKIE_SECURE']}\n")
        f.write(f"SESSION_COOKIE_SECURE={env_vars['SESSION_COOKIE_SECURE']}\n\n")
        
        f.write("# ===== CONFIGURATION EMAIL =====\n\n")
        f.write(f"EMAIL_HOST={env_vars['EMAIL_HOST']}\n")
        f.write(f"EMAIL_PORT={env_vars['EMAIL_PORT']}\n")
        f.write(f"EMAIL_USE_TLS={env_vars['EMAIL_USE_TLS']}\n")
        f.write(f"EMAIL_HOST_USER={env_vars['EMAIL_HOST_USER']}\n")
        f.write(f"EMAIL_HOST_PASSWORD={env_vars['EMAIL_HOST_PASSWORD']}\n\n")
        
        f.write("# ===== CONFIGURATION CACHE =====\n\n")
        f.write(f"REDIS_URL={env_vars['REDIS_URL']}\n")
    
    print("✅ Fichier .env créé avec succès pour Render !")
    print("\n📝 IMPORTANT : Modifiez les valeurs suivantes selon votre configuration Render :")
    print("   - DATABASE_URL : votre URL de base de données Render (format: postgresql://user:pass@host.render.com:5432/dbname)")
    print("   - ALLOWED_HOSTS : ajoutez votre domaine Render (ex: votre-app.onrender.com)")
    print("   - DB_USER et DB_PASSWORD : vos identifiants PostgreSQL locaux pour le développement")
    print("   - EMAIL_HOST_USER et EMAIL_HOST_PASSWORD : vos identifiants email")
    print("\n🔒 Le fichier .env contient des informations sensibles, ne le committez jamais !")
    print("\n🚀 Pour déployer sur Render :")
    print("   1. Créez une base de données PostgreSQL sur Render")
    print("   2. Copiez l'URL de connexion dans DATABASE_URL")
    print("   3. Ajoutez votre domaine Render dans ALLOWED_HOSTS")

if __name__ == "__main__":
    create_env_file()
