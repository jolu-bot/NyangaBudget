# deploy_hostinger.py - Script de déploiement automatique via FTP pour Hostinger
#
# INSTRUCTIONS:
# 1. Installer ftplib: pip install ftplib (inclus dans Python standard)
# 2. Modifier les constantes FTP ci-dessous avec vos identifiants
# 3. Exécuter: python deploy_hostinger.py

import ftplib
import os
import sys
from pathlib import Path
from datetime import datetime

# ==================== CONFIGURATION FTP ====================

# ⚠️ IMPORTANT: Remplacer par vos vrais identifiants Hostinger
FTP_HOST = '92.113.28.219'  # Ex: ftp.nyangabudget.com (sans ftp://)
FTP_USER = 'u173662183'  # Ex: u123456789
FTP_PASS = '!@Jody0.Yed'  # Mot de passe FTP depuis hPanel
FTP_REMOTE_DIR = '/public_html/nyangabudget'  # Chemin distant

# Fichiers et dossiers à EXCLURE de l'upload
EXCLUDE_PATTERNS = [
    '.git',
    '.venv',
    '__pycache__',
    '*.pyc',
    '*.pyo',
    '*.db',
    '*.sqlite',
    '*.sqlite3',
    '*.log',
    'data/',
    '.env',  # Ne pas uploader .env (créer manuellement sur serveur)
    '.gitignore',
    'deploy_hostinger.py',  # Ce script lui-même
]

# Dossiers à créer mais ne pas uploader le contenu
EMPTY_DIRS = [
    'uploads',
    'uploads/vault',
    'uploads/heritage',
    'uploads/receipts',
    'data',
    'logs',
]

# ==================== FONCTIONS ====================


def should_exclude(path):
    """Vérifie si un fichier/dossier doit être exclu"""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path_str:
            return True
    return False


def create_remote_directory(ftp, remote_path):
    """Créer un répertoire distant (récursif)"""
    dirs = remote_path.strip('/').split('/')
    current_path = ''

    for dir_name in dirs:
        if not dir_name:
            continue
        current_path += '/' + dir_name
        try:
            ftp.mkd(current_path)
            print(f"✅ Dossier créé: {current_path}")
        except ftplib.error_perm:
            # Le dossier existe déjà
            pass
        except Exception as e:
            print(f"⚠️  Erreur création dossier {current_path}: {str(e)}")


def upload_file(ftp, local_path, remote_path):
    """Upload un fichier via FTP"""
    try:
        with open(local_path, 'rb') as file:
            ftp.storbinary(f'STOR {remote_path}', file)
        file_size = os.path.getsize(local_path)
        print(f"✅ Uploadé: {local_path.name} ({file_size:,} octets)")
        return True
    except Exception as e:
        print(f"❌ Erreur upload {local_path.name}: {str(e)}")
        return False


def upload_directory(ftp, local_dir, remote_dir, stats):
    """Upload récursif d'un répertoire"""
    local_dir = Path(local_dir)

    # Créer le dossier distant
    create_remote_directory(ftp, remote_dir)

    # Parcourir les fichiers et sous-dossiers
    for item in local_dir.iterdir():
        # Vérifier l'exclusion
        if should_exclude(item):
            print(f"⏭️  Ignoré: {item.name}")
            stats['skipped'] += 1
            continue

        remote_path = f"{remote_dir}/{item.name}"

        if item.is_file():
            # Upload du fichier
            if upload_file(ftp, item, remote_path):
                stats['uploaded'] += 1
            else:
                stats['failed'] += 1

        elif item.is_dir():
            # Récursion pour les sous-dossiers
            print(f"\n📁 Dossier: {item.name}")
            upload_directory(ftp, item, remote_path, stats)


def deploy():
    """Déploiement complet sur Hostinger"""
    print("=" * 60)
    print("🚀 DÉPLOIEMENT NYANGABUDGET SUR HOSTINGER")
    print("=" * 60)
    print(f"\nHôte: {FTP_HOST}")
    print(f"Utilisateur: {FTP_USER}")
    print(f"Destination: {FTP_REMOTE_DIR}")
    print(f"\nDébut: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    # Statistiques
    stats = {
        'uploaded': 0,
        'failed': 0,
        'skipped': 0
    }

    try:
        # Connexion FTP
        print("\n🔌 Connexion au serveur FTP...")
        ftp = ftplib.FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        print("✅ Connecté avec succès!")

        # Afficher le message de bienvenue FTP
        print(f"\n📝 Message serveur: {ftp.getwelcome()}")

        # Aller dans le répertoire de travail
        print(f"\n📂 Navigation vers {FTP_REMOTE_DIR}...")
        try:
            ftp.cwd(FTP_REMOTE_DIR)
        except BaseException:
            # Créer le répertoire s'il n'existe pas
            print(f"📁 Création du répertoire {FTP_REMOTE_DIR}...")
            create_remote_directory(ftp, FTP_REMOTE_DIR)
            ftp.cwd(FTP_REMOTE_DIR)

        # Créer les dossiers vides nécessaires
        print("\n📁 Création des dossiers système...")
        for empty_dir in EMPTY_DIRS:
            create_remote_directory(ftp, f"{FTP_REMOTE_DIR}/{empty_dir}")

        # Upload des fichiers
        print("\n📤 Upload des fichiers...")
        print("-" * 60)

        current_dir = Path('.')
        upload_directory(ftp, current_dir, FTP_REMOTE_DIR, stats)

        # Statistiques finales
        print("\n" + "=" * 60)
        print("📊 STATISTIQUES DE DÉPLOIEMENT")
        print("=" * 60)
        print(f"✅ Fichiers uploadés: {stats['uploaded']}")
        print(f"❌ Échecs: {stats['failed']}")
        print(f"⏭️  Ignorés: {stats['skipped']}")
        print(f"\n🕒 Fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # Fermer la connexion
        ftp.quit()

        # Message final
        print("\n" + "=" * 60)
        if stats['failed'] == 0:
            print("✅ DÉPLOIEMENT TERMINÉ AVEC SUCCÈS!")
        else:
            print("⚠️  DÉPLOIEMENT TERMINÉ AVEC DES ERREURS")
        print("=" * 60)

        print("\n🌐 Application disponible sur:")
        print("   https://votredomaine.com/nyangabudget")
        print("\n📝 PROCHAINES ÉTAPES:")
        print("   1. Se connecter en SSH")
        print("   2. Créer le virtualenv et installer les dépendances")
        print("   3. Créer le fichier .env avec les credentials MySQL")
        print("   4. Redémarrer: touch tmp/restart.txt")
        print("   5. Tester l'application")

        return stats['failed'] == 0

    except ftplib.error_perm as e:
        print(f"\n❌ ERREUR FTP: {str(e)}")
        print("⚠️  Vérifiez vos identifiants FTP dans hPanel > FTP Accounts")
        return False

    except Exception as e:
        print(f"\n❌ ERREUR INATTENDUE: {str(e)}")
        return False


def verify_credentials():
    """Vérifier que les identifiants FTP sont configurés"""
    if 'votredomaine.com' in FTP_HOST or 'VotreMotDePasseFTP' in FTP_PASS:
        print("\n" + "=" * 60)
        print("⚠️  CONFIGURATION REQUISE")
        print("=" * 60)
        print("\nMerci de configurer vos identifiants FTP dans ce fichier:")
        print("  - FTP_HOST: Remplacer par ftp.votredomaine.com")
        print("  - FTP_USER: Votre utilisateur FTP depuis hPanel")
        print("  - FTP_PASS: Votre mot de passe FTP")
        print("  - FTP_REMOTE_DIR: Chemin de destination sur le serveur")
        print("\n📖 Voir DEPLOIEMENT_HOSTINGER.md pour les détails")
        print("=" * 60)
        return False
    return True

# ==================== POINT D'ENTRÉE ====================


if __name__ == '__main__':
    print("\n")
    print("█" * 60)
    print("█" + " " * 58 + "█")
    print("█" + "  NyangaBudget - Déploiement Automatique Hostinger  ".center(58) + "█")
    print("█" + " " * 58 + "█")
    print("█" * 60)
    print("\n")

    # Vérifier la configuration
    if not verify_credentials():
        sys.exit(1)

    # Demander confirmation
    print("⚠️  Ce script va uploader tous les fichiers vers Hostinger.")
    confirmation = input("   Continuer? (oui/non): ").strip().lower()

    if confirmation not in ['oui', 'o', 'yes', 'y']:
        print("\n❌ Déploiement annulé.")
        sys.exit(0)

    # Lancer le déploiement
    success = deploy()

    # Code de sortie
    sys.exit(0 if success else 1)
