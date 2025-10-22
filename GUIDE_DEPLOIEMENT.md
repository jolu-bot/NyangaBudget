# 🚀 Guide de Déploiement Rapide - NyangaBudget 2.0

## ✅ ÉTAPE 1 : Préparer le Code

### A. Vérifier que tous les fichiers sont présents
```bash
# Fichiers obligatoires pour le déploiement :
✓ app.py (2500+ lignes)
✓ requirements.txt (12 dépendances)
✓ Procfile (commande gunicorn)
✓ render.yaml (config Render)
✓ .gitignore (fichiers à ignorer)
✓ README.md (documentation)
✓ templates/ (16 fichiers HTML)
✓ static/ (CSS + JS)
```

### B. Initialiser Git (si pas encore fait)
```bash
git init
git add .
git commit -m "Initial commit - NyangaBudget 2.0 ready for deployment"
```

---

## ✅ ÉTAPE 2 : Créer un Repository GitHub

### Option A : Via GitHub Desktop (plus simple)
1. Télécharger **GitHub Desktop** : https://desktop.github.com
2. Ouvrir GitHub Desktop
3. File → Add Local Repository → Sélectionner `NyangaBudget`
4. Publish Repository (bouton en haut)
5. Choisir un nom : `NyangaBudget`
6. Cocher "Private" si vous voulez un dépôt privé
7. Cliquer "Publish Repository"

### Option B : Via la Ligne de Commande
```bash
# 1. Créer un nouveau repo sur GitHub.com (via navigateur)
#    Aller sur github.com → New Repository → NyangaBudget

# 2. Lier le repo local au remote
git remote add origin https://github.com/VOTRE-USERNAME/NyangaBudget.git
git branch -M main
git push -u origin main
```

---

## ✅ ÉTAPE 3 : Déployer sur Render

### 1. Créer un Compte Render
- Aller sur https://render.com
- Cliquer "Get Started for Free"
- S'inscrire avec GitHub (recommandé) ou email

### 2. Connecter GitHub à Render
- Une fois connecté, cliquer "New +"
- Sélectionner "Web Service"
- Cliquer "Connect GitHub"
- Autoriser Render à accéder à vos repos
- Sélectionner le repo `NyangaBudget`

### 3. Configuration du Service Web

Render détectera automatiquement `render.yaml`. Vérifier les paramètres :

```yaml
Name:                nyangabudget
Environment:         Python 3
Region:              Frankfurt (Europe) ou Oregon (US)
Branch:              main
Build Command:       pip install -r requirements.txt
Start Command:       gunicorn app:app
Instance Type:       Free
```

### 4. Variables d'Environnement (Automatiques)
Render générera automatiquement :
- `SECRET_KEY` → Clé secrète Flask
- `PYTHON_VERSION` → 3.11.0

**Pas besoin de les ajouter manuellement !**

### 5. Déployer
- Cliquer "Create Web Service"
- Attendre 3-5 minutes (barre de progression)
- Une fois terminé, votre URL sera : `https://nyangabudget.onrender.com`

---

## ✅ ÉTAPE 4 : Premier Test en Production

### 1. Ouvrir l'Application
Cliquer sur l'URL fournie par Render ou aller sur :
```
https://votre-app.onrender.com
```

**Note :** Le premier chargement peut prendre 30-60 secondes (plan gratuit).

### 2. Se Connecter avec le Compte Admin
```
Email : admin@nyanga.cm
Mot de passe : admin123
```

### 3. Tester les Fonctionnalités Principales
- ✅ Créer une dépense
- ✅ Ajouter un compte bancaire
- ✅ Créer une famille et générer le QR code
- ✅ Ajouter un document au coffre-fort
- ✅ Voir le score de santé financière
- ✅ Créer un rappel et un objectif

---

## ✅ ÉTAPE 5 : Mise à Jour de l'Application

### Déploiement Automatique (Recommandé)
Render redéploie automatiquement à chaque push sur `main` :

```bash
# Après avoir modifié du code
git add .
git commit -m "Description des changements"
git push

# Render va automatiquement :
# 1. Détecter le push
# 2. Rebuild l'application
# 3. Redéployer (2-3 minutes)
```

### Déploiement Manuel
Si vous voulez forcer un redéploiement :
1. Aller sur le dashboard Render
2. Sélectionner votre service
3. Cliquer "Manual Deploy" → "Clear build cache & deploy"

---

## 🔧 Résolution des Problèmes Courants

### ❌ Problème : "Application Error" après déploiement
**Solution :**
1. Aller dans Render Dashboard → Votre service → Logs
2. Lire les logs pour identifier l'erreur
3. Problèmes fréquents :
   - Dépendance manquante → Vérifier `requirements.txt`
   - Erreur de syntaxe Python → Tester localement d'abord
   - Port incorrect → Utiliser `gunicorn app:app` (pas `app.run()`)

### ❌ Problème : "Build Failed"
**Solution :**
```bash
# Tester localement d'abord
pip install -r requirements.txt
python app.py

# Si ça fonctionne localement, le build devrait fonctionner
```

### ❌ Problème : Page blanche / 404
**Solution :**
- Vérifier que `app.py` est bien à la racine du projet (pas dans un sous-dossier)
- Vérifier que le fichier `Procfile` contient : `web: gunicorn app:app`

### ❌ Problème : Base de données vide après redéploiement
**Cause :** Render utilise un système de fichiers éphémère (plan gratuit).
**Solution :**
- Pour une base de données persistante, utiliser PostgreSQL :
  1. Sur Render : New → PostgreSQL
  2. Copier l'URL de connexion
  3. Ajouter dans app.py :
     ```python
     import os
     DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///data/nyanga_v2.db')
     if DATABASE_URL.startswith('postgres://'):
         DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
     app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
     ```
  4. Redéployer

---

## 💰 Tarifs Render (Janvier 2025)

### Plan Gratuit (Actuel)
- ✅ 750 heures/mois (suffisant pour usage personnel)
- ✅ SSL automatique (HTTPS)
- ⚠️ L'app se met en veille après 15 min d'inactivité
- ⚠️ Stockage éphémère (base SQLite réinitialisée au redéploiement)
- ⚠️ 512 MB RAM

### Plan Starter ($7/mois)
- ✅ Toujours actif (pas de mise en veille)
- ✅ Stockage persistant
- ✅ 1 GB RAM
- ✅ Domaine personnalisé gratuit

### Plan Pro ($25/mois)
- ✅ 4 GB RAM
- ✅ Scaling automatique
- ✅ Support prioritaire

**Recommandation :** Commencer avec le plan gratuit, passer à Starter si > 20 utilisateurs.

---

## 🌍 Configuration d'un Domaine Personnalisé (Optionnel)

### 1. Acheter un Domaine
- Namecheap : https://www.namecheap.com (~$10/an)
- OVH : https://www.ovh.com (~8€/an)
- Google Domains : https://domains.google

### 2. Configurer le DNS
Dans votre registrar de domaine, ajouter un enregistrement CNAME :
```
Type:  CNAME
Name:  @ (ou www)
Value: votre-app.onrender.com
TTL:   Automatic
```

### 3. Ajouter le Domaine dans Render
1. Dashboard Render → Votre service → Settings
2. Section "Custom Domain"
3. Cliquer "Add Custom Domain"
4. Entrer : `www.nyangabudget.cm` (exemple)
5. Render configurera automatiquement le SSL (HTTPS)

**Délai de propagation DNS :** 1-24 heures

---

## 📊 Monitoring & Performance

### 1. Voir les Logs en Temps Réel
```bash
# Sur Render Dashboard → Votre service → Logs
# Ou via CLI :
render logs --tail
```

### 2. Statistiques d'Utilisation
- Dashboard Render → Votre service → Metrics
- Voir : CPU, RAM, Bandwidth, Requests/sec

### 3. Alertes (Plan Starter+)
Configurer des alertes email si :
- L'application crash
- CPU > 80%
- RAM > 80%

---

## 🔐 Sécurité en Production

### 1. Changer le Mot de Passe Admin
**Important :** Après le premier déploiement, se connecter et créer un nouvel utilisateur admin avec un mot de passe fort.

### 2. Activer HTTPS (Automatique sur Render)
Render fournit automatiquement un certificat SSL Let's Encrypt.

### 3. Variables d'Environnement Sensibles
Ne jamais commit :
- Mots de passe
- Clés API
- Secret keys

Utiliser les "Environment Variables" de Render à la place.

### 4. Backup de la Base de Données
Si vous utilisez PostgreSQL sur Render :
```bash
# Backup automatique (Plan Pro)
# Ou manuel via :
pg_dump DATABASE_URL > backup_$(date +%Y%m%d).sql
```

---

## 🎉 Félicitations !

Votre application **NyangaBudget 2.0** est maintenant en ligne et accessible au monde entier !

### Prochaines Étapes (Optionnelles)
1. ✅ Partager l'URL avec vos proches
2. ✅ Créer un compte utilisateur pour chaque membre de la famille
3. ✅ Tester la fonctionnalité d'invitation familiale
4. ✅ Configurer un domaine personnalisé
5. ✅ Passer au plan Starter si vous avez > 10 utilisateurs actifs
6. ✅ Migrer vers PostgreSQL pour persistence des données

---

## 📞 Support

- **GitHub Issues :** https://github.com/votre-username/NyangaBudget/issues
- **Documentation :** README.md
- **Email Support :** support@nyangabudget.cm

---

**Propulsé par JoYed'S** 🚀

_Guide créé avec ❤️ pour faciliter votre déploiement_
