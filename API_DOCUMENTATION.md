# 📱 Documentation API REST - NyangaBudget

## Vue d'ensemble

API REST complète avec authentification JWT pour application mobile NyangaBudget.

**Base URL Production:** `https://jolubot.pythonanywhere.com/api/v1`  
**Base URL Développement:** `http://localhost:5000/api/v1`

## 🔐 Authentification

### Inscription
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "nom": "John Doe",
  "email": "john@example.com",
  "password": "motdepasse123"
}
```

**Réponse 201:**
```json
{
  "success": true,
  "message": "Inscription réussie",
  "user_id": 123
}
```

### Connexion
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "motdepasse123"
}
```

**Réponse 200:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 123,
    "nom": "John Doe",
    "email": "john@example.com"
  }
}
```

**Durée de vie:**
- Access Token: 1 heure
- Refresh Token: 30 jours

### Rafraîchir le Token
```http
POST /api/v1/auth/refresh
Authorization: Bearer <refresh_token>
```

**Réponse 200:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Utilisateur Actuel
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

**Réponse 200:**
```json
{
  "id": 123,
  "nom": "John Doe",
  "email": "john@example.com",
  "date_inscription": "2026-01-09"
}
```

---

## 💰 Dépenses

### Liste des Dépenses
```http
GET /api/v1/depenses?page=1&limit=20&categorie_id=5
Authorization: Bearer <access_token>
```

**Paramètres Query:**
- `page` (int, défaut: 1): Numéro de page
- `limit` (int, défaut: 20): Éléments par page
- `categorie_id` (int, optionnel): Filtrer par catégorie
- `date_debut` (date, optionnel): Format YYYY-MM-DD
- `date_fin` (date, optionnel): Format YYYY-MM-DD

**Réponse 200:**
```json
{
  "items": [
    {
      "id": 456,
      "nom": "Courses Carrefour",
      "montant": 15000,
      "date": "2026-01-09",
      "categorie": {
        "id": 5,
        "nom": "Alimentation"
      },
      "compte": {
        "id": 2,
        "nom": "Compte Principal"
      }
    }
  ],
  "total": 152,
  "page": 1,
  "pages": 8
}
```

### Détails d'une Dépense
```http
GET /api/v1/depenses/456
Authorization: Bearer <access_token>
```

**Réponse 200:**
```json
{
  "id": 456,
  "nom": "Courses Carrefour",
  "montant": 15000,
  "date": "2026-01-09",
  "notes": "Achats hebdomadaires",
  "categorie": {
    "id": 5,
    "nom": "Alimentation"
  },
  "compte": {
    "id": 2,
    "nom": "Compte Principal"
  }
}
```

### Créer une Dépense
```http
POST /api/v1/depenses
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nom": "Restaurant Le Palais",
  "montant": 8500,
  "date": "2026-01-09",
  "categorie_id": 6,
  "compte_id": 2,
  "notes": "Déjeuner d'affaires"
}
```

**Réponse 201:**
```json
{
  "success": true,
  "depense_id": 789,
  "message": "Dépense créée"
}
```

### Modifier une Dépense
```http
PUT /api/v1/depenses/789
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nom": "Restaurant Le Palais (Modifié)",
  "montant": 9000,
  "notes": "Mise à jour du montant"
}
```

**Réponse 200:**
```json
{
  "success": true,
  "message": "Dépense mise à jour"
}
```

### Supprimer une Dépense
```http
DELETE /api/v1/depenses/789
Authorization: Bearer <access_token>
```

**Réponse 200:**
```json
{
  "success": true,
  "message": "Dépense supprimée"
}
```

---

## 💵 Revenus

### Liste des Revenus
```http
GET /api/v1/revenus?page=1&limit=20
Authorization: Bearer <access_token>
```

**Réponse 200:**
```json
{
  "items": [
    {
      "id": 101,
      "source": "Salaire Janvier",
      "montant": 500000,
      "date": "2026-01-05",
      "recurrent": true
    }
  ],
  "total": 24,
  "page": 1,
  "pages": 2
}
```

### Créer un Revenu
```http
POST /api/v1/revenus
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "source": "Prime Performance",
  "montant": 100000,
  "date": "2026-01-09",
  "recurrent": false
}
```

**Réponse 201:**
```json
{
  "success": true,
  "revenu_id": 102,
  "message": "Revenu créé"
}
```

### Supprimer un Revenu
```http
DELETE /api/v1/revenus/102
Authorization: Bearer <access_token>
```

**Réponse 200:**
```json
{
  "success": true,
  "message": "Revenu supprimé"
}
```

---

## 🏷️ Catégories

### Liste des Catégories
```http
GET /api/v1/categories
Authorization: Bearer <access_token>
```

**Réponse 200:**
```json
{
  "items": [
    {
      "id": 5,
      "nom": "Alimentation",
      "type": "depense",
      "couleur": "#ff6b6b",
      "icon": "bi-cart"
    },
    {
      "id": 6,
      "nom": "Restaurant",
      "type": "depense",
      "couleur": "#4ecdc4",
      "icon": "bi-shop"
    }
  ]
}
```

### Créer une Catégorie
```http
POST /api/v1/categories
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "nom": "Santé",
  "type": "depense",
  "couleur": "#95e1d3",
  "icon": "bi-heart-pulse"
}
```

**Réponse 201:**
```json
{
  "success": true,
  "categorie_id": 7
}
```

---

## 📊 Statistiques

### Statistiques Globales
```http
GET /api/v1/stats
Authorization: Bearer <access_token>
```

**Réponse 200:**
```json
{
  "total_depenses": 450000,
  "total_revenus": 600000,
  "solde": 150000,
  "nb_depenses": 87,
  "nb_revenus": 12
}
```

---

## 🧪 Tests Automatiques

### Exécuter les Tests

**Développement:**
```bash
python test_api.py
```

**Production:**
```bash
python test_api.py https://jolubot.pythonanywhere.com/api/v1
```

**Tests Inclus (15 tests):**
1. ✅ Inscription utilisateur
2. ✅ Connexion JWT
3. ✅ Récupération utilisateur connecté
4. ✅ Création catégorie
5. ✅ Liste catégories
6. ✅ Création dépense
7. ✅ Liste dépenses paginées
8. ✅ Détails dépense
9. ✅ Modification dépense
10. ✅ Création revenu
11. ✅ Liste revenus
12. ✅ Statistiques
13. ✅ Rafraîchissement token
14. ✅ Suppression dépense
15. ✅ Suppression revenu

---

## 🔒 Codes d'Erreur

| Code | Description |
|------|-------------|
| 200 | Succès |
| 201 | Ressource créée |
| 400 | Requête invalide |
| 401 | Non authentifié (token invalide/expiré) |
| 404 | Ressource non trouvée |
| 409 | Conflit (email déjà utilisé) |
| 500 | Erreur serveur |

**Exemple erreur:**
```json
{
  "error": "Token has expired"
}
```

---

## 📱 Exemple d'Intégration Mobile

### Flutter/Dart
```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class NyangaAPI {
  static const baseUrl = 'https://jolubot.pythonanywhere.com/api/v1';
  String? accessToken;
  
  Future<void> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'email': email, 'password': password}),
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      accessToken = data['access_token'];
    }
  }
  
  Future<List<dynamic>> getDepenses() async {
    final response = await http.get(
      Uri.parse('$baseUrl/depenses'),
      headers: {'Authorization': 'Bearer $accessToken'},
    );
    
    if (response.statusCode == 200) {
      final data = jsonDecode(response.body);
      return data['items'];
    }
    return [];
  }
}
```

### React Native/JavaScript
```javascript
const API_BASE = 'https://jolubot.pythonanywhere.com/api/v1';

class NyangaAPI {
  constructor() {
    this.accessToken = null;
  }
  
  async login(email, password) {
    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({email, password})
    });
    
    const data = await response.json();
    this.accessToken = data.access_token;
    return data;
  }
  
  async getDepenses(page = 1, limit = 20) {
    const response = await fetch(
      `${API_BASE}/depenses?page=${page}&limit=${limit}`,
      {
        headers: {'Authorization': `Bearer ${this.accessToken}`}
      }
    );
    
    return await response.json();
  }
  
  async createDepense(depense) {
    const response = await fetch(`${API_BASE}/depenses`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.accessToken}`
      },
      body: JSON.stringify(depense)
    });
    
    return await response.json();
  }
}

export default new NyangaAPI();
```

---

## 📝 Notes Importantes

### Sécurité
- ✅ Tous les endpoints protégés par JWT
- ✅ Tokens expirables (1h access, 30j refresh)
- ✅ Validation des données côté serveur
- ✅ Rate limiting actif (20 req/min)

### Performance
- ✅ Pagination automatique (20 items/page)
- ✅ Cache serveur (5-10min)
- ✅ Filtres optimisés (date, catégorie)

### Best Practices
1. **Stocker le refresh_token de manière sécurisée** (Keychain iOS, Keystore Android)
2. **Rafraîchir l'access_token avant expiration** (à 45min par exemple)
3. **Gérer les erreurs 401** → rediriger vers login
4. **Utiliser la pagination** pour les listes longues
5. **Implémenter un cache local** pour le mode hors-ligne

---

**Auteur:** NyangaBudget Team  
**Version:** 1.0.0  
**Date:** 9 janvier 2026  
**Support:** https://github.com/jolu-bot/NyangaBudget
