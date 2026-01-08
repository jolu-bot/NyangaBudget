# NyangaBudget 💰

Application de gestion budgétaire personnelle développée avec Flask.

## 🚀 Déploiement sur PythonAnywhere

L'application est déployée sur : **https://jolubot.pythonanywhere.com**

### Configuration requise

- Python 3.10
- MySQL Database
- Variables d'environnement (voir `.env.pythonanywhere`)

### Installation locale

```bash
# Cloner le projet
git clone https://github.com/jolu-bot/NyangaBudget.git
cd NyangaBudget

# Créer un environnement virtuel
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
# Créer un fichier .env avec :
# DATABASE_URL=votre_url_mysql
# SECRET_KEY=votre_clé_secrète
# ENCRYPTION_KEY=votre_clé_chiffrement

# Initialiser la base de données
python init_mysql.py

# Lancer l'application
python app.py
```

## ✨ Fonctionnalités

- 📊 Gestion des dépenses et revenus
- 💳 Multi-comptes bancaires
- 🎯 Objectifs financiers
- 🏦 Coffre-fort numérique
- 👨‍👩‍👧‍👦 Gestion familiale
- 🔔 Notifications et rappels
- 📈 Statistiques et rapports
- 🌙 Mode sombre
- 🔒 Sécurité CSRF et rate limiting

## 📦 Structure du projet

```
NyangaBudget/
├── app.py                      # Application Flask principale
├── requirements.txt            # Dépendances Python
├── init_mysql.py              # Initialisation base de données
├── wsgi_pythonanywhere.py     # Configuration WSGI
├── setup_pythonanywhere.py    # Script de configuration
├── templates/                 # Templates HTML
├── static/                    # Fichiers statiques (CSS, JS, images)
├── data/                      # Données persistantes
├── instance/                  # Instance Flask
└── uploads/                   # Fichiers uploadés
```

## 🔧 Technologies utilisées

- **Backend**: Flask, SQLAlchemy
- **Base de données**: MySQL (PyMySQL)
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Sécurité**: Flask-Limiter, CSRF Protection
- **Déploiement**: PythonAnywhere

## 👨‍💻 Auteur

**JoYed'S**

## 📄 Licence

Projet personnel - Tous droits réservés
