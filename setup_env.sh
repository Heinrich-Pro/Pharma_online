#!/bin/bash
# Script de configuration de l'environnement pour Pharma_online
# Ce script automatise la mise en place des variables d'environnement

echo "🚀 Configuration de l'environnement Pharma_online"
echo "=================================================="

# ===== VÉRIFICATION DES PRÉREQUIS =====

echo "📋 Vérification des prérequis..."

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si pip est installé
if ! command -v pip &> /dev/null; then
    echo "❌ pip n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

echo "✅ Python et pip sont installés"

# ===== INSTALLATION DES DÉPENDANCES =====

echo "📦 Installation des dépendances Python..."

# Activer l'environnement virtuel s'il existe
if [ -d ".venv" ]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source .venv/bin/activate
else
    echo "🔧 Création d'un nouvel environnement virtuel..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Installer les dépendances
pip install -r requirements.txt

echo "✅ Dépendances installées"

# ===== CRÉATION DU FICHIER .ENV =====

echo "🔐 Configuration des variables d'environnement..."

# Exécuter le script Python pour créer le fichier .env
python3 create_env.py

if [ $? -eq 0 ]; then
    echo "✅ Fichier .env créé avec succès"
else
    echo "❌ Erreur lors de la création du fichier .env"
    exit 1
fi

# ===== CRÉATION DES RÉPERTOIRES NÉCESSAIRES =====

echo "📁 Création des répertoires nécessaires..."

# Créer le répertoire des logs
mkdir -p logs

# Créer le répertoire des fichiers statiques
mkdir -p static

# Créer le répertoire des fichiers media
mkdir -p media

echo "✅ Répertoires créés"

# ===== CONFIGURATION DE LA BASE DE DONNÉES =====

echo "🗄️ Configuration de la base de données..."

# Demander les informations de la base de données
echo "Veuillez configurer votre base de données PostgreSQL :"
read -p "Nom d'utilisateur PostgreSQL (défaut: postgres): " db_user
db_user=${db_user:-postgres}

read -s -p "Mot de passe PostgreSQL: " db_password
echo

read -p "Nom de la base de données (défaut: pharmacy_db): " db_name
db_name=${db_name:-pharmacy_db}

read -p "Hôte PostgreSQL (défaut: localhost): " db_host
db_host=${db_host:-localhost}

read -p "Port PostgreSQL (défaut: 5432): " db_port
db_port=${db_port:-5432}

# Mettre à jour le fichier .env
sed -i "s/DB_USER=.*/DB_USER=$db_user/" .env
sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=$db_password/" .env
sed -i "s/DB_NAME=.*/DB_NAME=$db_name/" .env
sed -i "s/DB_HOST=.*/DB_HOST=$db_host/" .env
sed -i "s/DB_PORT=.*/DB_PORT=$db_port/" .env

echo "✅ Configuration de la base de données mise à jour"

# ===== VÉRIFICATION DE LA CONFIGURATION =====

echo "🔍 Vérification de la configuration..."

# Tester la configuration Django
python3 manage.py check

if [ $? -eq 0 ]; then
    echo "✅ Configuration Django valide"
else
    echo "❌ Erreurs dans la configuration Django"
    echo "Veuillez vérifier le fichier .env et les paramètres"
    exit 1
fi

# ===== FINALISATION =====

echo ""
echo "🎉 Configuration terminée avec succès !"
echo ""
echo "📝 Prochaines étapes :"
echo "1. Vérifiez que PostgreSQL est démarré"
echo "2. Créez la base de données : createdb $db_name"
echo "3. Appliquez les migrations : python3 manage.py migrate"
echo "4. Créez un superutilisateur : python3 manage.py createsuperuser"
echo "5. Lancez le serveur : python3 manage.py runserver"
echo ""
echo "🔒 IMPORTANT : Le fichier .env contient des informations sensibles"
echo "   Ne le committez jamais dans Git !"
echo ""
echo "📚 Documentation : consultez le fichier env_example.txt pour plus d'informations"
