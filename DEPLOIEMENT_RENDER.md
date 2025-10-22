# 🚀 Guide Complet de Déploiement - NyangaBudget 2.0 sur Render

**Durée estimée:** 10-15 minutes  
**Coût:** GRATUIT (plan free tier)  
**Date:** Octobre 2025

---

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Préparation du projet](#préparation-du-projet)
3. [Création du compte Render](#création-du-compte-render)
4. [Déploiement automatique](#déploiement-automatique)
5. [Vérification et tests](#vérification-et-tests)
6. [Configuration du domaine personnalisé](#configuration-du-domaine-personnalisé)
7. [Dépannage](#dépannage)
8. [Maintenance](#maintenance)

---

## ✅ Prérequis

Avant de commencer, assurez-vous d'avoir :

- [x] Un compte GitHub avec le dépôt `NyangaBudget` à jour
- [x] Git installé et configuré sur votre machine
- [x] Tous les fichiers modifiés et commités (voir section Préparation)
- [x] Une connexion Internet stable

---

## 📦 Préparation du projet

### Étape 1: Vérifier les modifications

Les fichiers suivants ont été mis à jour pour supporter PostgreSQL :

✅ **app.py** - Configuration multi-base de données (SQLite + PostgreSQL)  
✅ **requirements.txt** - Ajout de `psycopg2-binary`  
✅ **render.yaml** - Configuration complète avec base de données  
✅ **.env.example** - Template des variables d'environnement  

### Étape 2: Committer et pousser sur GitHub

```powershell
# 1. Vérifier l'état
git status

# 2. Ajouter tous les fichiers modifiés
git add .

# 3. Créer un commit
git commit -m "Configuration pour déploiement Render avec PostgreSQL"

# 4. Pousser sur GitHub
git push origin main
```

### Étape 3: Vérifier sur GitHub

Allez sur `https://github.com/jolu-bot/NyangaBudget` et vérifiez que :
- Le fichier `render.yaml` est visible
- Les modifications de `app.py` sont présentes
- Le fichier `.env.example` est là

---

## 🎯 Création du compte Render

### Étape 1: Inscription

1. Allez sur **[render.com](https://render.com)**
2. Cliquez sur **"Get Started"** (en haut à droite)
3. Sélectionnez **"Sign up with GitHub"**
4. Autorisez Render à accéder à votre compte GitHub
5. Confirmez votre adresse email si demandé

### Étape 2: Connexion de votre dépôt

1. Render détectera automatiquement vos dépôts GitHub
2. Si demandé, cliquez sur **"Configure account"**
3. Sélectionnez les dépôts à autoriser :
   - Option 1: **All repositories** (recommandé pour débuter)
   - Option 2: **Only select repositories** → Choisir `NyangaBudget`
4. Cliquez sur **"Install"**

---

## 🚀 Déploiement automatique

### Étape 1: Créer le Blueprint

1. Dans le dashboard Render, cliquez sur **"New +"** → **"Blueprint"**
2. Render affichera vos dépôts GitHub
3. Trouvez et cliquez sur **"NyangaBudget"**
4. Render détectera automatiquement le fichier `render.yaml`

### Étape 2: Configuration automatique

Render créera automatiquement :

**🌐 Web Service: nyangabudget**
- Type: Web Service
- Environnement: Python 3.11
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Plan: Free
- Région: Frankfurt (Europe)

**🗄️ PostgreSQL Database: nyangabudget-db**
- Type: PostgreSQL 15
- Plan: Free (90 jours, renouvelable)
- Région: Frankfurt
- Connexion: Automatique via `DATABASE_URL`

### Étape 3: Valider et déployer

1. Vérifiez la configuration affichée
2. Cliquez sur **"Apply"** ou **"Create Blueprint"**
3. Render commencera le déploiement automatiquement

---

## ⏳ Processus de déploiement

### Ce qui se passe en arrière-plan:

```
[1/6] 🔄 Clonage du dépôt GitHub...
[2/6] 🏗️  Construction de l'environnement Python 3.11...
[3/6] 📦 Installation des dépendances (pip install)...
[4/6] 🗄️  Création de la base de données PostgreSQL...
[5/6] 🔗 Connexion de l'app à la base de données...
[6/6] 🚀 Démarrage du serveur Gunicorn...
```

**Durée:** 3-5 minutes

### Suivre les logs en temps réel:

1. Cliquez sur le service **"nyangabudget"**
2. Allez dans l'onglet **"Logs"**
3. Vous verrez :
   ```
   Installing dependencies...
   ✓ Flask installed
   ✓ PostgreSQL connected
   [OK] Utilisation de PostgreSQL (Production)
   Starting Gunicorn...
   Listening at: http://0.0.0.0:10000
   ```

---

## ✅ Vérification et tests

### Étape 1: Obtenir l'URL de votre application

Une fois le déploiement terminé :

1. Allez dans **Dashboard** → **nyangabudget**
2. En haut, vous verrez votre URL : `https://nyangabudget.onrender.com`
3. Cliquez dessus pour ouvrir l'application

### Étape 2: Créer le premier compte

**⚠️ IMPORTANT:** La base PostgreSQL est vide au premier déploiement !

1. Ouvrez votre application : `https://nyangabudget.onrender.com`
2. Cliquez sur **"S'inscrire"** ou **"Register"**
3. Créez votre compte administrateur :
   - Nom complet: Votre nom
   - Email: votre-email@exemple.cm
   - Mot de passe: *(sécurisé)*
   - Confirmez le mot de passe
4. Cliquez sur **"S'inscrire"**

### Étape 3: Tester les fonctionnalités

Vérifiez que tout fonctionne :

- ✅ Dashboard s'affiche correctement
- ✅ Ajout d'un compte bancaire
- ✅ Ajout d'une dépense
- ✅ Ajout d'un revenu
- ✅ Graphiques interactifs Plotly
- ✅ Coffre-fort (upload de fichier)
- ✅ Logos Nyanga visibles

---

## 🌐 Configuration du domaine personnalisé (Optionnel)

### Avec un domaine que vous possédez:

1. Dans Render, allez dans **Settings** → **Custom Domain**
2. Cliquez sur **"Add Custom Domain"**
3. Entrez votre domaine : `budget.votredomaine.cm`
4. Ajoutez un enregistrement CNAME chez votre registrar :
   ```
   Type: CNAME
   Name: budget
   Value: nyangabudget.onrender.com
   ```
5. Attendez la propagation DNS (5-30 minutes)
6. SSL sera activé automatiquement

---

## 🛠️ Dépannage

### Problème 1: "Application Error" au démarrage

**Cause:** Base de données non initialisée

**Solution:**
1. Allez dans **Shell** (dans Render)
2. Lancez Python :
   ```bash
   python
   ```
3. Créez les tables :
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
       print("Tables créées!")
   exit()
   ```

### Problème 2: "502 Bad Gateway"

**Cause:** L'application met du temps à démarrer (plan gratuit)

**Solution:** Attendez 30-60 secondes et rafraîchissez la page

### Problème 3: Images/Logos ne s'affichent pas

**Cause:** Fichiers statiques non chargés

**Solution:**
1. Vérifiez que le dossier `static/` est sur GitHub
2. Vérifiez les logs Render pour les erreurs 404
3. Redéployez : **Manual Deploy** → **Deploy latest commit**

### Problème 4: Base de données "expire après 90 jours"

**Cause:** Plan gratuit PostgreSQL limité

**Solution:**
1. Render vous préviendra par email avant expiration
2. Vous pouvez **renouveler gratuitement** la base
3. Ou exporter les données et recréer une nouvelle base

---

## 🔧 Maintenance

### Mettre à jour l'application

Chaque fois que vous modifiez le code :

```powershell
# 1. Committer localement
git add .
git commit -m "Nouvelle fonctionnalité"

# 2. Pousser sur GitHub
git push origin main

# 3. Render redéploie automatiquement! 🎉
```

**Auto-Deploy est activé par défaut**

### Voir les logs en production

1. Dashboard Render → **nyangabudget**
2. Onglet **"Logs"**
3. Recherchez les erreurs ou warnings

### Redémarrer l'application

1. Dashboard Render → **nyangabudget**
2. Cliquez sur **"Manual Deploy"**
3. Sélectionnez **"Clear build cache & deploy"**

### Sauvegarder la base de données

```bash
# Depuis votre terminal local
# 1. Installer PostgreSQL client
# 2. Obtenir DATABASE_URL depuis Render (Settings → Environment)
# 3. Exporter
pg_dump DATABASE_URL > backup_$(date +%Y%m%d).sql
```

---

## 📊 Limites du plan gratuit Render

| Ressource | Limite |
|-----------|--------|
| **RAM** | 512 MB |
| **Build minutes** | 500 min/mois (largement suffisant) |
| **Bande passante** | 100 GB/mois |
| **Base PostgreSQL** | 1 GB stockage, expire après 90 jours |
| **Inactivité** | L'app s'endort après 15 min sans trafic |
| **Réveil** | ~30 secondes |
| **Services** | 1 web + 1 base de données gratuits |

---

## 🎓 Ressources utiles

- **Dashboard Render:** [dashboard.render.com](https://dashboard.render.com)
- **Documentation Render:** [render.com/docs](https://render.com/docs)
- **Support Render:** [Community Forum](https://community.render.com)
- **Status Render:** [status.render.com](https://status.render.com)

---

## 🎉 Félicitations !

Votre application **NyangaBudget 2.0** est maintenant en ligne ! 🚀

**URL de production:** `https://nyangabudget.onrender.com`

### Prochaines étapes recommandées:

1. ✅ Partager le lien avec votre famille
2. ✅ Configurer un domaine personnalisé (optionnel)
3. ✅ Sauvegarder régulièrement la base de données
4. ✅ Surveiller l'expiration PostgreSQL (notification email)
5. ✅ Continuer à améliorer l'application

---

## 📞 Besoin d'aide ?

- **GitHub Issues:** [github.com/jolu-bot/NyangaBudget/issues](https://github.com/jolu-bot/NyangaBudget/issues)
- **Email:** joyed.lumoindou@exemple.cm
- **Render Community:** [community.render.com](https://community.render.com)

---

**Développé avec ❤️ par Joyed Lumoindou**  
**NyangaBudget 2.0 - Plateforme Familiale de Gestion Financière**  
**Cameroun 🇨🇲 | Octobre 2025**
