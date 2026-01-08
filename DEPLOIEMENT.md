# Guide de déploiement - PythonAnywhere

## Configuration complète pour NyangaBudget

### Prérequis
- Compte PythonAnywhere (gratuit ou payant)
- Dépôt GitHub accessible
- Python 3.10

---

## 📋 Étapes de déploiement

### 1. Cloner le projet

```bash
cd ~
git clone https://github.com/jolu-bot/NyangaBudget.git
cd NyangaBudget
```

### 2. Créer l'environnement virtuel

```bash
mkvirtualenv nyanga_env --python=/usr/bin/python3.10
workon nyanga_env
pip install --no-cache-dir -r requirements.txt
```

### 3. Créer la base de données MySQL

Via l'interface PythonAnywhere :
- Databases → Initialize MySQL
- Create database: `Username$nyangabudget`
- Noter les identifiants MySQL

### 4. Configurer les variables d'environnement

Créer `.env` :

```
SECRET_KEY=generer_une_cle_secrete_ici
DATABASE_URL=mysql+pymysql://Username:Password%21%40%3E@Username.mysql.pythonanywhere-services.com/Username$nyangabudget
ENCRYPTION_KEY=generer_32_caracteres_ici
DOMAIN=https://Username.pythonanywhere.com
```

⚠️ **Encodage URL** : Les caractères spéciaux du mot de passe doivent être encodés :
- `!` → `%21`
- `@` → `%40`
- `>` → `%3E`

### 5. Initialiser les tables

```bash
python3 init_mysql.py
```

Vérifier la création des 16 tables :
```bash
mysql -u Username -p -h Username.mysql.pythonanywhere-services.com Username$nyangabudget -e "SHOW TABLES;"
```

### 6. Configurer l'application Web

**Web Tab** → **Add a new web app**

- Framework: Manual configuration
- Python version: 3.10

**Source code** : `/home/Username/NyangaBudget`

**WSGI configuration file** : Remplacer par le contenu de `wsgi_pythonanywhere.py`

**Virtualenv** : `/home/Username/.virtualenvs/nyanga_env`

**Static files** :
```
URL: /static/
Directory: /home/Username/NyangaBudget/static
```

### 7. Recharger et tester

- Cliquer sur **Reload Username.pythonanywhere.com**
- Accéder à `https://Username.pythonanywhere.com`
- Tester l'inscription et la connexion

---

## 🔄 Mise à jour de l'application

```bash
cd ~/NyangaBudget
git pull
workon nyanga_env
pip install -r requirements.txt  # Si nouvelles dépendances
```

Recharger l'application via le bouton **Reload**.

---

## 📊 Monitoring et logs

### Logs d'erreur
```bash
tail -100 /var/log/Username.pythonanywhere.com.error.log
```

### Logs d'accès
```bash
tail -100 /var/log/Username.pythonanywhere.com.access.log
```

### Logs du serveur
```bash
tail -100 /var/log/Username.pythonanywhere.com.server.log
```

---

## 🐛 Résolution de problèmes courants

### Erreur de connexion MySQL

Vérifier l'encodage URL du mot de passe dans DATABASE_URL.

### Module non trouvé

```bash
cd ~/NyangaBudget
workon nyanga_env
pip install nom_du_module
```

### Erreur de template

```bash
cd ~/NyangaBudget
git status  # Vérifier les fichiers modifiés
git pull    # Récupérer la dernière version
```

### Application ne se charge pas

1. Vérifier les logs d'erreur
2. Vérifier que l'environnement virtuel est activé
3. Vérifier que les tables existent dans MySQL
4. Recharger l'application

---

## ✅ Checklist de déploiement

- [ ] Code cloné depuis GitHub
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées
- [ ] Base de données MySQL créée
- [ ] Fichier .env configuré avec DATABASE_URL encodée
- [ ] Tables créées avec init_mysql.py
- [ ] WSGI configuré
- [ ] Virtualenv configuré
- [ ] Static files mappés
- [ ] Application rechargée
- [ ] Tests effectués (inscription, connexion)

---

## 📞 Support

En cas de problème, vérifier :
1. Les logs d'erreur
2. La configuration .env
3. Les permissions des fichiers
4. L'état de la base de données
