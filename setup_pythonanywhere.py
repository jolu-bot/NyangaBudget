#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'assistance pour le déploiement sur PythonAnywhere
Génère automatiquement les clés et prépare les fichiers de configuration
"""

import secrets
from pathlib import Path


def print_header(title):
    """Afficher un titre formaté"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def print_section(title):
    """Afficher une section"""
    print(f"\n{'─' * 80}")
    print(f"📋 {title}")
    print('─' * 80)


def generate_secret_key():
    """Générer une clé secrète Flask (64 caractères)"""
    return secrets.token_hex(32)


def generate_encryption_key():
    """Générer une clé de cryptage (32 caractères exactement)"""
    return secrets.token_urlsafe(32)[:32]


def main():
    """Fonction principale"""
    print_header("🐍 Configuration PythonAnywhere - NyangaBudget")
    
    print("Ce script va vous aider à configurer votre application pour PythonAnywhere.")
    print("\n📝 Vous aurez besoin des informations suivantes :")
    print("   • Votre nom d'utilisateur PythonAnywhere")
    print("   • Votre mot de passe MySQL PythonAnywhere")
    print("   • Le nom de votre base de données MySQL\n")
    
    input("Appuyez sur ENTRÉE pour continuer...")
    
    # ============================================
    # ÉTAPE 1 : Informations utilisateur
    # ============================================
    print_section("ÉTAPE 1 : Informations PythonAnywhere")
    
    username = input("👤 Votre nom d'utilisateur PythonAnywhere : ").strip()
    if not username:
        print("❌ Le nom d'utilisateur est obligatoire !")
        return
    
    mysql_password = input("🔑 Votre mot de passe MySQL : ").strip()
    if not mysql_password:
        print("❌ Le mot de passe MySQL est obligatoire !")
        return
    
    # Nom de la base par défaut
    default_db = f"{username}$nyangabudget"
    db_name = input(f"💾 Nom de la base de données [{default_db}] : ").strip() or default_db
    
    # ============================================
    # ÉTAPE 2 : Génération des clés
    # ============================================
    print_section("ÉTAPE 2 : Génération des clés de sécurité")
    
    secret_key = generate_secret_key()
    encryption_key = generate_encryption_key()
    
    print("✅ Clés générées avec succès !")
    print(f"   • SECRET_KEY : {secret_key[:20]}... (64 caractères)")
    print(f"   • ENCRYPTION_KEY : {encryption_key[:20]}... (32 caractères)")
    
    # ============================================
    # ÉTAPE 3 : Création du fichier .env
    # ============================================
    print_section("ÉTAPE 3 : Création du fichier .env")
    
    env_content = f"""# Configuration PythonAnywhere - NyangaBudget
# Généré automatiquement le {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV=production

# Base de données MySQL PythonAnywhere
DATABASE_URL=mysql+pymysql://{username}:{mysql_password}@{username}.mysql.pythonanywhere-services.com/{db_name}

# Clé de cryptage pour le coffre-fort
ENCRYPTION_KEY={encryption_key}

# Domaine de l'application
DOMAIN={username}.pythonanywhere.com
"""
    
    env_file = Path('.env.pythonanywhere')
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"✅ Fichier créé : {env_file}")
    
    # ============================================
    # ÉTAPE 4 : Création du fichier WSGI
    # ============================================
    print_section("ÉTAPE 4 : Création du fichier WSGI")
    
    wsgi_content = f"""\"\"\"
WSGI Configuration pour PythonAnywhere - NyangaBudget
Généré automatiquement
\"\"\"

import sys
import os
from pathlib import Path

# Ajouter le dossier du projet au PATH Python
project_home = '/home/{username}/NyangaBudget'
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
"""
    
    wsgi_file = Path('wsgi_pythonanywhere.py')
    with open(wsgi_file, 'w', encoding='utf-8') as f:
        f.write(wsgi_content)
    
    print(f"✅ Fichier créé : {wsgi_file}")
    
    # ============================================
    # ÉTAPE 5 : Récapitulatif
    # ============================================
    print_section("ÉTAPE 5 : Récapitulatif & Prochaines étapes")
    
    print("\n✅ Configuration terminée avec succès !\n")
    print("📁 Fichiers créés :")
    print("   • .env.pythonanywhere")
    print("   • wsgi_pythonanywhere.py (avec votre username)")
    
    print("\n🚀 PROCHAINES ÉTAPES SUR PYTHONANYWHERE :\n")
    print("1️⃣  Téléverser tous les fichiers du projet")
    print("    ou cloner via Git : git clone https://github.com/jolu-bot/NyangaBudget.git\n")

    print("2️⃣  Copier .env.pythonanywhere vers .env :")
    print("    cp .env.pythonanywhere .env\n")
    
    print("3️⃣  Créer l'environnement virtuel :")
    print("    mkvirtualenv --python=/usr/bin/python3.10 nyanga_env")
    print("    workon nyanga_env")
    print("    pip install -r requirements.txt\n")
    
    print("4️⃣  Initialiser la base de données :")
    print("    python3 << EOF")
    print("    from app import app, db")
    print("    with app.app_context():")
    print("        db.create_all()")
    print("        print('✅ Base initialisée')")
    print("    EOF\n")
    
    print("5️⃣  Configurer l'application Web :")
    print(f"    • Path to WSGI : /home/{username}/NyangaBudget/wsgi_pythonanywhere.py")
    print(f"    • Virtualenv : /home/{username}/.virtualenvs/nyanga_env")
    print(f"    • Static files : /static/ → /home/{username}/NyangaBudget/static\n")
    
    print("6️⃣  Recharger l'application et tester !")
    print(f"    🌐 https://{username}.pythonanywhere.com\n")
    
    print("📖 Guide complet : DEPLOIEMENT_PYTHONANYWHERE.md")
    
    print("\n" + "=" * 80)
    print("✨ Bon déploiement ! ✨")
    print("=" * 80 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Configuration annulée par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur : {e}")
