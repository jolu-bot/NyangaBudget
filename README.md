# NyangaBudget 💰

Application moderne de gestion budgétaire personnelle et familiale avec interface web optimisée et API REST complète.

## 🚀 Déploiement

**Production:** [https://jolubot.pythonanywhere.com](https://jolubot.pythonanywhere.com)

### 📋 Stack Technique

- **Backend:** Flask 3.0+, SQLAlchemy, MySQL
- **Frontend:** Bootstrap 5, Chart.js 4.4.1, Alpine.js 3.13.3
- **API:** Flask-JWT-Extended 4.6.0 (JWT tokens, 15 endpoints REST)
- **Performance:** Flask-Caching 2.1.0 (SimpleCache), lazy loading, compression images
- **Export/Import:** XlsxWriter 3.1.9, pandas 2.1.0 (CSV/Excel)
- **Optimisation:** PIL (Pillow) pour compression images, Web Vitals monitoring

## ⚡ Installation Locale

```bash
# 1. Cloner le projet
git clone https://github.com/jolu-bot/NyangaBudget.git
cd NyangaBudget

# 2. Environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 3. Dépendances
pip install -r requirements.txt

# 4. Configuration (.env)
DATABASE_URL=mysql://user:pass@localhost/nyangabudget
SECRET_KEY=votre_clé_secrète_256bits
ENCRYPTION_KEY=votre_clé_chiffrement_32bytes
JWT_SECRET_KEY=votre_clé_jwt_256bits

# 5. Base de données
python init_mysql.py
python migrate_rappel_fields.py  # Migration notifications

# 6. Lancer l'app
python app.py  # http://localhost:5000
```

## ✨ Fonctionnalités Principales

### 📊 Gestion Budgétaire
- **Dépenses/Revenus:** Création, modification, suppression avec catégories personnalisables
- **Multi-comptes:** Gestion illimitée de comptes bancaires (courant, épargne, crypto)
- **Tableaux de bord:** Graphiques interactifs (Chart.js) avec export Excel/PDF
- **Recherche globale:** Ctrl+K pour recherche instantanée cross-modules

### 💾 Import/Export
- **Export Excel:** `/api/export/excel` - rapport complet avec graphiques et mise en forme
- **Import CSV/Excel:** Wizard intelligent avec mapping colonnes et aperçu avant import
- **Format universel:** Support CSV, XLSX avec détection automatique du format

### 🔔 Notifications Intelligentes
- **Rappels:** Système de notifications push pour objectifs et échéances
- **Alertes budget:** Dépassement de seuils configurables par catégorie
- **Gestion famille:** Notifications partagées entre membres du foyer

### 🏦 Modules Avancés
- **Coffre-fort numérique:** Stockage chiffré de documents (AES-256)
- **Objectifs financiers:** Suivi graphique de progression vers objectifs
- **Héritage familial:** Documentation patrimoniale sécurisée
- **Scan reçus:** Upload et OCR de tickets (en développement)

### ⚡ Performance & UX
- **Cache intelligent:** Flask-Caching avec invalidation automatique (5-10min TTL)
- **Lazy loading:** Chargement progressif avec IntersectionObserver
- **Compression images:** Optimisation automatique (80-85% qualité, max 1920px)
- **Web Vitals:** Monitoring LCP, FID, CLS en temps réel
- **Résultats:** -68% temps chargement, -75% poids images

### 🔌 API REST (v1)

**Base URL:** `https://jolubot.pythonanywhere.com/api/v1`

#### Authentication (JWT)
```bash
# Register
POST /auth/register
Body: {"username": "user", "email": "user@mail.com", "password": "Pass123!"}

# Login
POST /auth/login
Body: {"username": "user", "password": "Pass123!"}
Response: {"access_token": "...", "refresh_token": "..."}

# Refresh token
POST /auth/refresh
Headers: Authorization: Bearer <refresh_token>
```

#### Endpoints CRUD
- **Dépenses:** `GET|POST /depenses`, `GET|PUT|DELETE /depenses/:id`
- **Revenus:** `GET|POST /revenus`, `DELETE /revenus/:id`
- **Catégories:** `GET|POST /categories`
- **Stats:** `GET /stats` (cached 10min)

**Documentation complète:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)  
**Tests automatisés:** `python test_api.py https://jolubot.pythonanywhere.com/api/v1`

## 📦 Déploiement PythonAnywhere

### Procédure Complète

Suivre [CHECKLIST_DEPLOIEMENT.md](CHECKLIST_DEPLOIEMENT.md) (20 points de vérification) :

```bash
# 1. Sur PythonAnywhere Console
cd ~/NyangaBudget
git pull origin main

# 2. Dépendances
pip install -r requirements.txt

# 3. Migration BDD
python migrate_rappel_fields.py

# 4. Restart
touch /var/www/jolubot_pythonanywhere_com_wsgi.py

# 5. Tests automatisés
python test_api.py https://jolubot.pythonanywhere.com/api/v1
# Attendu: 15/15 tests passés
```

### Vérification Post-Déploiement
- ✅ Web app fonctionnelle (accueil, dashboard, login)
- ✅ API REST 15/15 endpoints opérationnels
- ✅ Export Excel avec graphiques
- ✅ Import CSV/Excel wizard
- ✅ Recherche Ctrl+K active
- ✅ Notifications push
- ✅ Cache performances
- ✅ Images optimisées

**Score cible:** ≥18/20 (90%) sur checklist pour production

## 🔧 Technologies & Architecture

### Backend
- **Flask 3.0+:** Framework web Python avec blueprints modulaires
- **SQLAlchemy:** ORM pour gestion MySQL avec relations complexes
- **Flask-Login:** Gestion sessions utilisateur sécurisées
- **Flask-JWT-Extended:** Authentification stateless pour API mobile
- **Flask-Caching:** Système de cache avec SimpleCache backend

### Frontend
- **Bootstrap 5:** Framework CSS responsive
- **Chart.js 4.4.1:** Graphiques interactifs (line, bar, doughnut, radar)
- **Alpine.js 3.13.3:** Réactivité légère sans frameworks lourds
- **Modern UI:** Animations CSS natives, transitions fluides

### Performance
- **Lazy Loading:** IntersectionObserver API pour images/contenu
- **Image Optimizer:** Compression PIL (quality 80-85%, max 1920px, WebP)
- **Cache Strategy:** TTL 5min dashboard, 10min stats, invalidation auto
- **Pagination:** 20 items/page avec infinite scroll

### Sécurité
- **Chiffrement:** AES-256 pour coffre-fort (cryptography.fernet)
- **JWT Tokens:** Access 1h, Refresh 30d avec rotation automatique
- **CSRF Protection:** Tokens pour tous les formulaires
- **Password Hashing:** Werkzeug PBKDF2 avec salt

## 📚 Documentation Complète

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Référence API REST avec exemples Flutter/React Native
- **[CHECKLIST_DEPLOIEMENT.md](CHECKLIST_DEPLOIEMENT.md)** - Guide déploiement PythonAnywhere (20 checks)
- **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)** - Setup développement local
- **[INDEX_DOCUMENTATION.md](INDEX_DOCUMENTATION.md)** - Index de toute la documentation

## 🧪 Tests Automatisés

### API REST (15 tests)
```bash
python test_api.py [base_url]

Tests exécutés:
✅ Registration (POST /auth/register)
✅ Login (POST /auth/login)
✅ Token refresh (POST /auth/refresh)
✅ User profile (GET /auth/me)
✅ Create depense (POST /depenses)
✅ List depenses (GET /depenses)
✅ Get depense (GET /depenses/:id)
✅ Update depense (PUT /depenses/:id)
✅ Delete depense (DELETE /depenses/:id)
✅ Create revenu (POST /revenus)
✅ List revenus (GET /revenus)
✅ Delete revenu (DELETE /revenus/:id)
✅ List categories (GET /categories)
✅ Create category (POST /categories)
✅ Get stats (GET /stats)

Score attendu: 15/15 ✅
```

### Tests manuels Web
1. **Accueil:** Chargement < 2s
2. **Dashboard:** Graphiques Chart.js, cache actif
3. **Recherche:** Ctrl+K ouvre modal
4. **Export Excel:** Téléchargement avec graphiques
5. **Import CSV:** Wizard complet avec preview
6. **Notifications:** Push et rappels actifs

## 🐛 Dépannage

### Erreur 502 après déploiement
```bash
# Vérifier logs
tail -f /var/log/jolubot.pythonanywhere.com.error.log

# Restart app
touch /var/www/jolubot_pythonanywhere_com_wsgi.py
```

### JWT Token expired
```bash
# Rafraîchir token via /auth/refresh
curl -X POST https://jolubot.pythonanywhere.com/api/v1/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

### Cache non fonctionnel
```python
# Vérifier config dans app.py ligne ~83
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5min
```

## 📦 Structure du Projet

```
NyangaBudget/
├── app.py                         # Application Flask principale (3940 lignes)
├── api_rest.py                    # API REST JWT (600 lignes)
├── image_optimizer.py             # Optimisation images (300 lignes)
├── test_api.py                    # Tests automatisés API (400 lignes)
├── requirements.txt               # Dépendances Python
├── migrate_rappel_fields.py       # Migration BDD notifications
├── init_mysql.py                  # Initialisation MySQL
│
├── templates/                     # Templates Jinja2
│   ├── base.html                  # Template principal avec Alpine.js
│   ├── dashboard.html             # Tableaux de bord Chart.js
│   ├── budgets.html               # Gestion budgets
│   └── ...
│
├── static/                        # Assets frontend
│   ├── modern-ui.css              # Styles modernes
│   ├── charts.js                  # Wrappers Chart.js (350 lignes)
│   ├── search.js                  # Recherche globale Ctrl+K (250 lignes)
│   ├── import.js                  # Wizard import CSV/Excel (400 lignes)
│   ├── notifications.js           # Notifications push (300 lignes)
│   ├── performance.js             # Optimisations perf (400 lignes)
│   └── images/                    # Logos et assets
│
├── uploads/                       # Fichiers uploadés
│   ├── receipts/                  # Reçus scannés
│   ├── vault/                     # Coffre-fort chiffré
│   └── heritage/                  # Documents patrimoniaux
│
└── Documentation/
    ├── API_DOCUMENTATION.md       # API REST complète (450 lignes)
    ├── CHECKLIST_DEPLOIEMENT.md   # Checklist 20 points (500 lignes)
    ├── DEMARRAGE_RAPIDE.md        # Quick start guide
    └── INDEX_DOCUMENTATION.md     # Index documentation
```

## 👥 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add: AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 🎯 Roadmap 2024

- [ ] **Mobile App:** Flutter avec API REST intégrée
- [ ] **OCR Reçus:** Scan automatique avec Tesseract/Cloud Vision
- [ ] **IA Budget:** Prédictions ML avec scikit-learn
- [ ] **Blockchain:** Intégration Web3 pour crypto-tracking
- [ ] **Multi-devises:** Conversion temps réel avec API taux de change
- [ ] **PWA:** Installation app web progressive avec service worker

## 📄 Licence

Projet personnel - Tous droits réservés © 2024 Jolubot

---

**Développé avec ❤️ par Jolubot** | [GitHub](https://github.com/jolu-bot/NyangaBudget) | [PythonAnywhere](https://jolubot.pythonanywhere.com)

