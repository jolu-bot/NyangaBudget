# ✅ Checklist de Déploiement PythonAnywhere

## 📋 Avant le Déploiement

### Préparation Locale
- [ ] Tous les fichiers sont commités sur Git
- [ ] Tests locaux réussis : `python app.py`
- [ ] Aucune erreur dans la console
- [ ] requirements.txt à jour : `pip freeze > requirements.txt`
- [ ] .env.example créé avec toutes les variables
- [ ] Documentation à jour

### Vérifications Code
- [ ] DEBUG = False dans app.py pour production
- [ ] SECRET_KEY chargée depuis variable d'environnement
- [ ] Chemins uploads configurés correctement
- [ ] Rate limiting activé
- [ ] CSRF protection activée
- [ ] Validation formulaires en place

---

## 🔧 Configuration PythonAnywhere

### Compte et Console
- [ ] Compte PythonAnywhere créé
- [ ] Console Bash ouverte
- [ ] Repository cloné : `git clone https://github.com/jolu-bot/NyangaBudget.git`
- [ ] Navigué dans le dossier : `cd NyangaBudget`

### Environnement Virtuel
- [ ] Virtualenv créé : `mkvirtualenv --python=/usr/bin/python3.10 nyangabudget-env`
- [ ] Virtualenv activé : `workon nyangabudget-env`
- [ ] Python version vérifiée : `python --version` (3.10+)
- [ ] Dépendances installées : `pip install -r requirements.txt`
- [ ] Installation vérifiée : `pip list`

### Variables d'Environnement
- [ ] Fichier .env créé : `nano .env`
- [ ] SECRET_KEY générée : `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`
- [ ] SECRET_KEY ajoutée au .env
- [ ] DATABASE_URL configurée
- [ ] FLASK_ENV=production
- [ ] FLASK_DEBUG=0
- [ ] Fichier sauvegardé et permissions OK : `chmod 600 .env`

### Dossiers et Permissions
- [ ] Dossier data créé : `mkdir -p data`
- [ ] Dossier uploads créé : `mkdir -p uploads/vault uploads/heritage uploads/receipts`
- [ ] Permissions uploads : `chmod -R 755 uploads/`
- [ ] Permissions data : `chmod 755 data/`

---

## 🌐 Configuration Web App

### Création Web App
- [ ] Onglet "Web" ouvert dans PythonAnywhere
- [ ] "Add a new web app" cliqué
- [ ] "Manual configuration" sélectionné
- [ ] Python 3.10 choisi
- [ ] Web app créée

### Configuration WSGI
- [ ] Fichier WSGI ouvert (lien dans Web tab)
- [ ] Code WSGI remplacé par template du guide
- [ ] USERNAME remplacé partout dans le code
- [ ] Chemin projet correct : `/home/USERNAME/NyangaBudget`
- [ ] Chemin virtualenv correct : `/home/USERNAME/.virtualenvs/nyangabudget-env`
- [ ] Import `from app import app as application` correct
- [ ] `load_dotenv()` ajouté pour charger .env
- [ ] Fichier WSGI sauvegardé

### Chemins dans Web Tab
- [ ] Source code : `/home/USERNAME/NyangaBudget`
- [ ] Working directory : `/home/USERNAME/NyangaBudget`
- [ ] Virtualenv : `/home/USERNAME/.virtualenvs/nyangabudget-env`

### Fichiers Statiques
- [ ] Mapping `/static/` → `/home/USERNAME/NyangaBudget/static/`
- [ ] Mapping `/uploads/` → `/home/USERNAME/NyangaBudget/uploads/`

---

## 🗄️ Base de Données

### Initialisation SQLite
- [ ] Console Python ouverte : `python3` (avec workon actif)
- [ ] Commandes exécutées :
  ```python
  from app import app, db
  with app.app_context():
      db.create_all()
      print("Base de données créée !")
  exit()
  ```
- [ ] Fichier nyanga.db créé : `ls -lh data/`
- [ ] Permissions DB correctes : `chmod 644 data/nyanga.db`

### (Optionnel) Migration vers MySQL
- [ ] Base MySQL créée dans PythonAnywhere
- [ ] DATABASE_URL mise à jour dans .env
- [ ] Tables créées dans MySQL
- [ ] Données migrées depuis SQLite

---

## 🚀 Lancement

### Premier Démarrage
- [ ] Bouton "Reload" cliqué dans Web tab
- [ ] Attente 10 secondes pour le chargement
- [ ] URL ouverte : `https://USERNAME.pythonanywhere.com`
- [ ] Page d'accueil charge sans erreur

### Tests de Base
- [ ] Page d'accueil s'affiche
- [ ] CSS modernes chargés (pas de design cassé)
- [ ] Login accessible
- [ ] Inscription accessible
- [ ] Création du premier compte admin réussie
- [ ] Connexion avec nouveau compte fonctionne
- [ ] Dashboard s'affiche après login
- [ ] Navbar moderne visible
- [ ] Footer visible

---

## 🎨 Tests Fonctionnels

### Pages Principales
- [ ] 📊 Dashboard : stats et graphiques Plotly
- [ ] 💰 Revenus : création et liste
- [ ] 💸 Dépenses : création, filtres et liste
- [ ] 📂 Catégories : CRUD fonctionnel
- [ ] 🎯 Budgets : création et barres de progression
- [ ] 🏆 Objectifs : cartes premium et badges
- [ ] 📧 Notifications : centre avec badges priorité
- [ ] 🔔 Rappels : création et liste

### Pages Avancées
- [ ] 📷 Scan Reçu : drag & drop et OCR
- [ ] 🔐 Coffre-fort : upload chiffré AES-256
- [ ] 👨‍👩‍👧‍👦 Famille : gestion membres et QR codes
- [ ] 🏛️ Héritage : testament numérique
- [ ] 👤 Comptes : multi-comptes bancaires
- [ ] 📄 Rapports : génération PDF

### Design et UX
- [ ] 🌓 Dark mode fonctionne
- [ ] 💎 Glassmorphism visible sur cartes
- [ ] ✨ Animations CSS actives (hover, pulse, float)
- [ ] 📱 Responsive design (tester sur mobile)
- [ ] 🔍 Search modale navbar fonctionnelle
- [ ] 🎨 Gradients colorés visibles

### Uploads et Fichiers
- [ ] Upload fichier < 16MB fonctionne
- [ ] Preview images fonctionne
- [ ] Téléchargement fichiers fonctionne
- [ ] Suppression fichiers fonctionne
- [ ] Dossiers uploads accessibles

---

## 🔐 Tests Sécurité

### Authentification
- [ ] Login requis pour pages protégées
- [ ] Logout fonctionne
- [ ] Session expire après inactivité
- [ ] Rate limiting bloque tentatives répétées
- [ ] CSRF tokens présents dans formulaires

### Protection Données
- [ ] Fichiers vault chiffrés (AES-256)
- [ ] Mots de passe hashés en base
- [ ] SQLi protection (ORM SQLAlchemy)
- [ ] XSS protection (Jinja2 auto-escape)
- [ ] HTTPS actif (PythonAnywhere par défaut)

---

## 📊 Vérifications Performance

### Temps de Chargement
- [ ] Page d'accueil < 2s
- [ ] Dashboard < 3s (avec graphiques)
- [ ] Autres pages < 2s
- [ ] Images chargent rapidement

### Ressources
- [ ] Aucune erreur dans console navigateur (F12)
- [ ] CSS chargés sans 404
- [ ] JS chargés sans erreur
- [ ] Pas de warning dans console

### Logs
- [ ] Error log vide ou sans erreurs critiques
- [ ] Access log montre les requêtes
- [ ] Pas de 500 Internal Server Error

---

## 📝 Post-Déploiement

### Documentation
- [ ] URL production notée
- [ ] Identifiants admin sauvegardés (sécurisé)
- [ ] .env backupé (hors Git, sécurisé)
- [ ] Guide déploiement suivi et coché

### Monitoring
- [ ] Disk space vérifié (PythonAnywhere dashboard)
- [ ] CPU seconds vérifiés
- [ ] Quotas notés

### Backup
- [ ] Backup initial DB créé : `cp data/nyanga.db data/nyanga_backup_$(date +%Y%m%d).db`
- [ ] Dossier backups créé : `mkdir -p data/backups`
- [ ] Script backup documenté

### Communication
- [ ] Équipe informée du déploiement
- [ ] URL partagée
- [ ] Utilisateurs peuvent créer comptes
- [ ] Support préparé pour questions

---

## 🐛 En Cas de Problème

### App ne démarre pas
- [ ] Vérifier Error log : Web tab → Log files
- [ ] Vérifier chemins dans WSGI
- [ ] Vérifier virtualenv activé dans WSGI
- [ ] Tester import : `python3 -c "from app import app"`

### CSS ne charge pas
- [ ] Vérifier Static files mappings
- [ ] Vérifier permissions : `ls -la static/`
- [ ] Vider cache navigateur (Ctrl+Shift+R)
- [ ] Vérifier chemins dans templates

### DB erreurs
- [ ] Vérifier que nyanga.db existe
- [ ] Permissions : `chmod 644 data/nyanga.db`
- [ ] Recréer tables si nécessaire
- [ ] Vérifier DATABASE_URL dans .env

### Uploads échouent
- [ ] Créer dossiers uploads
- [ ] Permissions : `chmod -R 755 uploads/`
- [ ] Vérifier MAX_CONTENT_LENGTH
- [ ] Vérifier espace disque disponible

---

## ✅ Validation Finale

### Tests Complets Réussis
- [ ] Toutes les pages accessibles
- [ ] Tous les formulaires fonctionnent
- [ ] Tous les uploads fonctionnent
- [ ] Design moderne partout
- [ ] Dark mode opérationnel
- [ ] Mobile responsive OK
- [ ] Performance acceptable
- [ ] Sécurité validée

### Production Ready
- [ ] DEBUG = False
- [ ] HTTPS actif
- [ ] Logs propres
- [ ] Backup configuré
- [ ] Monitoring actif
- [ ] Documentation complète

---

## 🎉 Déploiement Réussi !

**URL Production** : `https://USERNAME.pythonanywhere.com`

**Prochaines Étapes** :
1. Créer utilisateurs de test
2. Former les utilisateurs finaux
3. Surveiller performance 24-48h
4. Optimiser si nécessaire
5. Planifier roadmap futures features

---

**Date de déploiement** : _______________  
**Déployé par** : _______________  
**Version** : NyangaBudget 2.0 (Post-Modernisation)

---

*Checklist version 1.0 - Janvier 2026*
