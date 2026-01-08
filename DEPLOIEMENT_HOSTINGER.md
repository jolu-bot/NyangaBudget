# 🌟 Guide Complet de Déploiement sur Hostinger - NyangaBudget 2.0

**Plateforme Familiale de Gestion Financière & Patrimoniale**

**Date:** 26 Décembre 2025  
**Durée estimée:** 30-45 minutes  
**Niveau:** Intermédiaire

---

## 📋 Table des Matières

1. [Vue d'ensemble du Projet](#-vue-densemble-du-projet)
2. [Architecture Technique](#-architecture-technique)
3. [État Actuel du Projet](#-état-actuel-du-projet)
4. [Choix d'Hébergement Hostinger](#-choix-dhébergement-hostinger)
5. [Prérequis et Préparation](#-prérequis-et-préparation)
6. [Configuration de la Base de Données MySQL Hostinger](#-configuration-de-la-base-de-données-mysql-hostinger)
7. [Déploiement via FTP/SSH](#-déploiement-via-ftpssh)
8. [Configuration Environnement Production](#-configuration-environnement-production)
9. [Tests Post-Déploiement](#-tests-post-déploiement)
10. [Maintenance et Monitoring](#-maintenance-et-monitoring)
11. [Optimisations Recommandées](#-optimisations-recommandées)
12. [Dépannage](#-dépannage)

---

## 🎯 Vue d'ensemble du Projet

### Informations Générales

| Élément | Détail |
|---------|--------|
| **Nom** | NyangaBudget 2.0 |
| **Type** | Application Web Flask (Python) |
| **Version Python** | 3.11.7 |
| **Framework** | Flask 3.0.0+ |
| **Base de données actuelle** | SQLite (développement) |
| **Base de données cible** | MySQL/PostgreSQL (production) |
| **Taille du projet** | ~3,357 lignes de code |
| **Templates HTML** | 18 fichiers |
| **Assets** | 2.9 MB (logos) |

### Fonctionnalités Principales (17)

#### 🏦 Financier de Base (7)
1. ✅ Gestion des dépenses avec catégories colorées
2. ✅ Gestion des revenus
3. ✅ Budgets mensuels avec alertes
4. ✅ Dashboard interactif (graphiques Plotly)
5. ✅ Exports PDF & CSV professionnels
6. ✅ Authentification sécurisée (Flask-Login)
7. ✅ Catégories personnalisables (icônes Bootstrap)

#### 🚀 Fonctionnalités Révolutionnaires (10)
8. ✅ **Multi-Comptes Bancaires** avec transferts hash SHA-256
9. ✅ **Coffre-Fort Crypté** AES-256 militaire
10. ✅ **Héritage & Testament Numérique**
11. ✅ **Gestion Familiale** avec QR codes d'invitation
12. ✅ **IA Prédictive** - Score de santé financière (0-100)
13. ✅ **Notifications Temps Réel**
14. ✅ **Rappels Récurrents** (hebdo/mensuel/annuel)
15. ✅ **Objectifs d'Épargne** collaboratifs
16. ✅ **Dark Mode** avec localStorage
17. ✅ **API REST** pour intégrations externes

---

## 🏗️ Architecture Technique

### Stack Technologique

```
Frontend:
├── HTML5 + Jinja2 Templates
├── Bootstrap 5.3 (UI/UX)
├── JavaScript Vanilla (dark mode, voice assistant)
├── Chart.js / Plotly.js (graphiques interactifs)
└── PWA (Progressive Web App) - manifest.json

Backend:
├── Flask 3.0.0+ (framework web)
├── Flask-SQLAlchemy (ORM)
├── Flask-Login (authentification)
├── Flask-Limiter (protection brute force)
├── Flask-WTF (CSRF protection)
├── Flask-Caching (optimisation)
└── Gunicorn (serveur WSGI production)

Sécurité:
├── CSRF Protection
├── Rate Limiting (200/jour, 50/heure)
├── Cryptographie AES-256 (coffre-fort)
├── Hash SHA-256 (transferts bancaires)
└── PBKDF2 (dérivation de clés)

Base de Données:
├── SQLAlchemy ORM
├── SQLite (développement local)
├── PostgreSQL (Render - cloud)
└── MySQL (Hostinger - cible)

Dépendances Clés:
├── cryptography>=41.0.0 (cryptage)
├── qrcode>=7.4.2 (QR codes famille)
├── plotly>=5.18.0 (graphiques)
├── reportlab>=4.0.7 (exports PDF)
├── scikit-learn>=1.3.0 (IA scoring)
└── psycopg2-binary>=2.9.9 (PostgreSQL)
```

### Structure des Fichiers

```
NyangaBudget/
├── app.py                    (3,357 lignes - cœur de l'application)
├── requirements.txt          (18 dépendances)
├── Procfile                  (Gunicorn pour Render)
├── runtime.txt               (Python 3.11.7)
├── render.yaml               (Configuration Render)
│
├── 📚 Documentation (5 fichiers)
│   ├── README.md             (13 KB)
│   ├── STATUS_FINAL.md       (Statut complet)
│   ├── DEPLOIEMENT_RENDER.md (Guide Render)
│   ├── INTEGRATION_LOGOS.md  (Guide logos)
│   └── DEPLOIEMENT_HOSTINGER.md (ce fichier)
│
├── 📂 data/
│   └── nyanga_v2.db          (SQLite - dev local)
│
├── 📂 uploads/
│   ├── vault/                (Documents cryptés)
│   ├── heritage/             (Testaments/biens)
│   └── receipts/             (Reçus scannés)
│
├── 📂 static/
│   ├── style.css             (Styles + dark mode)
│   ├── darkmode.js           (Script dark mode)
│   ├── voice-assistant.js    (Assistant vocal)
│   ├── manifest.webmanifest  (PWA)
│   ├── service-worker.js     (PWA)
│   └── images/
│       ├── logo.png          (958 KB)
│       └── logo-white.png    (2.0 MB)
│
└── 📂 templates/ (18 fichiers HTML)
    ├── base.html             (Template principal)
    ├── login.html
    ├── register.html
    ├── dashboard.html
    ├── comptes.html
    ├── coffre_fort.html
    ├── heritage.html
    ├── famille.html
    ├── rappels.html
    ├── objectifs.html
    └── ...
```

---

## 📊 État Actuel du Projet

### ✅ Ce qui est Terminé (100%)

1. **Développement** - Toutes les 17 fonctionnalités implémentées
2. **Tests Locaux** - Application testée sous Windows avec SQLite
3. **Interface UI/UX** - Design responsive avec Bootstrap 5
4. **Sécurité** - CSRF, Rate Limiting, Cryptage AES-256
5. **Documentation** - 5 guides complets (48 KB)
6. **Logos** - Intégrés dans 6 emplacements (navbar, login, footer, PWA, etc.)
7. **Configuration Render** - Prêt pour PostgreSQL (render.yaml)
8. **Compte Admin** - admin@nyanga.cm / admin123

### 🔄 Ce qui Nécessite une Adaptation pour Hostinger

1. **Base de données** - Passer de SQLite à MySQL Hostinger
2. **Configuration serveur** - Adapter pour Apache/LiteSpeed + Python
3. **Variables d'environnement** - Configurer SECRET_KEY, DB_URL, etc.
4. **Upload de fichiers** - Configurer permissions et chemins absolus
5. **Déploiement** - Via FTP/SSH au lieu de Git/CI-CD
6. **Serveur WSGI** - Configuration Gunicorn ou Passenger WSGI

### 📈 Statistiques du Projet

| Métrique | Valeur |
|----------|--------|
| **Lignes de code Python** | 3,357 |
| **Routes Flask** | 52 |
| **Modèles de données** | 17 tables |
| **Templates HTML** | 18 |
| **Fichiers JavaScript** | 3 |
| **Fichiers CSS** | 1 (style.css) |
| **Assets (images)** | 2.9 MB |
| **Documentation** | 48 KB (5 fichiers) |
| **Dépendances Python** | 18 packages |

---

## 🏅 Choix d'Hébergement Hostinger

### Pourquoi Hostinger ?

| Critère | Hostinger | Render | Heroku |
|---------|-----------|--------|--------|
| **Prix** | 2-8€/mois | Gratuit + 7$/mois | Payant |
| **Base de données** | MySQL incluse | PostgreSQL | PostgreSQL |
| **Support Python** | ✅ Via SSH | ✅ Natif | ✅ Natif |
| **FTP/SSH** | ✅ Les deux | ❌ Git only | ❌ Git only |
| **Panneau contrôle** | hPanel intuitif | Dashboard web | Dashboard web |
| **Domaine personnalisé** | Inclus | Gratuit | Payant |
| **Espace disque** | 50-200 GB | Limité | Limité |
| **Trafic** | Illimité | Limité | Limité |
| **Email inclus** | ✅ Oui | ❌ Non | ❌ Non |

### Plans Hostinger Recommandés

#### 🥇 **Premium Hosting** (Recommandé)
- **Prix:** ~3.99€/mois
- **Stockage:** 100 GB SSD
- **Base de données:** MySQL illimitées
- **Domaines:** 100
- **Emails:** 100 comptes
- **SSL:** Gratuit
- **Backups:** Hebdomadaires

#### 🥈 **Business Hosting** (Alternative Pro)
- **Prix:** ~7.99€/mois
- **Stockage:** 200 GB SSD
- **Base de données:** MySQL illimitées
- **Performance:** 2x plus rapide
- **Backups:** Quotidiens
- **CDN:** Cloudflare inclus

### Fonctionnalités Clés Hostinger

✅ **MySQL** - Base de données incluse  
✅ **Python Support** - Via SSH + virtualenv  
✅ **SSH Access** - Installation de packages Python  
✅ **FTP/SFTP** - Upload facile via FileZilla  
✅ **hPanel** - Interface graphique intuitive  
✅ **Auto-installer** - Softaculous (WordPress, etc.)  
✅ **SSL Gratuit** - Let's Encrypt automatique  
✅ **Email** - Adresses @votredomaine.com  
✅ **Support 24/7** - Chat en direct  

---

## 🛠️ Prérequis et Préparation

### 1. Compte Hostinger

Assurez-vous d'avoir :

- [ ] Un compte Hostinger actif (Premium ou Business)
- [ ] Un domaine configuré (ex: nyangabudget.com)
- [ ] Accès au hPanel (panneau de contrôle)
- [ ] Identifiants FTP/SSH disponibles

### 2. Logiciels Requis

Sur votre machine Windows :

```powershell
# Vérifier Python
python --version  # Devrait afficher 3.11.x

# Vérifier Git
git --version

# Installer FileZilla (client FTP)
# Télécharger sur: https://filezilla-project.org/
```

### 3. Préparation du Projet

#### A. Créer un Fichier de Configuration Hostinger

Créez `hostinger_config.py` :

```python
# hostinger_config.py - Configuration spécifique Hostinger

import os

class HostingerConfig:
    """Configuration pour déploiement Hostinger avec MySQL"""
    
    # Base de données MySQL Hostinger
    # Format: mysql://username:password@hostname/database_name
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'u123456789_nyanga')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'VotreMotDePasseMySQL')
    DB_NAME = os.environ.get('DB_NAME', 'u123456789_nyangabudget')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    # Clés de sécurité (générer des valeurs uniques)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'votre-cle-secrete-unique-32-caracteres')
    MASTER_ENCRYPTION_KEY = os.environ.get('MASTER_ENCRYPTION_KEY', 'votre-cle-cryptage-32-caracteres')
    
    # Chemins absolus pour Hostinger
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    VAULT_FOLDER = os.path.join(UPLOAD_FOLDER, 'vault')
    HERITAGE_FOLDER = os.path.join(UPLOAD_FOLDER, 'heritage')
    RECEIPTS_FOLDER = os.path.join(UPLOAD_FOLDER, 'receipts')
    
    # Environnement de production
    FLASK_ENV = 'production'
    DEBUG = False
```

#### B. Mettre à Jour `requirements.txt`

Ajoutez le driver MySQL :

```txt
# Ajouter à requirements.txt
PyMySQL>=1.1.0
```

Le fichier complet devient :

```txt
Flask>=3.0.0
Flask-SQLAlchemy>=3.1.1
Flask-Login>=0.6.3
Flask-Limiter>=3.5.0
Flask-WTF>=1.2.1
Flask-Caching>=2.1.0
plotly>=5.18.0
reportlab>=4.0.7
python-dateutil>=2.8.2
werkzeug>=3.0.0
cryptography>=41.0.0
qrcode>=7.4.2
Pillow>=10.0.0
scikit-learn>=1.3.0
numpy>=1.24.0
gunicorn>=21.2.0
openpyxl>=3.1.0
psycopg2-binary>=2.9.9
PyMySQL>=1.1.0
```

#### C. Créer `.htaccess` pour Hostinger

```apache
# .htaccess - Configuration Apache pour Flask

<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    
    # Rediriger tout vers l'application Flask
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ passenger_wsgi.py [QSA,L]
</IfModule>

# Sécurité
<Files "passenger_wsgi.py">
    Order allow,deny
    Allow from all
</Files>

# Protéger les fichiers sensibles
<FilesMatch "\.(db|env|log|ini)$">
    Order allow,deny
    Deny from all
</FilesMatch>
```

#### D. Créer `passenger_wsgi.py` (Serveur WSGI Hostinger)

```python
# passenger_wsgi.py - Point d'entrée WSGI pour Hostinger

import sys
import os

# Chemin vers votre application
INTERP = os.path.join(os.environ['HOME'], 'nyangabudget_venv', 'bin', 'python3')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Ajouter le répertoire de l'application au path
sys.path.insert(0, os.path.dirname(__file__))

# Importer l'application Flask
from app import app as application

# Variable nécessaire pour Passenger
if __name__ == "__main__":
    application.run()
```

#### E. Créer Script de Déploiement

Créez `deploy_hostinger.py` :

```python
# deploy_hostinger.py - Script de déploiement automatique via FTP

import ftplib
import os
from pathlib import Path

FTP_HOST = 'ftp.votredomaine.com'
FTP_USER = 'votreuser@votredomaine.com'
FTP_PASS = 'votre_mot_de_passe_ftp'
FTP_REMOTE_DIR = '/public_html/nyangabudget'

def upload_directory(ftp, local_dir, remote_dir):
    """Upload récursif d'un répertoire via FTP"""
    for item in Path(local_dir).iterdir():
        if item.is_file():
            # Ignorer les fichiers inutiles
            if item.suffix in ['.pyc', '.db', '.log'] or item.name in ['.git', '__pycache__']:
                continue
            
            print(f"Upload: {item.name}")
            with open(item, 'rb') as file:
                ftp.storbinary(f'STOR {remote_dir}/{item.name}', file)
        
        elif item.is_dir():
            # Créer le répertoire distant
            try:
                ftp.mkd(f'{remote_dir}/{item.name}')
            except:
                pass  # Répertoire existe déjà
            
            # Upload récursif
            upload_directory(ftp, item, f'{remote_dir}/{item.name}')

def deploy():
    """Déploiement complet sur Hostinger"""
    print("=== Déploiement NyangaBudget sur Hostinger ===\n")
    
    # Connexion FTP
    print(f"Connexion à {FTP_HOST}...")
    ftp = ftplib.FTP(FTP_HOST)
    ftp.login(FTP_USER, FTP_PASS)
    
    # Créer le répertoire racine
    try:
        ftp.mkd(FTP_REMOTE_DIR)
    except:
        pass
    
    ftp.cwd(FTP_REMOTE_DIR)
    
    # Upload des fichiers
    print("\nUpload des fichiers...")
    upload_directory(ftp, '.', FTP_REMOTE_DIR)
    
    print("\n✅ Déploiement terminé!")
    print(f"Application disponible sur: https://votredomaine.com/nyangabudget")
    
    ftp.quit()

if __name__ == '__main__':
    deploy()
```

---

## 🗄️ Configuration de la Base de Données MySQL Hostinger

### Étape 1: Créer la Base de Données MySQL

1. **Connectez-vous à hPanel Hostinger**
   - URL: https://hpanel.hostinger.com
   - Email + mot de passe

2. **Aller dans "Databases" > "MySQL Databases"**

3. **Créer une nouvelle base de données**
   ```
   Nom: u123456789_nyangabudget
   (Hostinger ajoute automatiquement le préfixe u123456789_)
   ```

4. **Créer un utilisateur MySQL**
   ```
   Utilisateur: u123456789_nyanga
   Mot de passe: [Générer un mot de passe fort]
   ```

5. **Associer l'utilisateur à la base**
   - Sélectionner l'utilisateur créé
   - Cocher "Tous les privilèges"
   - Cliquer sur "Ajouter"

6. **Noter les informations de connexion**
   ```
   Hôte: localhost (ou mysql.votredomaine.com)
   Base: u123456789_nyangabudget
   Utilisateur: u123456789_nyanga
   Mot de passe: [votre mot de passe]
   Port: 3306 (par défaut)
   ```

### Étape 2: Tester la Connexion MySQL

Via hPanel > phpMyAdmin :

1. Cliquer sur "Manage" à côté de la base créée
2. phpMyAdmin s'ouvre automatiquement
3. Vérifier que vous voyez la base `u123456789_nyangabudget`

### Étape 3: Migrer les Données (si nécessaire)

Si vous avez déjà des données dans SQLite :

```powershell
# Sur votre machine locale

# 1. Exporter la base SQLite
sqlite3 data/nyanga_v2.db .dump > nyanga_backup.sql

# 2. Convertir SQLite vers MySQL (manuellement)
# - Remplacer AUTOINCREMENT par AUTO_INCREMENT
# - Remplacer les types de données (TEXT -> VARCHAR, etc.)

# 3. Importer via phpMyAdmin
# - Aller dans phpMyAdmin Hostinger
# - Sélectionner la base u123456789_nyangabudget
# - Cliquer sur "Importer"
# - Charger nyanga_backup.sql (adapté pour MySQL)
```

**Alternative:** Laisser Flask recréer les tables automatiquement :

```python
# Dans app.py - La fonction init_db() créera les tables
# Pas besoin de migration si c'est un nouveau déploiement
```

### Étape 4: Adapter `app.py` pour MySQL

Modifier la section de configuration de la base de données :

```python
# Dans app.py (ligne ~75)

DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Format universel (PostgreSQL ou MySQL)
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    print(f"[OK] Base de données externe (Production)")
    
elif os.environ.get('DB_HOST'):  # Configuration MySQL Hostinger
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'u123456789_nyanga')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
    DB_NAME = os.environ.get('DB_NAME', 'u123456789_nyangabudget')
    
    # Driver PyMySQL pour MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    print(f"[OK] MySQL Hostinger configuré")
    
else:
    # Développement local: SQLite
    db_path = os.path.join(data_folder, 'nyanga_v2.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    print(f"[OK] SQLite local")
```

---

## 🚀 Déploiement via FTP/SSH

### Méthode 1: Upload FTP (FileZilla) - Plus Simple

#### Étape 1: Configurer FileZilla

1. **Télécharger et installer FileZilla Client**
   - https://filezilla-project.org/

2. **Obtenir les identifiants FTP Hostinger**
   - hPanel > "FTP Accounts"
   - Noter: Hôte, Utilisateur, Mot de passe, Port

3. **Configurer une connexion dans FileZilla**
   ```
   Hôte: ftp.votredomaine.com
   Utilisateur: votreuser@votredomaine.com
   Mot de passe: [votre mot de passe FTP]
   Port: 21
   ```

4. **Se connecter**

#### Étape 2: Préparer les Fichiers Localement

```powershell
# Dans votre dossier NyangaBudget

# 1. Créer un dossier de déploiement
mkdir deploy
cd deploy

# 2. Copier tous les fichiers nécessaires
# (NE PAS inclure: .venv, data/, __pycache__, .git)
```

Fichiers à inclure :

```
✅ app.py
✅ passenger_wsgi.py (nouveau)
✅ .htaccess (nouveau)
✅ requirements.txt
✅ static/ (tout le dossier)
✅ templates/ (tout le dossier)
✅ uploads/ (créer les dossiers vides)

❌ .venv/ (NE PAS inclure)
❌ data/nyanga_v2.db (NE PAS inclure)
❌ __pycache__/ (NE PAS inclure)
❌ .git/ (NE PAS inclure)
```

#### Étape 3: Upload via FileZilla

1. **Panneau gauche** (local): Naviguer vers votre dossier `deploy`
2. **Panneau droit** (serveur): Aller dans `/public_html/`
3. **Créer un dossier** `nyangabudget` sur le serveur
4. **Sélectionner tous les fichiers** dans le panneau gauche
5. **Glisser-déposer** vers le panneau droit
6. **Attendre la fin du transfert** (~5-10 minutes selon connexion)

#### Étape 4: Créer les Dossiers Manquants

Via FileZilla, créer :

```
/public_html/nyangabudget/uploads/
/public_html/nyangabudget/uploads/vault/
/public_html/nyangabudget/uploads/heritage/
/public_html/nyangabudget/uploads/receipts/
/public_html/nyangabudget/data/ (optionnel - MySQL)
```

### Méthode 2: Upload SSH + Git - Plus Professionnel

#### Étape 1: Connexion SSH

```powershell
# Obtenir les identifiants SSH depuis hPanel > Advanced > SSH Access

# Se connecter via PowerShell ou PuTTY
ssh u123456789@votredomaine.com
# Entrer le mot de passe SSH
```

#### Étape 2: Installation de Python et Virtualenv

```bash
# Une fois connecté en SSH

# Vérifier Python (généralement déjà installé)
python3 --version

# Installer pip si nécessaire
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py --user

# Créer un environnement virtuel
cd ~/public_html
python3 -m venv nyangabudget_venv

# Activer l'environnement
source nyangabudget_venv/bin/activate
```

#### Étape 3: Cloner le Projet depuis Git

```bash
# Si votre projet est sur GitHub
cd ~/public_html
git clone https://github.com/jolu-bot/NyangaBudget.git nyangabudget

# Ou bien upload via FTP puis:
cd ~/public_html/nyangabudget
```

#### Étape 4: Installer les Dépendances

```bash
# Activer le virtualenv
source ~/nyangabudget_venv/bin/activate

# Installer les packages
cd ~/public_html/nyangabudget
pip install -r requirements.txt

# Vérifier l'installation
pip list
```

#### Étape 5: Configurer les Variables d'Environnement

```bash
# Créer un fichier .env (ne sera pas exposé publiquement)
nano .env
```

Contenu du fichier `.env` :

```bash
# .env - Variables d'environnement production

FLASK_ENV=production
DEBUG=False

# Base de données MySQL
DB_HOST=localhost
DB_USER=u123456789_nyanga
DB_PASSWORD=VotreMotDePasseMySQL
DB_NAME=u123456789_nyangabudget

# Clés de sécurité (générer des valeurs uniques)
SECRET_KEY=nyanga-prod-secret-key-32-chars-minimum-here
MASTER_ENCRYPTION_KEY=nyanga-encryption-key-32-chars-here

# Optionnel: Redis pour cache (si disponible)
# REDIS_URL=redis://localhost:6379/0
```

**Générer des clés sécurisées** :

```python
# Sur votre machine locale
python -c "import secrets; print(secrets.token_urlsafe(32))"
# Copier le résultat dans .env
```

#### Étape 6: Tester l'Application

```bash
# Initialiser la base de données
python3 app.py
# Vérifier qu'il n'y a pas d'erreurs

# Sortir avec Ctrl+C
```

---

## ⚙️ Configuration Environnement Production

### 1. Configurer Passenger WSGI (Hostinger)

Hostinger utilise **Phusion Passenger** pour exécuter les applications Python.

#### A. Vérifier `passenger_wsgi.py`

Assurez-vous que ce fichier est à la racine :

```python
# passenger_wsgi.py

import sys
import os

# Chemin vers l'environnement virtuel Python
INTERP = os.path.join(os.environ['HOME'], 'nyangabudget_venv', 'bin', 'python3')

if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Ajouter le répertoire de l'application au PYTHONPATH
sys.path.insert(0, os.path.dirname(__file__))

# Charger les variables d'environnement depuis .env
from dotenv import load_dotenv
load_dotenv()

# Importer l'application Flask
from app import app as application

# Point d'entrée WSGI
if __name__ == "__main__":
    application.run()
```

**Installer python-dotenv** :

```bash
pip install python-dotenv
```

Ajouter à `requirements.txt` :

```txt
python-dotenv>=1.0.0
```

#### B. Créer `.htaccess` pour Apache

```apache
# .htaccess - Redirection vers Passenger WSGI

PassengerEnabled On
PassengerAppRoot /home/u123456789/public_html/nyangabudget
PassengerStartupFile passenger_wsgi.py
PassengerPython /home/u123456789/nyangabudget_venv/bin/python3

# Rediriger tout le trafic vers l'application
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteBase /
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ passenger_wsgi.py [QSA,L]
</IfModule>

# Autoriser l'accès aux fichiers statiques
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot|ico|pdf)$">
    Allow from all
</FilesMatch>

# Protéger les fichiers sensibles
<FilesMatch "\.(db|env|log|ini|py)$">
    Order allow,deny
    Deny from all
</FilesMatch>

# Exceptions pour passenger_wsgi.py
<Files "passenger_wsgi.py">
    Order allow,deny
    Allow from all
</Files>
```

#### C. Redémarrer l'Application

```bash
# Via SSH
cd ~/public_html/nyangabudget
touch tmp/restart.txt  # Passenger redémarre l'application
```

Ou via hPanel :

- "Advanced" > "Passenger Python"
- Cliquer sur "Restart Application"

### 2. Configurer les Permissions de Fichiers

```bash
# Via SSH

# Donner les bonnes permissions
cd ~/public_html/nyangabudget

# Répertoires (755)
find . -type d -exec chmod 755 {} \;

# Fichiers (644)
find . -type f -exec chmod 644 {} \;

# Dossiers d'upload (775 pour écriture)
chmod -R 775 uploads/
chmod -R 775 data/ (si utilisé)

# Fichiers sensibles (600)
chmod 600 .env
```

### 3. Configurer SSL (HTTPS)

1. **Via hPanel > SSL**
2. **Activer Let's Encrypt SSL** (gratuit)
3. **Forcer HTTPS** :

Ajouter en haut de `.htaccess` :

```apache
# Forcer HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

### 4. Configurer le Domaine/Sous-domaine

#### Option 1: Sous-domaine dédié

1. **hPanel > "Domains" > "Subdomains"**
2. **Créer** : `budget.votredomaine.com`
3. **Document Root** : `/public_html/nyangabudget`

#### Option 2: Domaine principal

1. **hPanel > "Domains" > "Manage"**
2. **Pointer** le document root vers `/public_html/nyangabudget`

---

## ✅ Tests Post-Déploiement

### 1. Vérifications Basiques

#### A. Tester l'Accès à l'Application

```
https://votredomaine.com/nyangabudget
ou
https://budget.votredomaine.com
```

**Attendu:** Page de connexion avec logo

#### B. Vérifier les Logs

```bash
# Via SSH
cd ~/public_html/nyangabudget
cat tmp/passenger.log
cat tmp/error.log (si existe)
```

Ou via hPanel > "Files" > "File Manager" > Voir les logs

#### C. Tester la Connexion

```
Email: admin@nyanga.cm
Mot de passe: admin123
```

**Attendu:** Redirection vers le dashboard

### 2. Tests Fonctionnels

#### Checklist Complète

- [ ] **Authentification**
  - [ ] Connexion admin@nyanga.cm
  - [ ] Création d'un nouveau compte
  - [ ] Déconnexion

- [ ] **Dashboard**
  - [ ] Affichage des graphiques Plotly
  - [ ] Chargement des statistiques
  - [ ] Pas d'erreurs JavaScript (F12)

- [ ] **Dépenses & Revenus**
  - [ ] Ajouter une dépense
  - [ ] Ajouter un revenu
  - [ ] Voir la liste

- [ ] **Multi-Comptes**
  - [ ] Créer un compte bancaire
  - [ ] Effectuer un transfert
  - [ ] Vérifier le solde global

- [ ] **Coffre-Fort**
  - [ ] Ajouter un document
  - [ ] Upload un fichier PDF
  - [ ] Décrypter et visualiser

- [ ] **Famille**
  - [ ] Créer une famille
  - [ ] Générer un QR code
  - [ ] Télécharger le QR code

- [ ] **Rappels & Objectifs**
  - [ ] Créer un rappel mensuel
  - [ ] Créer un objectif d'épargne
  - [ ] Contribuer à l'objectif

- [ ] **Exports**
  - [ ] Export CSV
  - [ ] Export PDF
  - [ ] Téléchargement réussi

- [ ] **Notifications**
  - [ ] Badge de compteur visible
  - [ ] Cliquer sur une notification
  - [ ] Marquer comme lue

- [ ] **Score IA**
  - [ ] Cliquer sur le bouton ❤️
  - [ ] Voir le score (0-100)
  - [ ] Lire les suggestions

- [ ] **Dark Mode**
  - [ ] Activer le dark mode
  - [ ] Vérifier la persistance (recharger la page)
  - [ ] Désactiver

### 3. Tests de Performance

#### A. Temps de Chargement

```bash
# Via curl (depuis SSH ou local)
curl -w "Temps total: %{time_total}s\n" -o /dev/null -s https://votredomaine.com/nyangabudget
```

**Objectif:** < 3 secondes

#### B. Tester sous Charge

Utiliser un outil comme **Apache Bench** :

```bash
# 100 requêtes, 10 concurrentes
ab -n 100 -c 10 https://votredomget.com/nyangabudget/
```

**Objectif:** Pas d'erreurs 500

#### C. Vérifier la Consommation Mémoire

```bash
# Via SSH
top -u u123456789
# Regarder le processus Python (WSGI)
```

**Objectif:** < 500 MB RAM

### 4. Tests de Sécurité

#### A. SSL/TLS

```bash
# Vérifier le certificat SSL
curl -I https://votredomaine.com/nyangabudget
```

**Attendu:** `200 OK` + `Strict-Transport-Security` header

#### B. CSRF Protection

- Essayer de soumettre un formulaire sans token CSRF
- **Attendu:** Erreur 400 Bad Request

#### C. Rate Limiting

- Faire 60 requêtes en 1 minute sur `/login`
- **Attendu:** Erreur 429 Too Many Requests

#### D. Upload de Fichiers

- Essayer d'uploader un fichier `.exe` dans le coffre-fort
- **Attendu:** Rejeté (extension non autorisée)

---

## 🔧 Maintenance et Monitoring

### 1. Logs et Surveillance

#### A. Activer les Logs Flask

Modifier `app.py` :

```python
# Après la création de l'app

if app.config.get('FLASK_ENV') == 'production':
    import logging
    from logging.handlers import RotatingFileHandler
    
    # Créer le dossier logs
    log_dir = os.path.join(BASE_DIR, 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Handler avec rotation (10 MB max)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, 'nyanga.log'),
        maxBytes=10240000,
        backupCount=10
    )
    
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('NyangaBudget startup')
```

#### B. Consulter les Logs

```bash
# Via SSH
cd ~/public_html/nyangabudget/logs
tail -f nyanga.log  # Suivi en temps réel
```

Ou via hPanel > File Manager > logs/

#### C. Monitoring avec UptimeRobot (Gratuit)

1. S'inscrire sur **uptimerobot.com** (gratuit)
2. Ajouter un monitor :
   ```
   Type: HTTP(S)
   URL: https://votredomaine.com/nyangabudget/login
   Intervalle: 5 minutes
   ```
3. Configurer les alertes par email

### 2. Backups Automatiques

#### A. Backup de la Base de Données MySQL

Via hPanel :

1. **"Databases" > "MySQL Databases"**
2. Cliquer sur **"Manage"**
3. **"Export"** dans phpMyAdmin
4. Télécharger le fichier `.sql`

**Automatiser avec un cron job** :

```bash
# Via SSH - Créer un script backup.sh

#!/bin/bash
# backup.sh - Backup automatique MySQL

DATE=$(date +%Y%m%d_%H%M%S)
DB_USER="u123456789_nyanga"
DB_PASS="VotreMotDePasseMySQL"
DB_NAME="u123456789_nyangabudget"
BACKUP_DIR="$HOME/backups"

mkdir -p $BACKUP_DIR

mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/nyanga_$DATE.sql

# Garder seulement les 7 derniers backups
ls -t $BACKUP_DIR/nyanga_*.sql | tail -n +8 | xargs rm -f

echo "Backup créé: nyanga_$DATE.sql"
```

**Ajouter au cron** :

```bash
chmod +x backup.sh

# Éditer crontab
crontab -e

# Ajouter (backup quotidien à 2h du matin)
0 2 * * * /home/u123456789/backup.sh
```

#### B. Backup des Fichiers Uploadés

```bash
# Script backup_uploads.sh

#!/bin/bash
DATE=$(date +%Y%m%d)
cd ~/public_html/nyangabudget
tar -czf ~/backups/uploads_$DATE.tar.gz uploads/

# Garder 14 jours
find ~/backups/uploads_*.tar.gz -mtime +14 -delete
```

### 3. Mises à Jour

#### A. Mettre à Jour le Code

```bash
# Via SSH

cd ~/public_html/nyangabudget

# Si utilisation de Git
git pull origin main

# Redémarrer l'application
touch tmp/restart.txt
```

Ou via FTP : réuploader les fichiers modifiés

#### B. Mettre à Jour les Dépendances Python

```bash
source ~/nyangabudget_venv/bin/activate
pip install --upgrade -r requirements.txt
touch tmp/restart.txt
```

### 4. Gestion des Erreurs Courantes

#### Problème: Application ne démarre pas

**Solution:**

```bash
# Vérifier les logs
cat ~/public_html/nyangabudget/tmp/passenger.log

# Vérifier la syntaxe Python
python3 app.py
```

#### Problème: Erreur base de données

**Solution:**

```bash
# Tester la connexion MySQL
mysql -u u123456789_nyanga -p u123456789_nyangabudget

# Vérifier les variables d'environnement
cat .env
```

#### Problème: Fichiers non uploadables

**Solution:**

```bash
# Vérifier les permissions
ls -la uploads/
chmod 775 uploads/vault/
```

---

## 🚀 Optimisations Recommandées

### 1. Performance

#### A. Activer le Cache Flask

Dans `app.py`, le cache est déjà configuré. Pour utiliser Redis :

```bash
# Installer Redis sur Hostinger (si disponible)
# Contacter le support Hostinger pour activer Redis

# Mettre à jour .env
REDIS_URL=redis://localhost:6379/0
```

#### B. Optimiser les Requêtes SQL

```python
# Dans app.py - Utiliser les index existants

# Exemple: Requêtes optimisées avec joinedload
from sqlalchemy.orm import joinedload

depenses = Depense.query\
    .options(joinedload(Depense.categorie))\
    .filter_by(user_id=current_user.id)\
    .order_by(Depense.date_created.desc())\
    .limit(100)\
    .all()
```

#### C. Minifier CSS/JS

```bash
# Installer un minifier
pip install cssmin jsmin

# Créer un script minify.py
```

#### D. Compresser les Images

```bash
# Optimiser les logos
pip install pillow

# Script Python pour compresser
from PIL import Image

img = Image.open('static/images/logo.png')
img.save('static/images/logo.png', optimize=True, quality=85)
```

### 2. Sécurité Avancée

#### A. Configurer les Headers de Sécurité

Ajouter dans `.htaccess` :

```apache
# Headers de sécurité

Header set X-Frame-Options "SAMEORIGIN"
Header set X-Content-Type-Options "nosniff"
Header set X-XSS-Protection "1; mode=block"
Header set Referrer-Policy "strict-origin-when-cross-origin"
Header set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' cdn.jsdelivr.net cdn.plot.ly; style-src 'self' 'unsafe-inline' cdn.jsdelivr.net"
```

#### B. Activer Fail2Ban (Protection Brute Force)

```bash
# Contacter le support Hostinger pour activer Fail2Ban
# ou utiliser Flask-Limiter (déjà en place)
```

#### C. Scanner les Vulnérabilités

```bash
# Localement, scanner les dépendances
pip install safety
safety check -r requirements.txt
```

### 3. SEO et PWA

#### A. Ajouter un `robots.txt`

```txt
# robots.txt

User-agent: *
Disallow: /uploads/
Disallow: /api/
Allow: /

Sitemap: https://votredomaine.com/sitemap.xml
```

#### B. Configurer la PWA

Le fichier `manifest.webmanifest` existe déjà. Ajouter dans `base.html` :

```html
<link rel="manifest" href="{{ url_for('static', filename='manifest.webmanifest') }}">
<meta name="theme-color" content="#4a90e2">
```

#### C. Optimiser pour Mobile

```html
<!-- Dans base.html <head> -->
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
```

---

## 🛠️ Dépannage

### Problèmes Courants

#### 1. Erreur 500 - Internal Server Error

**Causes possibles:**

- Erreur de syntaxe Python
- Module manquant
- Erreur de connexion base de données
- Permissions fichiers incorrectes

**Solutions:**

```bash
# Vérifier les logs
cat ~/public_html/nyangabudget/tmp/passenger.log

# Vérifier la syntaxe
python3 app.py

# Vérifier les modules
source ~/nyangabudget_venv/bin/activate
pip list

# Vérifier les permissions
chmod -R 755 ~/public_html/nyangabudget
chmod -R 775 ~/public_html/nyangabudget/uploads
```

#### 2. Page Blanche

**Solution:**

```bash
# Vérifier .htaccess
cat .htaccess

# Vérifier passenger_wsgi.py
cat passenger_wsgi.py

# Redémarrer
touch tmp/restart.txt
```

#### 3. Fichiers Statiques Non Chargés (404)

**Solution:**

```apache
# Dans .htaccess - Ajouter
<FilesMatch "\.(css|js|png|jpg|jpeg|gif|svg)$">
    Header set Cache-Control "public, max-age=2592000"
    Allow from all
</FilesMatch>
```

#### 4. Base de Données Non Connectée

**Solution:**

```bash
# Tester la connexion MySQL
mysql -h localhost -u u123456789_nyanga -p u123456789_nyangabudget

# Vérifier les variables .env
echo $DB_HOST
echo $DB_USER
echo $DB_NAME

# Re-créer les tables
python3
>>> from app import db, init_db
>>> init_db()
```

#### 5. Upload de Fichiers Échoue

**Solution:**

```bash
# Vérifier les permissions
ls -la uploads/vault/

# Corriger
chmod 775 uploads/vault/
chown u123456789:u123456789 uploads/vault/

# Vérifier la limite PHP
# hPanel > "Advanced" > "PHP Configuration"
# post_max_size = 16M
# upload_max_filesize = 16M
```

#### 6. Dark Mode Ne Fonctionne Pas

**Solution:**

```html
<!-- Vérifier que darkmode.js est chargé dans base.html -->
<script src="{{ url_for('static', filename='darkmode.js') }}"></script>

<!-- Vérifier la console navigateur (F12) -->
```

---

## 📞 Support et Ressources

### Documentation

- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **Hostinger Help**: https://support.hostinger.com/
- **MySQL**: https://dev.mysql.com/doc/

### Commandes Utiles

```bash
# SSH Hostinger
ssh u123456789@votredomaine.com

# Activer virtualenv
source ~/nyangabudget_venv/bin/activate

# Redémarrer l'app
touch ~/public_html/nyangabudget/tmp/restart.txt

# Voir les logs
tail -f ~/public_html/nyangabudget/logs/nyanga.log

# Backup MySQL
mysqldump -u user -p database > backup.sql

# Restore MySQL
mysql -u user -p database < backup.sql

# Permissions
chmod 755 dossier/
chmod 644 fichier.txt

# Espace disque
df -h
du -sh ~/public_html/nyangabudget
```

### Contact Support Hostinger

- **Chat Live 24/7**: Via hPanel
- **Email**: support@hostinger.com
- **Base de connaissances**: https://support.hostinger.com/fr/

---

## ✅ Checklist Finale de Déploiement

### Avant le Déploiement

- [ ] Base de données MySQL créée sur Hostinger
- [ ] Utilisateur MySQL créé avec tous les privilèges
- [ ] Fichier `.env` configuré avec bonnes credentials
- [ ] `requirements.txt` inclut `PyMySQL>=1.1.0`
- [ ] `passenger_wsgi.py` créé à la racine
- [ ] `.htaccess` configuré pour Passenger
- [ ] Logos uploadés dans `static/images/`
- [ ] Dossiers `uploads/` créés

### Pendant le Déploiement

- [ ] Fichiers uploadés via FTP/SSH
- [ ] Environnement virtuel créé
- [ ] Dépendances installées (`pip install -r requirements.txt`)
- [ ] Permissions configurées (755 pour dossiers, 775 pour uploads)
- [ ] Variables d'environnement dans `.env`
- [ ] Application redémarrée (`touch tmp/restart.txt`)

### Après le Déploiement

- [ ] Page de connexion accessible
- [ ] SSL/HTTPS activé
- [ ] Connexion admin@nyanga.cm fonctionne
- [ ] Dashboard affiche les graphiques
- [ ] Upload de fichiers fonctionne
- [ ] Transferts bancaires fonctionnent
- [ ] QR codes générés correctement
- [ ] Notifications visibles
- [ ] Score IA calculé
- [ ] Dark mode fonctionne
- [ ] Exports PDF/CSV téléchargeables
- [ ] Logs configurés
- [ ] Backup automatique planifié
- [ ] Monitoring (UptimeRobot) activé

---

## 🎉 Conclusion

Votre application **NyangaBudget 2.0** est maintenant prête pour un déploiement professionnel sur **Hostinger** !

### Récapitulatif

✅ **17 fonctionnalités** complètes et testées  
✅ **Architecture robuste** avec Flask + MySQL  
✅ **Sécurité renforcée** (CSRF, Rate Limiting, AES-256)  
✅ **Interface moderne** avec Bootstrap 5 + Dark Mode  
✅ **Documentation complète** (48 KB - 5 fichiers)  
✅ **Prêt pour la production** sur Hostinger

### Prochaines Étapes Recommandées

1. **Déployer** en suivant ce guide étape par étape
2. **Tester** toutes les fonctionnalités en production
3. **Configurer** les backups automatiques
4. **Activer** le monitoring (UptimeRobot)
5. **Optimiser** les performances (cache, CDN)
6. **Promouvoir** votre application auprès des utilisateurs
7. **Collecter** les feedbacks et améliorer

### URL Finale

```
https://votredomaine.com/nyangabudget
ou
https://budget.votredomaine.com
```

**Compte admin par défaut:**
- Email: `admin@nyanga.cm`
- Mot de passe: `admin123`

**⚠️ Important:** Changez le mot de passe admin dès la première connexion !

---

## 📧 Besoin d'Aide ?

Si vous rencontrez des difficultés :

1. **Vérifier les logs** (`~/public_html/nyangabudget/logs/`)
2. **Consulter la section Dépannage** de ce guide
3. **Contacter le support Hostinger** (chat 24/7)
4. **Consulter la documentation Flask** (flask.palletsprojects.com)

---

**Créé avec ❤️ pour NyangaBudget 2.0**  
**Dernière mise à jour:** 26 Décembre 2025  
**Version:** 1.0

**Bon déploiement ! 🚀**
