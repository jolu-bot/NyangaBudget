# ⚡ DÉPLOIEMENT EXPRESS - 5 MINUTES

## 🎯 Objectif
Déployer NyangaBudget 2.0 sur PythonAnywhere en **5 minutes chrono**.

---

## ✅ Prérequis (1 min)

- [ ] Compte [PythonAnywhere](https://www.pythonanywhere.com) (gratuit OK)
- [ ] Git installé localement
- [ ] Python 3.10+ installé

---

## 🚀 Étapes Express

### 1️⃣ Préparation Locale (1 min)

```bash
# Dans votre dossier projet
python deploy_helper.py
# Choisir option 8 : "Tout vérifier"
# Copier la SECRET_KEY générée
```

### 2️⃣ Sur PythonAnywhere (2 min)

#### A. Console Bash
```bash
git clone https://github.com/jolu-bot/NyangaBudget.git
cd NyangaBudget
mkvirtualenv --python=/usr/bin/python3.10 nyangabudget-env
pip install -r requirements.txt
```

#### B. Créer .env
```bash
nano .env
```

Copier-coller (remplacer SECRET_KEY) :
```
SECRET_KEY=VOTRE_CLE_GENEREE_PAR_LE_SCRIPT
DATABASE_URL=sqlite:///data/nyanga.db
FLASK_ENV=production
FLASK_DEBUG=0
```

Sauver : `Ctrl+O` → `Enter` → `Ctrl+X`

#### C. Initialiser DB
```bash
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ DB créée !")
EOF
```

### 3️⃣ Configuration Web App (2 min)

#### A. Créer Web App
- Web tab → **Add new web app**
- **Manual configuration** → **Python 3.10**

#### B. WSGI File (copier-coller - remplacer USERNAME)
```python
import sys
import os
from dotenv import load_dotenv

path = '/home/USERNAME/NyangaBudget'
if path not in sys.path:
    sys.path.insert(0, path)

load_dotenv(os.path.join(path, '.env'))

os.environ['VIRTUAL_ENV'] = '/home/USERNAME/.virtualenvs/nyangabudget-env'
activate_this = os.path.join(os.environ['VIRTUAL_ENV'], 'bin/activate_this.py')

with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

from app import app as application
application.config['DEBUG'] = False
```

#### C. Configurer Chemins (Web tab)
- **Source code** : `/home/USERNAME/NyangaBudget`
- **Working directory** : `/home/USERNAME/NyangaBudget`
- **Virtualenv** : `/home/USERNAME/.virtualenvs/nyangabudget-env`

#### D. Static Files (Web tab)
| URL | Directory |
|-----|-----------|
| `/static/` | `/home/USERNAME/NyangaBudget/static/` |
| `/uploads/` | `/home/USERNAME/NyangaBudget/uploads/` |

### 4️⃣ Lancement
- **Reload** app (bouton vert Web tab)
- Ouvrir : `https://USERNAME.pythonanywhere.com`
- Login : `admin@nyanga.cm` / `admin123`

---

## ✅ Checklist Rapide

- [ ] Script `deploy_helper.py` exécuté
- [ ] SECRET_KEY copiée
- [ ] Repository cloné sur PythonAnywhere
- [ ] Virtualenv créé et actif
- [ ] Dépendances installées
- [ ] `.env` créé avec SECRET_KEY
- [ ] Base de données initialisée
- [ ] Web app créée (Manual + Python 3.10)
- [ ] WSGI configuré (USERNAME remplacé)
- [ ] Chemins configurés (3 champs)
- [ ] Static files mappés (2 lignes)
- [ ] App Reloadée
- [ ] Site accessible et login fonctionne

---

## 🐛 Problème ?

### App ne charge pas
```bash
# Voir logs
tail -f /var/log/USERNAME.pythonanywhere.com.error.log
```

### CSS ne charge pas
- Vérifier Static files dans Web tab
- Vider cache navigateur (Ctrl+Shift+R)

### DB erreur
```bash
cd ~/NyangaBudget
python3
>>> from app import app, db
>>> with app.app_context(): db.create_all()
```

---

## 📚 Documentation Complète

Si besoin de plus de détails :

1. **[GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md](GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md)** - Guide détaillé
2. **[CHECKLIST_PYTHONANYWHERE.md](CHECKLIST_PYTHONANYWHERE.md)** - 50+ items
3. **[PROJET_COMPLET.md](PROJET_COMPLET.md)** - Vue d'ensemble
4. **[INDEX_COMPLETE.md](INDEX_COMPLETE.md)** - Navigation docs

---

## 🎉 Terminé !

**URL** : `https://USERNAME.pythonanywhere.com`  
**Login** : `admin@nyanga.cm` / `admin123`

⚠️ **Changer le mot de passe admin après premier login !**

---

**Durée réelle** : 5-10 minutes  
**Difficulté** : ⭐⭐ Facile avec ce guide  
**Version** : NyangaBudget 2.0

---

*Guide Express - Janvier 2026*
