# 🚀 Guide Pratique de Déploiement Hostinger - NyangaBudget

**Date:** 26 Décembre 2025  
**Durée:** 15-20 minutes

---

## ✅ ÉTAPE 1 : Connexion à hPanel Hostinger

### 1.1 Se connecter
1. Allez sur : https://hpanel.hostinger.com
2. Connectez-vous avec vos identifiants Hostinger
3. Sélectionnez votre plan d'hébergement

---

## 🗄️ ÉTAPE 2 : Créer la Base de Données MySQL

### 2.1 Accéder aux bases de données
1. Dans hPanel, allez dans **Bases de données** → **Gestion MySQL**
2. Cliquez sur **Créer une nouvelle base de données**

### 2.2 Configuration de la base
```
Nom de la base : u123456789_nyangabudget
Nom d'utilisateur : u123456789_nyanga
Mot de passe : [GÉNÉRER UN MOT DE PASSE FORT]
```

**⚠️ IMPORTANT : Notez ces informations quelque part !**

### 2.3 Informations à récupérer
Après création, notez :
- ✅ Nom de la base : `u123456789_nyangabudget`
- ✅ Utilisateur : `u123456789_nyanga`
- ✅ Mot de passe : `[votre_mdp_généré]`
- ✅ Hôte : `localhost` (généralement)
- ✅ Port : `3306` (par défaut)

---

## 📂 ÉTAPE 3 : Récupérer les Identifiants FTP

### 3.1 Accéder aux comptes FTP
1. Dans hPanel, allez dans **Fichiers** → **Comptes FTP**
2. Notez ou créez un compte FTP :

```
Hôte FTP : ftp.votredomaine.com
Utilisateur FTP : u123456789
Mot de passe FTP : [votre_mdp_ftp]
Port : 21
```

### 3.2 Déterminer le chemin de destination
Le chemin typique Hostinger :
```
/home/u123456789/public_html/nyangabudget/
```

**💡 Astuce :** Pour un sous-domaine comme `budget.votredomaine.com`, utilisez :
```
/home/u123456789/domains/budget.votredomaine.com/public_html/
```

---

## ⚙️ ÉTAPE 4 : Configuration Locale pour le Déploiement

### 4.1 Créer le fichier .env pour la production

Créez un fichier `.env.production` avec vos vraies informations :

```bash
# Base de données MySQL Hostinger
DATABASE_URL=mysql+pymysql://u123456789_nyanga:VOTRE_MDP_MYSQL@localhost:3306/u123456789_nyangabudget

# Clé secrète Flask (génération aléatoire)
SECRET_KEY=votre_clé_secrète_très_longue_et_aléatoire_ici

# Clé de cryptage (32 caractères minimum)
MASTER_ENCRYPTION_KEY=VotreCléDeCryptage32BytesIci!!

# Mode production
FLASK_ENV=production
DEBUG=False

# Configuration email (optionnel)
MAIL_SERVER=smtp.hostinger.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=noreply@votredomaine.com
MAIL_PASSWORD=votre_mdp_email
```

### 4.2 Générer les clés secrètes

Exécutez dans votre terminal :

```powershell
# Générer SECRET_KEY
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"

# Générer MASTER_ENCRYPTION_KEY (doit faire 32 caractères)
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_urlsafe(32)[:32])"
```

---

## 🔧 ÉTAPE 5 : Configurer deploy_hostinger.py

Ouvrez le fichier `deploy_hostinger.py` et modifiez les lignes 19-22 :

```python
# ==================== CONFIGURATION FTP ====================
FTP_HOST = 'ftp.votredomaine.com'              # ← Votre hôte FTP
FTP_USER = 'u123456789'                         # ← Votre utilisateur FTP
FTP_PASS = 'VOTRE_MDP_FTP_ICI'                 # ← Votre mot de passe FTP
FTP_REMOTE_DIR = '/public_html/nyangabudget'    # ← Chemin de destination
```

---

## 🚀 ÉTAPE 6 : Lancer le Déploiement

### 6.1 Vérifier que l'app locale fonctionne
```powershell
# Arrêter le serveur si nécessaire
Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue

# Vérifier que tout est OK
.\.venv\Scripts\python.exe -m flake8 app.py --count
```

### 6.2 Lancer le déploiement FTP
```powershell
.\.venv\Scripts\python.exe deploy_hostinger.py
```

Le script va :
- ✅ Se connecter au serveur FTP
- ✅ Créer les dossiers nécessaires
- ✅ Uploader tous les fichiers (~50 fichiers)
- ✅ Afficher la progression en temps réel

---

## 📡 ÉTAPE 7 : Configuration SSH (Post-Déploiement)

### 7.1 Se connecter en SSH

```bash
ssh u123456789@votredomaine.com
# Entrer votre mot de passe SSH
```

### 7.2 Naviguer vers votre application
```bash
cd public_html/nyangabudget
ls -la
```

### 7.3 Créer l'environnement virtuel Python
```bash
# Vérifier la version Python disponible
python3 --version

# Créer le virtualenv
python3 -m venv venv

# Activer le virtualenv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt
```

### 7.4 Créer le fichier .env sur le serveur
```bash
nano .env
```

Copier-coller le contenu de votre `.env.production` local, puis :
- `CTRL+O` pour sauvegarder
- `CTRL+X` pour quitter

### 7.5 Initialiser la base de données
```bash
python3 -c "from app import db, app; app.app_context().push(); db.create_all(); print('Base de données initialisée!')"
```

### 7.6 Redémarrer l'application
```bash
# Créer/toucher le fichier de redémarrage Passenger
touch tmp/restart.txt

# Ou créer le dossier tmp s'il n'existe pas
mkdir -p tmp
touch tmp/restart.txt
```

---

## 🧪 ÉTAPE 8 : Tester l'Application

### 8.1 Accéder à l'application
Ouvrez votre navigateur :
```
https://votredomaine.com/nyangabudget
```
ou
```
https://budget.votredomaine.com
```

### 8.2 Tester les fonctionnalités
1. ✅ Page de connexion s'affiche
2. ✅ Connexion avec admin@nyanga.cm / admin123
3. ✅ Dashboard s'affiche
4. ✅ Créer une dépense de test
5. ✅ Vérifier les graphiques
6. ✅ Tester le dark mode

---

## 🔍 ÉTAPE 9 : Vérifier les Logs d'Erreurs

### 9.1 Via SSH
```bash
# Voir les logs d'erreurs Passenger
tail -f logs/error.log

# Ou voir les logs Apache
tail -f /var/log/apache2/error.log
```

### 9.2 Via hPanel
1. Allez dans **Fichiers** → **Gestionnaire de fichiers**
2. Naviguez vers `public_html/nyangabudget/logs/`
3. Téléchargez et consultez les fichiers de log

---

## ⚠️ Problèmes Courants et Solutions

### Erreur 500 - Internal Server Error
**Cause :** Permissions incorrectes ou .env manquant

**Solution :**
```bash
# Vérifier les permissions
chmod 755 passenger_wsgi.py
chmod 644 .env
chmod -R 755 static/
chmod -R 755 templates/

# Redémarrer
touch tmp/restart.txt
```

### Erreur "ModuleNotFoundError"
**Cause :** Dépendances non installées

**Solution :**
```bash
source venv/bin/activate
pip install -r requirements.txt
touch tmp/restart.txt
```

### Base de données inaccessible
**Cause :** Credentials MySQL incorrects

**Solution :**
1. Vérifier `.env` : `DATABASE_URL` doit correspondre exactement
2. Tester la connexion MySQL :
```bash
mysql -u u123456789_nyanga -p u123456789_nyangabudget
```

### Assets CSS/JS ne chargent pas
**Cause :** Chemins incorrects

**Solution :**
```bash
# Vérifier que le dossier static existe
ls -la static/

# Permissions
chmod -R 755 static/
```

---

## 🎯 Checklist Finale

Avant de considérer le déploiement terminé :

- [ ] ✅ Base de données MySQL créée
- [ ] ✅ Utilisateur MySQL avec permissions accordées
- [ ] ✅ Compte FTP fonctionnel
- [ ] ✅ Fichiers uploadés via FTP
- [ ] ✅ Environnement virtuel Python créé
- [ ] ✅ Dépendances installées (requirements.txt)
- [ ] ✅ Fichier .env configuré sur le serveur
- [ ] ✅ Base de données initialisée (tables créées)
- [ ] ✅ passenger_wsgi.py configuré
- [ ] ✅ Application redémarrée (tmp/restart.txt)
- [ ] ✅ Site accessible via navigateur
- [ ] ✅ Connexion admin fonctionne
- [ ] ✅ Toutes les pages s'affichent correctement

---

## 📞 Support

Si vous rencontrez des problèmes :

1. **Documentation Hostinger :** https://support.hostinger.com
2. **Forum Hostinger :** https://community.hostinger.com
3. **Support 24/7 :** Via le chat dans hPanel

---

## 🎉 Félicitations !

Votre application NyangaBudget est maintenant en production sur Hostinger ! 🚀

**Prochaines étapes recommandées :**
- Configurer un certificat SSL (HTTPS)
- Configurer les sauvegardes automatiques
- Mettre en place un monitoring
- Créer un domaine personnalisé
- Configurer les emails transactionnels

---

**Bon déploiement ! 💪**
