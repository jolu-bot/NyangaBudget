"""
WSGI Configuration pour PythonAnywhere - NyangaBudget
Généré automatiquement
"""

import sys
import os
from pathlib import Path

# Ajouter le dossier du projet au PATH Python
project_home = '/home/Jolubot/NyangaBudget'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Charger les variables d'environnement depuis .env
env_path = Path(project_home) / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip()

# Importer l'application Flask
from app import app as application

# Point d'entrée WSGI
if __name__ == '__main__':
    application.run()
