# -*- coding: utf-8 -*-
"""
Script d'assistance au déploiement Hostinger
Ce script vous aide à configurer votre déploiement étape par étape
"""

import os
import secrets
from pathlib import Path


def print_header(title):
    """Afficher un titre formaté"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_step(step, description):
    """Afficher une étape"""
    print(f"\n{'=' * 70}")
    print(f"ÉTAPE {step}: {description}")
    print('=' * 70)


def generate_secret_key():
    """Générer une clé secrète Flask"""
    return secrets.token_hex(32)


def generate_encryption_key():
    """Générer une clé de cryptage de 32 caractères"""
    return secrets.token_urlsafe(32)[:32]


def create_env_production():
    """Créer le fichier .env.production avec les informations de l'utilisateur"""
    print_header("🔧 CONFIGURATION DU FICHIER .env.production")

    print("Je vais vous aider à créer votre fichier de configuration production.")
    print("\n⚠️  IMPORTANT: Préparez les informations suivantes depuis hPanel:\n")
    print("  - Nom de la base MySQL")
    print("  - Utilisateur MySQL")
    print("  - Mot de passe MySQL")
    print("  - Votre domaine\n")

    input("Appuyez sur ENTRÉE quand vous êtes prêt...")

    # Générer les clés
    secret_key = generate_secret_key()
    encryption_key = generate_encryption_key()

    print("\n✅ Clés secrètes générées automatiquement!\n")

    # Demander les informations MySQL
    print("\n📋 Configuration MySQL Hostinger:")
    print("-" * 70)

    db_name = input("Nom de la base (ex: u123456789_nyangabudget): ").strip()
    db_user = input("Utilisateur MySQL (ex: u123456789_nyanga): ").strip()
    db_pass = input("Mot de passe MySQL: ").strip()
    db_host = input("Hôte MySQL (généralement 'localhost'): ").strip() or "localhost"
    db_port = input("Port MySQL (généralement '3306'): ").strip() or "3306"

    # Demander le domaine
    print("\n🌐 Configuration Domaine:")
    print("-" * 70)
    domain = input("Votre domaine (ex: monsite.com): ").strip()

    # Créer le contenu du fichier .env
    env_content = f"""# Configuration Production Hostinger - NyangaBudget
# Généré automatiquement le {os.popen('date /t').read().strip()}

# ==================== BASE DE DONNÉES ====================
DATABASE_URL=mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}

# ==================== SÉCURITÉ ====================
SECRET_KEY={secret_key}
MASTER_ENCRYPTION_KEY={encryption_key}

# ==================== MODE ====================
FLASK_ENV=production
DEBUG=False

# ==================== DOMAINE ====================
SERVER_NAME={domain}

# ==================== EMAIL (Optionnel - à configurer plus tard) ====================
# MAIL_SERVER=smtp.hostinger.com
# MAIL_PORT=587
# MAIL_USE_TLS=True
# MAIL_USERNAME=noreply@{domain}
# MAIL_PASSWORD=votre_mot_de_passe_email

# ==================== BACKUP ====================
# BACKUP_ENABLED=True
# BACKUP_FREQUENCY=daily
"""

    # Sauvegarder le fichier
    env_path = Path('.env.production')
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)

    print("\n✅ Fichier .env.production créé avec succès!")
    print(f"📁 Emplacement: {env_path.absolute()}\n")

    print("⚠️  IMPORTANT: Gardez ce fichier SECRET!")
    print("   Ne le commitez JAMAIS sur GitHub!\n")

    return env_path


def configure_deploy_script():
    """Configurer le script deploy_hostinger.py"""
    print_step(2, "CONFIGURATION DU SCRIPT DE DÉPLOIEMENT FTP")

    print("\n📋 Configuration FTP Hostinger:")
    print("-" * 70)
    print("\nRetournez dans hPanel > Fichiers > Comptes FTP\n")

    ftp_host = input("Hôte FTP (ex: ftp.monsite.com): ").strip()
    ftp_user = input("Utilisateur FTP (ex: u123456789): ").strip()
    ftp_pass = input("Mot de passe FTP: ").strip()

    print("\n📂 Chemin de destination:")
    print("   Pour le domaine principal: /public_html/nyangabudget")
    print("   Pour un sous-domaine: /domains/budget.monsite.com/public_html\n")

    ftp_dir = input("Chemin de destination: ").strip()

    # Lire le fichier actuel
    deploy_file = Path('deploy_hostinger.py')
    if not deploy_file.exists():
        print("\n❌ Erreur: deploy_hostinger.py n'existe pas!")
        return False

    with open(deploy_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remplacer les valeurs
    content = content.replace(
        "FTP_HOST = 'ftp.votredomaine.com'",
        f"FTP_HOST = '{ftp_host}'"
    )
    content = content.replace(
        "FTP_USER = 'u123456789'",
        f"FTP_USER = '{ftp_user}'"
    )
    content = content.replace(
        "FTP_PASS = 'VotreMotDePasseFTP'",
        f"FTP_PASS = '{ftp_pass}'"
    )
    content = content.replace(
        "FTP_REMOTE_DIR = '/public_html/nyangabudget'",
        f"FTP_REMOTE_DIR = '{ftp_dir}'"
    )

    # Sauvegarder
    with open(deploy_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print("\n✅ Script deploy_hostinger.py configuré!")
    return True


def show_next_steps():
    """Afficher les prochaines étapes"""
    print_header("🚀 PROCHAINES ÉTAPES")

    print(r"""
1. DÉPLOYER LES FICHIERS:
   > .\.venv\Scripts\python.exe deploy_hostinger.py

2. SE CONNECTER EN SSH:
   > ssh votre_utilisateur@votredomaine.com

3. SUR LE SERVEUR, EXÉCUTER:
   cd public_html/nyangabudget
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

4. COPIER LE FICHIER .env:
   Uploadez .env.production vers le serveur et renommez-le en .env

5. INITIALISER LA BASE:
   python3 -c "from app import db, app; app.app_context().push(); db.create_all()"

6. REDÉMARRER:
   mkdir -p tmp
   touch tmp/restart.txt

7. TESTER:
   Ouvrez https://votredomaine.com/nyangabudget dans votre navigateur

Pour plus de détails, consultez: GUIDE_DEPLOIEMENT_PRATIQUE.md
    """)


def main():
    """Fonction principale"""
    print_header("🌟 ASSISTANT DE DÉPLOIEMENT HOSTINGER - NyangaBudget")

    print("""
Cet assistant va vous aider à configurer votre déploiement sur Hostinger.

Prérequis:
  ✅ Compte Hostinger actif
  ✅ Base de données MySQL créée dans hPanel
  ✅ Compte FTP configuré
  ✅ Application testée en local

Temps estimé: 10-15 minutes
""")

    response = input("\nVoulez-vous continuer? (o/n): ").lower()
    if response != 'o':
        print("\nDéploiement annulé.")
        return

    # Étape 1: Créer .env.production
    print_step(1, "CRÉATION DU FICHIER .env.production")
    create_env_production()

    # Étape 2: Configurer deploy_hostinger.py
    if not configure_deploy_script():
        return

    # Afficher les prochaines étapes
    show_next_steps()

    print_header("✅ CONFIGURATION TERMINÉE!")
    print("\nVous êtes maintenant prêt à déployer!")
    print("\nFichiers créés/modifiés:")
    print("  - .env.production")
    print("  - deploy_hostinger.py (mis à jour)")
    print("\n💡 Conseil: Lisez GUIDE_DEPLOIEMENT_PRATIQUE.md pour les détails.\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDéploiement interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\n❌ Erreur: {str(e)}")
        print("\nConsultez GUIDE_DEPLOIEMENT_PRATIQUE.md pour l'aide.")
