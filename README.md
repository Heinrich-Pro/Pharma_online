# Documentation de l'API Pharma Online

## Table des matières
1. [Introduction](#introduction)
2. [Authentification](#authentification)
3. [Points d'accès API](#points-daccès-api)
   - [Comptes utilisateurs](#comptes-utilisateurs)
   - [Produits](#produits)
   - [Commandes](#commandes)
   - [Inventaire](#inventaire)
4. [Modèles de données](#modèles-de-données)
5. [Exemples de requêtes](#exemples-de-requêtes)
6. [Gestion des erreurs](#gestion-des-erreurs)

## Introduction

Cette API permet de gérer une pharmacie en ligne avec les fonctionnalités suivantes :
- Gestion des utilisateurs (inscription, connexion, déconnexion)
- Consultation et recherche de produits
- Gestion du panier et des commandes
- Gestion des stocks (réservé aux administrateurs)
- Génération de factures au format PDF

## Authentification

L'API utilise le système d'authentification par session de Django. Certaines routes nécessitent une authentification et/ou des droits d'administrateur.

## Points d'accès API

### Comptes utilisateurs

| Méthode | Endpoint | Description | Authentification requise |
|---------|----------|-------------|--------------------------|
| POST | /accounts/register/ | Inscription d'un nouvel utilisateur | Non |
| POST | /accounts/login/ | Connexion d'un utilisateur | Non |
| POST | /accounts/logout/ | Déconnexion de l'utilisateur | Oui |

### Produits

| Méthode | Endpoint | Description | Paramètres de requête |
|---------|----------|-------------|----------------------|
| GET | /products/ | Liste des produits | `category` (optionnel), `search` (optionnel) |

### Commandes

| Méthode | Endpoint | Description | Authentification requise |
|---------|----------|-------------|--------------------------|
| POST | /orders/cart/add/<int:product_id>/ | Ajouter un produit au panier | Oui |
| GET | /orders/cart/ | Voir le panier | Oui |
| POST | /orders/cart/confirm/ | Confirmer la commande | Oui |
| GET | /orders/order/<int:order_id>/ | Détails d'une commande | Oui (propriétaire uniquement) |

### Inventaire

| Méthode | Endpoint | Description | Authentification requise |
|---------|----------|-------------|--------------------------|
| GET, POST | /inventory/ | Gérer les stocks (admin) | Oui (staff uniquement) |

## Modèles de données

### Utilisateur (User)
- `username` (string): Nom d'utilisateur
- `email` (string): Adresse email
- `password` (string): Mot de passe (hashé)
- `is_staff` (booléen): Si l'utilisateur est administrateur

### Produit (Product)
- `name` (string): Nom du produit
- `description` (text): Description détaillée
- `price` (decimal): Prix unitaire
- `category` (Category): Catégorie du produit
- `image` (image, optionnel): Image du produit

### Commande (Order)
- `user` (User): Utilisateur ayant passé la commande
- `status` (string): Statut de la commande ('pending', 'confirmed', 'shipped', 'delivered')
- `created_at` (datetime): Date de création
- `total_price` (decimal): Montant total

### Ligne de commande (OrderItem)
- `order` (Order): Commande associée
- `product` (Product): Produit commandé
- `quantity` (integer): Quantité
- `price` (decimal): Prix unitaire au moment de la commande

### Inventaire (Inventory)
- `product` (Product): Produit en stock
- `quantity` (integer): Quantité disponible

## Exemples de requêtes

### Inscription d'un nouvel utilisateur
```http
POST /accounts/register/
Content-Type: application/x-www-form-urlencoded

username=john_doe&email=john@example.com&password1=securepass123&password2=securepass123
```

### Ajout d'un produit au panier
```http
POST /orders/cart/add/1/
```

### Confirmation d'une commande
```http
POST /orders/cart/confirm/
```

### Consultation des produits avec filtres
```http
GET /products/?category=1&search=paracetamol
```

## Gestion des erreurs

L'API renvoie des codes HTTP standard :
- 200 : Requête réussie
- 302 : Redirection (après connexion/déconnexion)
- 400 : Mauvaise requête (données invalides)
- 403 : Accès refusé (droits insuffisants)
- 404 : Ressource non trouvée
- 500 : Erreur serveur

Les messages d'erreur sont renvoyés au format JSON avec une clé `error` contenant la description de l'erreur.

---
Documentation générée le 04/08/2025
