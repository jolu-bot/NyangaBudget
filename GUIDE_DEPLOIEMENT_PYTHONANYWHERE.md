# 🚀 Guide de Déploiement PythonAnywhere - NyangaBudget 2.0

## 📋 Prérequis

### Compte PythonAnywhere
- [ ] Compte créé sur [www.pythonanywhere.com](https://www.pythonanywhere.com)
- [ ] Plan : Gratuit (suffisant pour démarrer) ou Payant (recommandé pour production)

### Préparation Locale
- [x] Code modernisé et testé localement
- [x] Tous les commits pushés sur GitHub
- [x] Requirements.txt à jour
- [x] Variables d'environnement identifiées

---

## 🔧 Étape 1 : Configuration Initiale sur PythonAnywhere

### 1.1 Se connecter et ouvrir une console Bash

```bash
# Dans PythonAnywhere Dashboard > Consoles > Bash
```

### 1.2 Cloner le repository GitHub

```bash
# Cloner votre projet
git clone https://github.com/jolu-bot/NyangaBudget.git
cd NyangaBudget

# Vérifier que tout est là
ls -la
```

### 1.3 Créer l'environnement virtuel

```bash
# Créer virtualenv avec Python 3.10 (recommandé)
mkvirtualenv --python=/usr/bin/python3.10 nyangabudget-env

# Activer l'environnement
workon nyangabudget-env

# Vérifier la version Python
python --version
```

### 1.4 Installer les dépendances

```bash
# Installer toutes les dépendances
pip install -r requirements.txt

# Vérifier l'installation
pip list
```

---

## 🌐 Étape 2 : Configuration de l'Application Web

### 2.1 Créer une nouvelle Web App

1. Aller dans **Web** tab
2. Cliquer sur **Add a new web app**
3. Choisir **Manual configuration**
4. Sélectionner **Python 3.10**

### 2.2 Configurer le fichier WSGI

Cliquer sur le lien **WSGI configuration file** et remplacer tout le contenu par :

```python
# /var/www/VOTRE_USERNAME_pythonanywhere_com_wsgi.py

import sys
import os

# Ajouter le chemin de votre projet
path = '/home/VOTRE_USERNAME/NyangaBudget'
if path not in sys.path:
    sys.path.insert(0, path)

# Activer l'environnement virtuel
os.environ['VIRTUAL_ENV'] = '/home/VOTRE_USERNAME/.virtualenvs/nyangabudget-env'
activate_this = os.path.join(os.environ['VIRTUAL_ENV'], 'bin/activate_this.py')

# Pour Python 3.10+, utiliser exec au lieu d'execfile
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

# Importer l'application Flask
from app import app as application

# Configuration pour production
application.config['DEBUG'] = False
application.config['ENV'] = 'production'
```

**⚠️ Important** : Remplacer `VOTRE_USERNAME` par votre nom d'utilisateur PythonAnywhere !

### 2.3 Configurer les chemins dans Web tab

Dans l'onglet **Web**, configurer :

| Section | Valeur |
|---------|--------|
| **Source code** | `/home/VOTRE_USERNAME/NyangaBudget` |
| **Working directory** | `/home/VOTRE_USERNAME/NyangaBudget` |
| **Virtualenv** | `/home/VOTRE_USERNAME/.virtualenvs/nyangabudget-env` |

---

## 🔐 Étape 3 : Configuration des Variables d'Environnement

### 3.1 Créer le fichier .env (dans console Bash)

```bash
cd ~/NyangaBudget
nano .env
```

Ajouter le contenu suivant :

```bash
# SECRET_KEY : Générer une clé sécurisée
SECRET_KEY=votre-cle-super-secrete-generee-aleatoirement

# Base de données (SQLite par défaut)
DATABASE_URL=sqlite:///data/nyanga.db

# Configuration Flask
FLASK_ENV=production
FLASK_DEBUG=0

# Uploads
MAX_CONTENT_LENGTH=16777216

# OCR (optionnel)
OPENAI_API_KEY=votre-cle-openai-si-utilise

# Email (optionnel, pour notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=1
MAIL_USERNAME=votre-email@gmail.com
MAIL_PASSWORD=votre-mot-de-passe-app
```

**💡 Pour générer une SECRET_KEY sécurisée** :

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Sauvegarder : `Ctrl+O`, `Enter`, `Ctrl+X`

### 3.2 Charger les variables d'environnement dans WSGI

Modifier le fichier WSGI pour charger `.env` :

```python
# Ajouter au début du fichier WSGI
from dotenv import load_dotenv

# Charger les variables d'environnement
dotenv_path = os.path.join(path, '.env')
load_dotenv(dotenv_path)
```

---

## 📁 Étape 4 : Configuration des Fichiers Statiques

### 4.1 Dans l'onglet Web > Static files

Ajouter les mappages suivants :

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/VOTRE_USERNAME/NyangaBudget/static/` |
| `/uploads/` | `/home/VOTRE_USERNAME/NyangaBudget/uploads/` |

### 4.2 Créer les dossiers uploads

```bash
cd ~/NyangaBudget
mkdir -p uploads/vault uploads/heritage uploads/receipts
chmod 755 uploads
```

---

## 🗄️ Étape 5 : Initialisation de la Base de Données

### 5.1 Créer la base de données

```bash
cd ~/NyangaBudget
workon nyangabudget-env

# Lancer Python interactif
python3
```

Dans l'interpréteur Python :

```python
from app import app, db
with app.app_context():
    db.create_all()
    print("Base de données créée avec succès !")
exit()
```

### 5.2 Vérifier la base de données

```bash
ls -lh data/
# Vous devriez voir nyanga.db
```

---

## 🚀 Étape 6 : Lancement et Tests

### 6.1 Recharger l'application

Dans l'onglet **Web** :
- Cliquer sur le bouton vert **Reload VOTRE_USERNAME.pythonanywhere.com**
- Attendre quelques secondes

### 6.2 Tester l'application

1. Ouvrir : `https://VOTRE_USERNAME.pythonanywhere.com`
2. Vérifier que la page d'accueil s'affiche
3. Créer votre premier compte administrateur :
   - Cliquer sur "S'inscrire"
   - Remplir le formulaire d'inscription
   - Se connecter avec vos identifiants

### 6.3 Vérifier les logs en cas d'erreur

```bash
# Dans console Bash
cd ~/NyangaBudget
tail -f /var/log/VOTRE_USERNAME.pythonanywhere.com.error.log
```

Ou via l'onglet **Web** > **Log files** > **Error log**

---

## 🎨 Étape 7 : Vérifications Post-Déploiement

### Checklist Fonctionnelle

- [ ] ✅ Page d'accueil charge correctement
- [ ] ✅ Login fonctionne
- [ ] ✅ Dashboard s'affiche avec design moderne
- [ ] ✅ CSS modernes chargés (navbar-modern.css, forms-modern.css, dashboard-modern.css)
- [ ] ✅ Dark mode fonctionne
- [ ] ✅ Formulaires de création (revenus, dépenses) fonctionnent
- [ ] ✅ Upload de fichiers fonctionne (scan reçu, coffre-fort)
- [ ] ✅ Charts Plotly s'affichent
- [ ] ✅ Notifications s'affichent
- [ ] ✅ Mobile responsive fonctionne

### Checklist Performance

- [ ] ⚡ Temps de chargement < 3 secondes
- [ ] ⚡ CSS minifiés chargés
- [ ] ⚡ Images optimisées
- [ ] ⚡ Pas d'erreurs JavaScript console

### Checklist Sécurité

- [ ] 🔒 DEBUG = False en production
- [ ] 🔒 SECRET_KEY unique et sécurisée
- [ ] 🔒 CSRF protection active
- [ ] 🔒 HTTPS actif (automatique sur PythonAnywhere)
- [ ] 🔒 Rate limiting actif
- [ ] 🔒 Fichiers uploads sécurisés

---

## 🔄 Étape 8 : Mises à Jour Futures

### Mettre à jour le code

```bash
cd ~/NyangaBudget
workon nyangabudget-env

# Pull les dernières modifications
git pull origin main

# Installer nouvelles dépendances si nécessaire
pip install -r requirements.txt

# Recharger l'app
# Aller dans Web tab et cliquer sur Reload
```

### Migration de base de données

Si vous modifiez les modèles :

```bash
cd ~/NyangaBudget
workon nyangabudget-env

# Sauvegarder l'ancienne DB
cp data/nyanga.db data/nyanga.db.backup

# Recréer les tables (attention : perte de données !)
python3
```

```python
from app import app, db
with app.app_context():
    db.drop_all()
    db.create_all()
exit()
```

---

## 🛠️ Dépannage

### Problème : App ne démarre pas

**Solution** :
1. Vérifier les logs d'erreur
2. Vérifier que le virtualenv est activé dans WSGI
3. Vérifier les chemins dans Web tab
4. Tester localement : `python app.py`

### Problème : CSS ne charge pas

**Solution** :
1. Vérifier les mappages Static files
2. Vérifier les permissions : `chmod -R 755 static/`
3. Vider le cache navigateur (Ctrl+Shift+R)
4. Vérifier dans Error log

### Problème : Upload de fichiers échoue

**Solution** :
1. Créer les dossiers : `mkdir -p uploads/vault uploads/heritage uploads/receipts`
2. Permissions : `chmod -R 755 uploads/`
3. Vérifier `MAX_CONTENT_LENGTH` dans config
4. Vérifier l'espace disque disponible

### Problème : Base de données corrompue

**Solution** :
```bash
# Sauvegarder
cp data/nyanga.db data/nyanga.db.backup

# Vérifier intégrité
sqlite3 data/nyanga.db "PRAGMA integrity_check;"

# Si corruption, recréer
python3
from app import app, db
with app.app_context():
    db.create_all()
```

---

## 📊 Monitoring et Maintenance

### Surveiller les ressources

Dans **Dashboard** PythonAnywhere :
- CPU seconds : Éviter de dépasser la limite gratuite
- Disk space : Surveiller l'espace utilisé
- Database size : Optimiser si nécessaire

### Optimisations Recommandées

1. **Minifier CSS/JS** avant déploiement
2. **Compresser images** dans `/static/images/`
3. **Activer cache Flask** pour requêtes fréquentes
4. **Index database** sur colonnes recherchées souvent
5. **Paginer** listes longues (dépenses, revenus)

### Sauvegardes Régulières

```bash
# Script de backup automatique
cd ~/NyangaBudget
cp data/nyanga.db data/backups/nyanga_$(date +%Y%m%d).db
```

Ajouter au crontab PythonAnywhere (si compte payant) :
```bash
# Backup quotidien à 3h du matin
0 3 * * * cd ~/NyangaBudget && cp data/nyanga.db data/backups/nyanga_$(date +\%Y\%m\%d).db
```

---

## 🌟 Optimisations Avancées (Optionnel)

### 1. Utiliser MySQL au lieu de SQLite

Si compte payant PythonAnywhere :

```python
# Dans .env
DATABASE_URL=mysql+pymysql://USERNAME:PASSWORD@USERNAME.mysql.pythonanywhere-services.com/USERNAME$nyangabudget
```

### 2. Activer Compression Gzip

Ajouter au WSGI :

```python
from flask_compress import Compress
Compress(application)
```

### 3. CDN pour fichiers statiques

Héberger CSS/JS sur CDN externe si trafic élevé.

### 4. Redis pour cache (compte payant)

```python
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://...'
```

---

## 📞 Support

### Ressources PythonAnywhere
- [Documentation officielle](https://help.pythonanywhere.com/)
- [Forums](https://www.pythonanywhere.com/forums/)
- [Contact support](https://www.pythonanywhere.com/support/)

### GitHub Issues
- [NyangaBudget Issues](https://github.com/jolu-bot/NyangaBudget/issues)

---

## ✅ Checklist Finale

- [ ] Application déployée et accessible
- [ ] Compte admin fonctionne
- [ ] Toutes les pages chargent
- [ ] Design moderne visible
- [ ] Uploads fonctionnent
- [ ] Base de données initialisée
- [ ] Variables d'environnement configurées
- [ ] Logs vérifiés (pas d'erreurs)
- [ ] Tests fonctionnels passés
- [ ] Performance acceptable
- [ ] Backup automatique configuré

---

**🎉 Félicitations ! Votre application NyangaBudget 2.0 est maintenant en ligne !**

**URL Production** : `https://VOTRE_USERNAME.pythonanywhere.com`

---

*Guide créé le 14 janvier 2026*
*Version : 1.0*
*Application : NyangaBudget 2.0 (Post-Modernisation)*
