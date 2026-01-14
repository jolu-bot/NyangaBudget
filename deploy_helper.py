#!/usr/bin/env python3
"""
Script d'aide au déploiement PythonAnywhere
Génère les configurations nécessaires et vérifie l'environnement
"""

import os
import sys
import secrets
from pathlib import Path

def print_header(text):
    """Affiche un header stylisé"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def generate_secret_key():
    """Génère une SECRET_KEY sécurisée"""
    print_header("🔐 Génération SECRET_KEY")
    key = secrets.token_urlsafe(32)
    print(f"Votre SECRET_KEY sécurisée :\n")
    print(f"SECRET_KEY={key}")
    print("\n⚠️  IMPORTANT : Copiez cette clé dans votre fichier .env")
    print("⚠️  Ne partagez JAMAIS cette clé publiquement !")
    return key

def check_files():
    """Vérifie la présence des fichiers importants"""
    print_header("📁 Vérification des fichiers")
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        'templates/base.html',
        'static/style.css',
        'static/navbar-modern.css',
        'static/dashboard-modern.css',
        'static/forms-modern.css'
    ]
    
    optional_files = [
        '.env',
        'data/nyanga.db'
    ]
    
    all_good = True
    
    print("Fichiers requis :")
    for file in required_files:
        exists = Path(file).exists()
        status = "✅" if exists else "❌"
        print(f"  {status} {file}")
        if not exists:
            all_good = False
    
    print("\nFichiers optionnels (créés au déploiement) :")
    for file in optional_files:
        exists = Path(file).exists()
        status = "✅" if exists else "⚠️ "
        print(f"  {status} {file}")
    
    return all_good

def check_directories():
    """Vérifie la présence des dossiers importants"""
    print_header("📂 Vérification des dossiers")
    
    directories = [
        'static',
        'templates',
        'static/images',
        'data',
        'uploads',
        'uploads/vault',
        'uploads/heritage',
        'uploads/receipts'
    ]
    
    for directory in directories:
        path = Path(directory)
        exists = path.exists()
        status = "✅" if exists else "📁"
        print(f"  {status} {directory}")
        if not exists:
            print(f"      → Créer avec : mkdir -p {directory}")

def analyze_requirements():
    """Analyse le fichier requirements.txt"""
    print_header("📦 Analyse des dépendances")
    
    req_file = Path('requirements.txt')
    if not req_file.exists():
        print("❌ requirements.txt introuvable !")
        return
    
    with open(req_file, 'r') as f:
        lines = f.readlines()
    
    packages = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    
    print(f"Nombre total de packages : {len(packages)}")
    print("\nPackages principaux détectés :")
    
    key_packages = ['Flask', 'SQLAlchemy', 'gunicorn', 'cryptography', 'plotly', 'pytesseract']
    for pkg in key_packages:
        found = any(pkg.lower() in p.lower() for p in packages)
        status = "✅" if found else "⚠️ "
        print(f"  {status} {pkg}")

def generate_wsgi_config(username):
    """Génère un template de configuration WSGI"""
    print_header("🌐 Génération configuration WSGI")
    
    wsgi_template = f"""# /var/www/{username}_pythonanywhere_com_wsgi.py

import sys
import os
from dotenv import load_dotenv

# Chemin du projet
path = '/home/{username}/NyangaBudget'
if path not in sys.path:
    sys.path.insert(0, path)

# Charger variables d'environnement
dotenv_path = os.path.join(path, '.env')
load_dotenv(dotenv_path)

# Activer environnement virtuel
os.environ['VIRTUAL_ENV'] = '/home/{username}/.virtualenvs/nyangabudget-env'
activate_this = os.path.join(os.environ['VIRTUAL_ENV'], 'bin/activate_this.py')

with open(activate_this) as f:
    exec(f.read(), {{'__file__': activate_this}})

# Importer application Flask
from app import app as application

# Configuration production
application.config['DEBUG'] = False
application.config['ENV'] = 'production'
"""
    
    print("Configuration WSGI générée :")
    print("\n" + "-"*60)
    print(wsgi_template)
    print("-"*60)
    
    # Sauvegarder dans un fichier
    output_file = Path('passenger_wsgi_template.py')
    with open(output_file, 'w') as f:
        f.write(wsgi_template)
    
    print(f"\n✅ Template sauvegardé dans : {output_file}")
    print(f"⚠️  Remplacer '{username}' par votre vrai username PythonAnywhere")

def check_env_variables():
    """Vérifie les variables d'environnement nécessaires"""
    print_header("🔧 Variables d'environnement requises")
    
    env_vars = {
        'SECRET_KEY': 'Clé secrète Flask (OBLIGATOIRE)',
        'DATABASE_URL': 'URL base de données',
        'FLASK_ENV': 'Environnement (production)',
        'FLASK_DEBUG': 'Mode debug (0 ou False)',
        'MAX_CONTENT_LENGTH': 'Taille max upload (16777216)',
    }
    
    print("Variables à définir dans .env :")
    for var, description in env_vars.items():
        print(f"  • {var:25} → {description}")
    
    print("\nVariables optionnelles :")
    optional = {
        'OPENAI_API_KEY': 'Pour OCR intelligent',
        'MAIL_SERVER': 'Pour notifications email',
        'MAIL_USERNAME': 'Email expéditeur',
        'MAIL_PASSWORD': 'Mot de passe email'
    }
    
    for var, description in optional.items():
        print(f"  • {var:25} → {description}")

def generate_deployment_commands(username):
    """Génère les commandes de déploiement"""
    print_header("🚀 Commandes de déploiement")
    
    commands = f"""
# 1. Cloner le repository
git clone https://github.com/jolu-bot/NyangaBudget.git
cd NyangaBudget

# 2. Créer environnement virtuel
mkvirtualenv --python=/usr/bin/python3.10 nyangabudget-env
workon nyangabudget-env

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Créer fichier .env
nano .env
# (Copier le contenu de .env.example et remplir les valeurs)

# 5. Créer dossiers nécessaires
mkdir -p data
mkdir -p uploads/vault uploads/heritage uploads/receipts
chmod -R 755 uploads/

# 6. Initialiser base de données
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✅ Base de données créée !")
EOF

# 7. Vérifier installation
python3 -c "from app import app; print('✅ Import OK')"

# 8. Dans Web tab PythonAnywhere :
#    - Add new web app → Manual configuration → Python 3.10
#    - Configurer WSGI (voir passenger_wsgi_template.py)
#    - Source code: /home/{username}/NyangaBudget
#    - Virtualenv: /home/{username}/.virtualenvs/nyangabudget-env
#    - Static files: /static/ → /home/{username}/NyangaBudget/static/
#    - Static files: /uploads/ → /home/{username}/NyangaBudget/uploads/
#    - Reload app

# 9. Tester
curl https://{username}.pythonanywhere.com
"""
    
    print(commands)
    
    # Sauvegarder dans un fichier
    output_file = Path('deploy_commands.sh')
    with open(output_file, 'w') as f:
        f.write(commands.strip())
    
    print(f"\n✅ Commandes sauvegardées dans : {output_file}")

def main():
    """Fonction principale"""
    print("\n" + "🎯"*30)
    print(" "*20 + "NYANGABUDGET 2.0")
    print(" "*15 + "Assistant Déploiement PythonAnywhere")
    print("🎯"*30)
    
    # Menu
    print("\nQue voulez-vous faire ?")
    print("  1. Générer SECRET_KEY")
    print("  2. Vérifier fichiers du projet")
    print("  3. Vérifier dossiers")
    print("  4. Analyser dépendances")
    print("  5. Générer configuration WSGI")
    print("  6. Afficher variables d'environnement requises")
    print("  7. Générer commandes de déploiement")
    print("  8. Tout vérifier (recommandé)")
    print("  0. Quitter")
    
    choice = input("\nVotre choix : ").strip()
    
    if choice == '1':
        generate_secret_key()
    elif choice == '2':
        check_files()
    elif choice == '3':
        check_directories()
    elif choice == '4':
        analyze_requirements()
    elif choice == '5':
        username = input("Entrez votre username PythonAnywhere : ").strip()
        if username:
            generate_wsgi_config(username)
        else:
            print("❌ Username requis !")
    elif choice == '6':
        check_env_variables()
    elif choice == '7':
        username = input("Entrez votre username PythonAnywhere : ").strip()
        if username:
            generate_deployment_commands(username)
        else:
            print("❌ Username requis !")
    elif choice == '8':
        # Tout vérifier
        generate_secret_key()
        files_ok = check_files()
        check_directories()
        analyze_requirements()
        check_env_variables()
        
        username = input("\nEntrez votre username PythonAnywhere (optionnel) : ").strip()
        if username:
            generate_wsgi_config(username)
            generate_deployment_commands(username)
        
        print_header("📊 Résumé")
        if files_ok:
            print("✅ Tous les fichiers requis sont présents")
            print("✅ Projet prêt pour le déploiement")
            print("\n📖 Consultez GUIDE_DEPLOIEMENT_PYTHONANYWHERE.md pour les instructions détaillées")
            print("📋 Utilisez CHECKLIST_PYTHONANYWHERE.md pour suivre votre progression")
        else:
            print("⚠️  Certains fichiers sont manquants")
            print("⚠️  Vérifiez votre projet avant de déployer")
    elif choice == '0':
        print("\n👋 Au revoir !")
        sys.exit(0)
    else:
        print("❌ Choix invalide !")
    
    print("\n" + "="*60)
    print("✅ Terminé !")
    print("="*60 + "\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Opération annulée. Au revoir !")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
        sys.exit(1)
