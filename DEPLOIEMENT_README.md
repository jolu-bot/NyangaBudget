# 🚀 Déploiement NyangaBudget 2.0 sur PythonAnywhere

## 📌 Liens Rapides

- **Guide complet** : [GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md](GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md)
- **Checklist** : [CHECKLIST_PYTHONANYWHERE.md](CHECKLIST_PYTHONANYWHERE.md)
- **Script d'aide** : `python deploy_helper.py`
- **Template .env** : [.env.example](.env.example)

---

## ⚡ Démarrage Rapide (5 min)

### 1️⃣ Script d'Aide (Recommandé)

```bash
# Lancer l'assistant de déploiement
python deploy_helper.py

# Choisir option 8 : "Tout vérifier"
```

Le script va :
- ✅ Générer votre SECRET_KEY
- ✅ Vérifier tous les fichiers
- ✅ Créer la config WSGI
- ✅ Générer les commandes de déploiement

### 2️⃣ Sur PythonAnywhere

```bash
# Console Bash PythonAnywhere
git clone https://github.com/jolu-bot/NyangaBudget.git
cd NyangaBudget
mkvirtualenv --python=/usr/bin/python3.10 nyangabudget-env
pip install -r requirements.txt
```

### 3️⃣ Configuration Web App

- **Web Tab** → Add new web app → Manual → Python 3.10
- **WSGI file** → Copier le contenu généré par `deploy_helper.py`
- **Static files** :
  - `/static/` → `/home/USERNAME/NyangaBudget/static/`
  - `/uploads/` → `/home/USERNAME/NyangaBudget/uploads/`

### 4️⃣ Initialiser DB et Lancer

```bash
# Dans console PythonAnywhere
python3
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

**Reload** l'app dans Web tab → Visiter votre site !

---

## 📚 Documentation Complète

### Pour Débutants

👉 **[GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md](GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md)**

Guide pas-à-pas avec :
- Screenshots et explications détaillées
- Dépannage pour chaque étape
- Optimisations et bonnes pratiques
- Section maintenance et mises à jour

### Checklist Interactive

👉 **[CHECKLIST_PYTHONANYWHERE.md](CHECKLIST_PYTHONANYWHERE.md)**

Liste complète avec cases à cocher :
- ✅ Avant déploiement
- ✅ Configuration PythonAnywhere
- ✅ Tests fonctionnels
- ✅ Validation finale

---

## 🛠️ Outils Disponibles

### Script d'Aide Python

```bash
python deploy_helper.py
```

**Fonctionnalités** :
1. Générer SECRET_KEY sécurisée
2. Vérifier fichiers projet
3. Vérifier dossiers requis
4. Analyser dépendances
5. Générer config WSGI
6. Lister variables d'environnement
7. Générer commandes déploiement
8. **Tout vérifier (recommandé)**

### Template Variables d'Environnement

```bash
# Copier le template
cp .env.example .env

# Éditer avec vos valeurs
nano .env
```

Variables **obligatoires** :
- `SECRET_KEY` : Clé secrète Flask
- `DATABASE_URL` : URL base de données
- `FLASK_ENV=production`
- `FLASK_DEBUG=0`

---

## 🎯 Versions et Prérequis

### Versions Testées

| Composant | Version |
|-----------|---------|
| Python | 3.10+ |
| Flask | 3.0.0+ |
| SQLAlchemy | 3.1.1+ |
| Bootstrap | 5.3.2 |
| Plotly.js | 2.27.0 |

### Compte PythonAnywhere

- **Gratuit** : Suffisant pour tests (limitations CPU)
- **Payant** : Recommandé pour production (MySQL, domaine custom)

---

## 📦 Structure du Projet

```
NyangaBudget/
├── app.py                           # Application Flask principale
├── requirements.txt                 # Dépendances Python
├── .env.example                     # Template variables d'environnement
├── deploy_helper.py                 # Script d'aide déploiement
│
├── GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md    # Guide complet
├── CHECKLIST_PYTHONANYWHERE.md            # Checklist déploiement
├── MODERNISATION_FINALE.md                # Documentation design
│
├── static/                          # Fichiers statiques
│   ├── style.css                    # Styles base
│   ├── navbar-modern.css            # Navbar moderne (716 lignes)
│   ├── dashboard-modern.css         # Dashboard (393 lignes)
│   ├── forms-modern.css             # Formulaires (500+ lignes)
│   ├── darkmode.js                  # Dark mode
│   └── images/                      # Images et logos
│
├── templates/                       # Templates HTML
│   ├── base.html                    # Template de base
│   ├── dashboard.html               # Dashboard principal
│   ├── login.html                   # Page connexion
│   └── ...                          # Autres pages
│
├── data/                            # Base de données SQLite
│   └── nyanga.db                    # (créé au déploiement)
│
└── uploads/                         # Fichiers uploadés
    ├── vault/                       # Coffre-fort chiffré
    ├── heritage/                    # Documents testament
    └── receipts/                    # Reçus scannés
```

---

## ✅ Vérifications Pré-Déploiement

### Localement

```bash
# Tester l'application
python app.py

# Vérifier dépendances
pip list

# Lancer script de vérification
python deploy_helper.py
```

### Checklist Minimale

- [ ] Application démarre localement sans erreur
- [ ] Tous les commits pushés sur GitHub
- [ ] requirements.txt à jour
- [ ] .env.example créé
- [ ] Documentation lue

---

## 🔐 Sécurité

### Variables Sensibles

⚠️ **NE JAMAIS COMMIT** :
- `.env` (fichier réel avec vraies valeurs)
- `data/nyanga.db` (base de données)
- Clés API privées

✅ **Toujours vérifier** :
- `.gitignore` contient `.env`
- `DEBUG = False` en production
- `SECRET_KEY` unique et complexe

### Compte Admin Par Défaut

**⚠️ IMPORTANT** : Changer le mot de passe admin après premier déploiement !

Identifiants par défaut :
- Email : `admin@nyanga.cm`
- Mot de passe : `admin123`

---

## 🐛 Dépannage Rapide

### App ne démarre pas

```bash
# Vérifier logs
tail -f /var/log/USERNAME.pythonanywhere.com.error.log

# Tester import
python3 -c "from app import app"
```

### CSS ne charge pas

- Vérifier mappages Static files dans Web tab
- Permissions : `chmod -R 755 static/`
- Vider cache navigateur

### Uploads échouent

```bash
# Créer dossiers
mkdir -p uploads/vault uploads/heritage uploads/receipts

# Permissions
chmod -R 755 uploads/
```

👉 **Dépannage complet** : [GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md#dépannage](GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md)

---

## 📊 Monitoring Post-Déploiement

### PythonAnywhere Dashboard

- **CPU seconds** : Vérifier quota non dépassé
- **Disk space** : Surveiller espace uploads
- **Error log** : Pas d'erreurs critiques

### Tests Fonctionnels

- [ ] Login fonctionne
- [ ] Dashboard affiche stats
- [ ] Création revenus/dépenses OK
- [ ] Upload fichiers OK
- [ ] Dark mode fonctionne
- [ ] Mobile responsive OK

---

## 🔄 Mises à Jour

### Déployer Nouvelles Modifications

```bash
# Sur PythonAnywhere
cd ~/NyangaBudget
git pull origin main
workon nyangabudget-env
pip install -r requirements.txt

# Dans Web tab : Reload
```

### Backup Base de Données

```bash
# Backup manuel
cd ~/NyangaBudget
cp data/nyanga.db data/backups/nyanga_$(date +%Y%m%d).db
```

---

## 🌟 Fonctionnalités Principales

### Design Moderne 2.0
- ✨ Glassmorphism avec backdrop-filter
- 🎨 5 schémas de gradients colorés
- ⚡ 25+ animations CSS (pulse, float, swing, shimmer)
- 🌓 Dark mode complet
- 📱 Responsive (6 breakpoints)

### Fonctionnalités Métier
- 💰 Gestion revenus/dépenses multi-comptes
- 📊 Dashboard avec graphiques Plotly
- 🎯 Budgets et objectifs avec suivi
- 📷 Scan reçus avec OCR (pytesseract)
- 🔐 Coffre-fort chiffré AES-256
- 👨‍👩‍👧‍👦 Gestion familiale avec QR codes
- 🏛️ Testament numérique (héritage)
- 📧 Centre de notifications avec priorités
- 📄 Rapports PDF générés

---

## 📞 Support

### Documentation Projet
- [MODERNISATION_FINALE.md](MODERNISATION_FINALE.md) - Design système complet
- [PHASE_2_COMPLETE.md](PHASE_2_COMPLETE.md) - Phase 2 modernisation
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API endpoints

### Aide PythonAnywhere
- [Documentation officielle](https://help.pythonanywhere.com/)
- [Forums](https://www.pythonanywhere.com/forums/)
- [Contact support](https://www.pythonanywhere.com/support/)

### GitHub
- [Repository](https://github.com/jolu-bot/NyangaBudget)
- [Issues](https://github.com/jolu-bot/NyangaBudget/issues)

---

## 🎉 Après le Déploiement

### Validation
1. ✅ Ouvrir `https://USERNAME.pythonanywhere.com`
2. ✅ Tester login admin
3. ✅ Vérifier design moderne
4. ✅ Créer quelques données de test
5. ✅ Partager l'URL !

### Communication
- Informer l'équipe du déploiement
- Partager identifiants de test
- Documenter l'URL production
- Former les utilisateurs finaux

---

## 📈 Prochaines Étapes

### Optimisations Possibles
- [ ] Migration SQLite → MySQL (plus performant)
- [ ] Minification CSS/JS (réduction taille)
- [ ] Compression Gzip activée
- [ ] Cache Redis (si compte payant)
- [ ] CDN pour assets statiques
- [ ] Monitoring erreurs (Sentry)

### Nouvelles Fonctionnalités
- [ ] Export données Excel
- [ ] Intégration bancaire (Open Banking)
- [ ] App mobile (PWA)
- [ ] Multi-langue (i18n)
- [ ] Notifications push
- [ ] 2FA authentification

---

**Version** : NyangaBudget 2.0 (Post-Modernisation)  
**Dernière mise à jour** : Janvier 2026  
**Mainteneur** : jolu-bot

---

🚀 **Bon déploiement !**
