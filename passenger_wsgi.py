# passenger_wsgi.py - Point d'entrée WSGI pour Hostinger avec Phusion Passenger

import sys
import os

# ==================== CONFIGURATION ENVIRONNEMENT ====================

# Chemin vers l'environnement virtuel Python
# Remplacer 'u123456789' par votre ID utilisateur Hostinger réel
INTERP = os.path.join(os.environ['HOME'], 'nyangabudget_venv', 'bin', 'python3')

# Si Python actuel n'est pas celui du virtualenv, basculer
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Ajouter le répertoire de l'application au PYTHONPATH
sys.path.insert(0, os.path.dirname(__file__))

# ==================== CHARGEMENT VARIABLES D'ENVIRONNEMENT ====================

# Charger les variables depuis .env (si python-dotenv est installé)
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("[OK] Variables d'environnement chargées depuis .env")
except ImportError:
    print("[WARNING] python-dotenv non installé - Utiliser des variables d'environnement système")

# ==================== VARIABLES D'ENVIRONNEMENT PAR DÉFAUT ====================

# Si les variables ne sont pas définies dans .env, utiliser ces valeurs
# ⚠️ IMPORTANT: Modifier ces valeurs avec vos vraies credentials Hostinger

if not os.environ.get('FLASK_ENV'):
    os.environ['FLASK_ENV'] = 'production'

if not os.environ.get('DB_HOST'):
    os.environ['DB_HOST'] = 'localhost'

# Clés de sécurité (générer des valeurs uniques en production)
if not os.environ.get('SECRET_KEY'):
    os.environ['SECRET_KEY'] = 'CHANGE-THIS-IN-PRODUCTION-32-CHARS-MIN'

if not os.environ.get('MASTER_ENCRYPTION_KEY'):
    os.environ['MASTER_ENCRYPTION_KEY'] = 'CHANGE-THIS-ENCRYPTION-KEY-32-CHARS'

# ==================== IMPORTATION APPLICATION FLASK ====================

try:
    from app import app as application
    print("[OK] Application Flask chargée avec succès")
except Exception as e:
    print(f"[ERREUR] Impossible de charger l'application Flask: {str(e)}")
    raise

# ==================== POINT D'ENTRÉE WSGI ====================

# Variable 'application' requise par Passenger
# Ne pas renommer cette variable !

if __name__ == "__main__":
    # Mode debug désactivé en production
    application.run(debug=False)
