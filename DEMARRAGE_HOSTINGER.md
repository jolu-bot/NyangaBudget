# 🚀 Guide Rapide - Déploiement Hostinger (15 minutes)

**NyangaBudget 2.0 - Version Express pour Hostinger**

## 📋 Checklist Rapide

### ✅ Avant de Commencer

- [ ] Compte Hostinger Premium ou Business actif
- [ ] Domaine configuré (ex: nyangabudget.com)
- [ ] FileZilla installé (client FTP)
- [ ] Tous les fichiers du projet prêts

---

## 🎯 Étape 1: Créer la Base MySQL (5 min)

### Dans hPanel Hostinger :

1. **Aller dans "Databases" > "MySQL Databases"**

2. **Créer la base de données**
   - Cliquer sur "Create New Database"
   - Nom: `u123456789_nyangabudget` (Hostinger ajoute le préfixe automatiquement)

3. **Créer un utilisateur**
   - Cliquer sur "Create New User"
   - Utilisateur: `u123456789_nyanga`
   - Mot de passe: [Générer un mot de passe fort]
   - **NOTER ces informations !**

4. **Associer l'utilisateur à la base**
   - Privilèges: Tous
   - Cliquer sur "Add"

5. **Noter les credentials**
   ```
   Hôte: localhost
   Base: u123456789_nyangabudget
   Utilisateur: u123456789_nyanga
   Mot de passe: [le mot de passe créé]
   Port: 3306
   ```

---

## 📤 Étape 2: Upload des Fichiers FTP (5 min)

### Configuration FileZilla :

1. **Ouvrir FileZilla**

2. **Obtenir les identifiants FTP**
   - hPanel > "FTP Accounts"
   - Noter: Hôte, Utilisateur, Mot de passe

3. **Se connecter**
   ```
   Hôte: ftp.votredomaine.com
   Utilisateur: votreuser@votredomaine.com
   Mot de passe: [votre mot de passe FTP]
   Port: 21
   ```

4. **Créer le dossier distant**
   - Aller dans `/public_html/`
   - Créer le dossier `nyangabudget`

5. **Upload des fichiers**
   
   **À INCLURE :**
   - ✅ app.py
   - ✅ passenger_wsgi.py
   - ✅ .htaccess
   - ✅ requirements.txt
   - ✅ static/ (tout)
   - ✅ templates/ (tout)
   
   **À EXCLURE :**
   - ❌ .venv/
   - ❌ data/nyanga_v2.db
   - ❌ __pycache__/
   - ❌ .git/

6. **Créer les dossiers vides**
   
   Dans `/public_html/nyangabudget/` créer :
   ```
   uploads/
   uploads/vault/
   uploads/heritage/
   uploads/receipts/
   logs/
   tmp/
   ```

---

## 🔧 Étape 3: Configuration SSH (5 min)

### Connexion SSH :

```bash
# Via PowerShell ou PuTTY
ssh u123456789@votredomaine.com
# Entrer le mot de passe SSH
```

### Installation Python et Dépendances :

```bash
# 1. Créer l'environnement virtuel
cd ~/public_html/nyangabudget
python3 -m venv ~/nyangabudget_venv

# 2. Activer l'environnement
source ~/nyangabudget_venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Vérifier l'installation
pip list | grep Flask
```

### Créer le fichier .env :

```bash
# Créer le fichier
nano .env
```

**Contenu du .env :**

```bash
# Copier-coller et MODIFIER avec vos vraies valeurs

FLASK_ENV=production
DEBUG=False

# Base de données MySQL
DB_HOST=localhost
DB_USER=u123456789_nyanga
DB_PASSWORD=VotreMotDePasseMySQL
DB_NAME=u123456789_nyangabudget

# Clés de sécurité (générer des valeurs uniques)
SECRET_KEY=nyanga-prod-key-32-chars-minimum
MASTER_ENCRYPTION_KEY=nyanga-encryption-32-chars-min
```

**Sauvegarder:** `Ctrl+O`, `Enter`, `Ctrl+X`

### Générer des clés sécurisées :

```bash
# Générer une clé aléatoire
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Copier le résultat dans .env pour SECRET_KEY
# Relancer la commande pour MASTER_ENCRYPTION_KEY
```

### Modifier passenger_wsgi.py :

```bash
nano passenger_wsgi.py
```

**Modifier la ligne 11 :**

```python
# Remplacer 'u123456789' par votre vrai ID utilisateur
INTERP = os.path.join(os.environ['HOME'], 'nyangabudget_venv', 'bin', 'python3')
```

**Sauvegarder:** `Ctrl+O`, `Enter`, `Ctrl+X`

### Modifier .htaccess :

```bash
nano .htaccess
```

**Modifier les lignes 11 et 17 :**

```apache
# Ligne 11
PassengerAppRoot /home/VOTRE_ID/public_html/nyangabudget

# Ligne 17
PassengerPython /home/VOTRE_ID/nyangabudget_venv/bin/python3
```

Remplacer `VOTRE_ID` par votre vraie valeur (ex: u123456789)

**Sauvegarder:** `Ctrl+O`, `Enter`, `Ctrl+X`

### Configurer les permissions :

```bash
# Permissions des dossiers
chmod 755 ~/public_html/nyangabudget
chmod 775 ~/public_html/nyangabudget/uploads
chmod 775 ~/public_html/nyangabudget/uploads/vault
chmod 775 ~/public_html/nyangabudget/uploads/heritage
chmod 775 ~/public_html/nyangabudget/uploads/receipts
chmod 775 ~/public_html/nyangabudget/logs
chmod 775 ~/public_html/nyangabudget/tmp

# Protéger .env
chmod 600 ~/public_html/nyangabudget/.env
```

### Initialiser la base de données :

```bash
# Activer le virtualenv
source ~/nyangabudget_venv/bin/activate

# Lancer Python
python3

# Dans l'interpréteur Python
>>> from app import db, app, init_db
>>> init_db()
>>> exit()
```

### Redémarrer l'application :

```bash
cd ~/public_html/nyangabudget
mkdir -p tmp
touch tmp/restart.txt
```

---

## ✅ Étape 4: Configuration Domaine (2 min)

### Option A: Sous-domaine

1. **hPanel > "Domains" > "Subdomains"**
2. **Créer** : `budget.votredomaine.com`
3. **Document Root** : `/public_html/nyangabudget`

### Option B: Domaine principal

1. **hPanel > "Domains" > "Manage"**
2. **Modifier Document Root** : `/public_html/nyangabudget`

### Activer SSL :

1. **hPanel > "SSL"**
2. **Activer Let's Encrypt** (gratuit)
3. **Forcer HTTPS** (optionnel)

---

## 🧪 Tests Finaux (3 min)

### 1. Accéder à l'Application

Ouvrir dans le navigateur :
```
https://votredomaine.com/nyangabudget
ou
https://budget.votredomaine.com
```

**Attendu:** Page de connexion avec logo

### 2. Se Connecter

```
Email: admin@nyanga.cm
Mot de passe: admin123
```

**Attendu:** Redirection vers le dashboard

### 3. Tester une Fonctionnalité

- Ajouter une dépense
- Créer un compte bancaire
- Voir le dashboard

**Si tout fonctionne : ✅ DÉPLOIEMENT RÉUSSI !**

---

## 🛠️ Dépannage Rapide

### Erreur 500 - Internal Server Error

**Solution :**

```bash
# Voir les logs
cat ~/public_html/nyangabudget/tmp/passenger.log

# Vérifier les permissions
ls -la ~/public_html/nyangabudget/

# Redémarrer
touch ~/public_html/nyangabudget/tmp/restart.txt
```

### Page Blanche

**Solution :**

```bash
# Vérifier .htaccess
cat ~/public_html/nyangabudget/.htaccess

# Vérifier passenger_wsgi.py
cat ~/public_html/nyangabudget/passenger_wsgi.py

# Redémarrer Passenger
touch ~/public_html/nyangabudget/tmp/restart.txt
```

### Base de Données Non Connectée

**Solution :**

```bash
# Tester la connexion MySQL
mysql -h localhost -u u123456789_nyanga -p u123456789_nyangabudget

# Si ça fonctionne, vérifier .env
cat ~/public_html/nyangabudget/.env

# Recréer les tables
python3
>>> from app import db, init_db
>>> init_db()
>>> exit()
```

### Fichiers Statiques 404

**Solution :**

```bash
# Vérifier que les fichiers existent
ls -la ~/public_html/nyangabudget/static/

# Vérifier les permissions
chmod 755 ~/public_html/nyangabudget/static/
```

---

## 📞 Support

### Support Hostinger
- **Chat 24/7** : Via hPanel
- **Documentation** : https://support.hostinger.com/fr/

### Documentation Projet
- **Guide Complet** : `DEPLOIEMENT_HOSTINGER.md`
- **README** : `README.md`
- **Statut** : `STATUS_FINAL.md`

---

## 🎉 Succès !

Votre application **NyangaBudget 2.0** est maintenant déployée sur **Hostinger** !

### URLs :
- **Application** : https://votredomaine.com/nyangabudget
- **Dashboard** : https://votredomaine.com/nyangabudget/dashboard
- **API** : https://votredomaine.com/nyangabudget/api/stats

### Prochaines Étapes :
1. ✅ Changer le mot de passe admin
2. ✅ Configurer les backups automatiques (voir `backup_mysql.sh`)
3. ✅ Activer le monitoring (UptimeRobot)
4. ✅ Optimiser les performances (cache, CDN)
5. ✅ Inviter les utilisateurs

**Bon déploiement ! 🚀**
