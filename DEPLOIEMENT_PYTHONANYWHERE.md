# 🐍 Guide de Déploiement sur PythonAnywhere

## 📋 Pourquoi PythonAnywhere ?

✅ **100% Gratuit** pour votre projet
✅ **Optimisé pour Flask** - Configuration simple
✅ **Base MySQL incluse** - Pas besoin de PostgreSQL
✅ **Domaine gratuit** : `votrenom.pythonanywhere.com`
✅ **SSL automatique** - HTTPS inclus
✅ **Interface web** - Pas besoin de ligne de commande

---

## 🚀 DÉPLOIEMENT EN 10 MINUTES

### ÉTAPE 1 : Créer un Compte (2 min)

1. Aller sur : https://www.pythonanywhere.com
2. Cliquer sur **"Start running Python online in less than a minute"**
3. Créer un compte **GRATUIT** (Beginner Account)
4. Confirmer votre email

---

### ÉTAPE 2 : Téléverser Votre Code (3 min)

#### Option A : Via Git (Recommandé)

1. Ouvrir un **Bash Console** depuis le Dashboard
2. Cloner votre dépôt :
   ```bash
   git clone https://github.com/jolu-bot/NyangaBudget.git
   cd NyangaBudget
   ```

#### Option B : Upload Manuel

1. Aller dans **Files** depuis le Dashboard
2. Créer un dossier `NyangaBudget`
3. Téléverser tous vos fichiers (sauf `.venv` et `__pycache__`)

---

### ÉTAPE 3 : Créer un Environnement Virtuel (2 min)

Dans la **Bash Console** :

```bash
# Se placer dans le dossier du projet
cd ~/NyangaBudget

# Créer l'environnement virtuel
mkvirtualenv --python=/usr/bin/python3.10 nyanga_env

# Activer l'environnement
workon nyanga_env

# Installer les dépendances
pip install -r requirements.txt
```

**⏳ Patience** : L'installation prend 2-3 minutes.

---

### ÉTAPE 4 : Configurer la Base de Données MySQL (2 min)

1. Aller dans **Databases** depuis le Dashboard
2. **Initialiser MySQL** (cliquer sur le bouton)
3. Créer une base de données :
   - Nom suggéré : `votrenom$nyangabudget`
   - Noter le nom complet affiché

4. **IMPORTANT** : Noter ces informations :
   ```
   Nom de la base : votrenom$nyangabudget
   Utilisateur    : votrenom
   Mot de passe   : (celui que vous avez créé)
   Hôte          : votrenom.mysql.pythonanywhere-services.com
   ```

---

### ÉTAPE 5 : Configurer l'Application Web (3 min)

1. Aller dans **Web** depuis le Dashboard
2. Cliquer sur **"Add a new web app"**
3. Choisir :
   - Domain : `votrenom.pythonanywhere.com` (gratuit)
   - Python framework : **Flask**
   - Python version : **Python 3.10**
   - Path to Flask app : `/home/votrenom/NyangaBudget/wsgi_pythonanywhere.py`

4. Dans la section **Virtualenv** :
   ```
   /home/votrenom/.virtualenvs/nyanga_env
   ```

5. Dans la section **Static files**, ajouter :
   ```
   URL: /static/
   Directory: /home/votrenom/NyangaBudget/static
   ```

---

### ÉTAPE 6 : Configurer les Variables d'Environnement (1 min)

Dans la **Bash Console** :

```bash
cd ~/NyangaBudget

# Créer le fichier .env
nano .env
```

Copier ce contenu (remplacer les valeurs) :

```bash
# Flask
SECRET_KEY=votre_cle_secrete_generee_ci_dessous
FLASK_ENV=production

# Base de données MySQL
DATABASE_URL=mysql+pymysql://votrenom:votre_mot_de_passe@votrenom.mysql.pythonanywhere-services.com/votrenom$nyangabudget

# Cryptographie
ENCRYPTION_KEY=votre_cle_32_caracteres_generee_ci_dessous

# Domaine
DOMAIN=votrenom.pythonanywhere.com
```

**Générer les clés secrètes** :

```bash
# Dans la Bash Console
python3 << EOF
import secrets
print("SECRET_KEY=" + secrets.token_hex(32))
print("ENCRYPTION_KEY=" + secrets.token_urlsafe(32)[:32])
EOF
```

Copier les clés générées dans le fichier `.env`.

**Sauvegarder** : `Ctrl+O`, `Enter`, `Ctrl+X`

---

### ÉTAPE 7 : Modifier le Fichier app.py (1 min)

Votre fichier `app.py` doit utiliser SQLite en local et MySQL en production.

Dans la **Bash Console** :

```bash
nano ~/NyangaBudget/app.py
```

Vérifier que cette section existe (ligne ~76) :

```python
# Configuration Base de données
if os.getenv('DATABASE_URL'):
    # Production : MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    # Local : SQLite
    os.makedirs('data', exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/nyanga_v2.db'
```

**Si ce n'est pas le cas**, ajoutez ce code après les imports.

---

### ÉTAPE 8 : Initialiser la Base de Données (1 min)

Dans la **Bash Console** :

```bash
cd ~/NyangaBudget
workon nyanga_env

python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ Base de données initialisée !")
EOF
```

---

### ÉTAPE 9 : Recharger l'Application (10 secondes)

1. Retourner dans **Web** depuis le Dashboard
2. Cliquer sur le grand bouton vert **"Reload votrenom.pythonanywhere.com"**
3. Attendre 10 secondes

---

### ÉTAPE 10 : Tester l'Application 🎉

1. Cliquer sur le lien : `https://votrenom.pythonanywhere.com`
2. Vous devriez voir la page de connexion de NyangaBudget
3. Créer un compte ou utiliser :
   - Email : `admin@nyanga.cm`
   - Mot de passe : `admin123`

---

## 🔧 RÉSOLUTION DES PROBLÈMES

### ❌ Erreur 500 - Internal Server Error

**Consulter les logs** :
1. **Web** → **Log files** → `error.log`
2. Lire les dernières lignes pour identifier l'erreur

**Causes communes** :
- ❌ Mauvaise connexion MySQL → Vérifier `.env`
- ❌ Packages manquants → `pip install -r requirements.txt`
- ❌ Mauvais chemin WSGI → Vérifier le path

### ❌ Erreur "No module named 'flask'"

```bash
workon nyanga_env
pip install -r requirements.txt
```

Puis **Reload** l'application.

### ❌ Erreur de connexion MySQL

Vérifier le `DATABASE_URL` dans `.env` :
```
mysql+pymysql://USER:PASSWORD@HOST/DATABASE
```

**Tester la connexion** :
```bash
mysql -h votrenom.mysql.pythonanywhere-services.com -u votrenom -p
```

### ❌ Page blanche ou erreur 404

1. Vérifier que le fichier `wsgi_pythonanywhere.py` existe
2. Vérifier le chemin dans **Web** → **Code**
3. **Reload** l'application

---

## 📊 LIMITES DU COMPTE GRATUIT

| Ressource | Limite Gratuite | Suffisant ? |
|-----------|-----------------|-------------|
| **Bande passante** | Illimitée | ✅ Oui |
| **Stockage** | 512 MB | ✅ Oui |
| **CPU** | Limité | ✅ Pour petite utilisation |
| **MySQL** | 1 base | ✅ Oui |
| **Domaine** | `.pythonanywhere.com` | ✅ Oui |
| **Maintenance** | Réactiver tous les 3 mois | ⚠️ Facile |

---

## 🔄 MISE À JOUR DU CODE

Quand vous modifiez votre code localement :

1. **Push sur GitHub** :
   ```bash
   git add .
   git commit -m "Mise à jour"
   git push
   ```

2. **Mettre à jour sur PythonAnywhere** :
   ```bash
   # Dans la Bash Console
   cd ~/NyangaBudget
   git pull
   ```

3. **Recharger** l'application via le bouton **Reload**

---

## 🎓 PASSER EN VERSION PAYANTE (Optionnel)

Si votre app devient populaire, passez à **Hacker Plan** (5$/mois) :
- ✅ CPU illimité
- ✅ 1 GB stockage
- ✅ Plus de bases MySQL
- ✅ Support prioritaire
- ✅ Domaine personnalisé gratuit

---

## 📞 SUPPORT

- **Documentation** : https://help.pythonanywhere.com/
- **Forum** : https://www.pythonanywhere.com/forums/
- **Email** : support@pythonanywhere.com

---

## ✅ CHECKLIST FINALE

- [ ] Compte PythonAnywhere créé
- [ ] Code uploadé via Git
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] Base MySQL créée et configurée
- [ ] Application web configurée
- [ ] Fichier `.env` créé avec les bonnes valeurs
- [ ] Base de données initialisée
- [ ] Application rechargée
- [ ] Site accessible à `votrenom.pythonanywhere.com`

---

## 🎉 FÉLICITATIONS !

Votre application **NyangaBudget** est maintenant en ligne et accessible à tous !

**Partagez le lien** : `https://votrenom.pythonanywhere.com`

**Prochaines étapes** :
- Inviter votre famille à créer des comptes
- Tester toutes les fonctionnalités
- Surveiller les logs pour détecter les erreurs
- Faire des backups réguliers de la base MySQL

---

**Besoin d'aide ?** Consultez les logs dans **Web** → **Log files** 📊
