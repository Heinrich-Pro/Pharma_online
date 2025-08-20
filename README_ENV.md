# 🔐 Configuration des Variables d'Environnement - Pharma_online

Ce guide explique comment configurer et utiliser les variables d'environnement dans votre projet Django Pharma_online.

## 🎯 **Pourquoi utiliser des Variables d'Environnement ?**

- **🔒 Sécurité** : Évite de committer des informations sensibles dans le code
- **🔄 Flexibilité** : Configuration différente selon l'environnement (dev/prod)
- **🚀 Déploiement** : Facilite le déploiement sur différents serveurs
- **👥 Collaboration** : Chaque développeur peut avoir sa propre configuration

## 📁 **Fichiers de Configuration**

### 1. **`.env`** (à créer - contient vos vraies valeurs)
```
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
SECRET_KEY=votre_cle_secrete
```

### 2. **`env_example.txt`** (exemple de configuration)
Contient la structure des variables avec des valeurs d'exemple.

### 3. **`.gitignore`** (exclut le fichier .env)
Le fichier `.env` ne sera jamais commité dans Git.

## 🚀 **Installation Rapide**

### **Option 1 : Script Automatique (Recommandé)**

```bash
# Rendre le script exécutable
chmod +x setup_env.sh

# Lancer la configuration automatique
./setup_env.sh
```

Le script va :
- ✅ Installer les dépendances
- ✅ Créer le fichier `.env`
- ✅ Configurer la base de données
- ✅ Créer les répertoires nécessaires
- ✅ Vérifier la configuration

### **Option 2 : Configuration Manuelle**

```bash
# 1. Installer python-dotenv
pip install python-dotenv

# 2. Créer le fichier .env
python3 create_env.py

# 3. Modifier le fichier .env avec vos vraies valeurs
nano .env
```

## ⚙️ **Configuration des Variables**

### **Base de Données (Développement)**
```bash
DB_ENGINE=django.db.backends.postgresql
DB_NAME=pharmacy_db
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

### **Base de Données (Production)**
```bash
# URL complète de votre base de données
DATABASE_URL=postgresql://username:password@host:port/database_name
```

### **Django**
```bash
SECRET_KEY=votre_cle_secrete_tres_longue
DEBUG=True  # False en production
ALLOWED_HOSTS=localhost,127.0.0.1,*.onrender.com
```

### **Fichiers Statiques**
```bash
STATIC_URL=/static/
STATIC_ROOT=staticfiles
MEDIA_URL=/media/
MEDIA_ROOT=media
```

### **Sécurité**
```bash
CSRF_COOKIE_SECURE=False  # True en production avec HTTPS
SESSION_COOKIE_SECURE=False  # True en production avec HTTPS
```

### **Email (Optionnel)**
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre_email@gmail.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe_app
```

## 🔧 **Utilisation dans le Code**

### **Dans settings.py**
```python
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Utiliser les variables
SECRET_KEY = os.environ.get('SECRET_KEY', 'valeur_par_defaut')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
```

### **Dans vos vues ou modèles**
```python
import os

# Accéder aux variables d'environnement
db_name = os.environ.get('DB_NAME')
api_key = os.environ.get('API_KEY')
```

## 🌍 **Environnements Multiples**

### **Développement (.env.development)**
```bash
DEBUG=True
DB_HOST=localhost
CSRF_COOKIE_SECURE=False
```

### **Production (.env.production)**
```bash
DEBUG=False
DB_HOST=production-server.com
CSRF_COOKIE_SECURE=True
```

### **Test (.env.test)**
```bash
DEBUG=True
DB_NAME=pharmacy_test_db
```

## 🚨 **Sécurité et Bonnes Pratiques**

### **✅ À FAIRE**
- Utiliser des mots de passe forts
- Changer la clé secrète Django
- Limiter l'accès au fichier `.env`
- Utiliser des variables d'environnement sur le serveur de production

### **❌ À ÉVITER**
- Committer le fichier `.env` dans Git
- Utiliser des mots de passe faibles
- Partager vos variables d'environnement
- Stocker des clés API en dur dans le code

## 🔍 **Vérification de la Configuration**

```bash
# Vérifier que Django peut lire la configuration
python3 manage.py check

# Vérifier les variables d'environnement
python3 manage.py shell
>>> import os
>>> print(os.environ.get('DB_NAME'))
```

## 🆘 **Dépannage**

### **Erreur : "ModuleNotFoundError: No module named 'dotenv'"**
```bash
pip install python-dotenv
```

### **Erreur : "Database connection failed"**
- Vérifiez que PostgreSQL est démarré
- Vérifiez les identifiants dans `.env`
- Testez la connexion : `psql -h localhost -U postgres`

### **Erreur : "SECRET_KEY not set"**
- Vérifiez que le fichier `.env` existe
- Vérifiez que `SECRET_KEY` est défini
- Redémarrez le serveur Django

## 📚 **Ressources Utiles**

- [Documentation python-dotenv](https://github.com/theskumar/python-dotenv)
- [Variables d'environnement Django](https://docs.djangoproject.com/en/stable/topics/settings/)
- [Sécurité Django](https://docs.djangoproject.com/en/stable/topics/security/)

## 🤝 **Support**

Si vous rencontrez des problèmes :
1. Vérifiez que tous les fichiers sont créés
2. Vérifiez la syntaxe du fichier `.env`
3. Vérifiez que PostgreSQL est accessible
4. Consultez les logs Django pour plus de détails

---

**🎉 Félicitations !** Votre projet est maintenant configuré avec des variables d'environnement sécurisées.
