# backup_mysql.sh - Script de backup automatique MySQL pour Hostinger
# 
# INSTRUCTIONS:
# 1. Uploader ce fichier sur le serveur Hostinger via SSH
# 2. Modifier les variables ci-dessous avec vos credentials
# 3. Rendre exécutable: chmod +x backup_mysql.sh
# 4. Tester: ./backup_mysql.sh
# 5. Automatiser avec cron (voir ci-dessous)

#!/bin/bash

# ==================== CONFIGURATION ====================

# Base de données
DB_USER="u123456789_nyanga"
DB_PASS="VotreMotDePasseMySQL"
DB_NAME="u123456789_nyangabudget"
DB_HOST="localhost"

# Répertoire de backup (sera créé si inexistant)
BACKUP_DIR="$HOME/backups/mysql"

# Nombre de jours de conservation des backups
RETENTION_DAYS=7

# Nom de l'application (pour le fichier)
APP_NAME="nyangabudget"

# ==================== SCRIPT ====================

# Créer le répertoire de backup si inexistant
mkdir -p "$BACKUP_DIR"

# Date et heure pour le nom de fichier
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${APP_NAME}_${DATE}.sql"

# Afficher les informations
echo "========================================="
echo "Backup MySQL - NyangaBudget"
echo "========================================="
echo "Date: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Base de données: $DB_NAME"
echo "Fichier: $BACKUP_FILE"
echo ""

# Dump de la base de données
echo "🔄 Sauvegarde en cours..."

mysqldump -h "$DB_HOST" -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" > "$BACKUP_FILE" 2>/dev/null

# Vérifier le résultat
if [ $? -eq 0 ]; then
    # Succès
    FILE_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
    echo "✅ Backup réussi!"
    echo "   Taille: $FILE_SIZE"
    echo "   Fichier: $BACKUP_FILE"
    
    # Compresser le fichier
    echo ""
    echo "🗜️  Compression..."
    gzip "$BACKUP_FILE"
    COMPRESSED_FILE="${BACKUP_FILE}.gz"
    COMPRESSED_SIZE=$(du -h "$COMPRESSED_FILE" | cut -f1)
    echo "✅ Fichier compressé: $COMPRESSED_SIZE"
    
    # Nettoyer les anciens backups
    echo ""
    echo "🧹 Nettoyage des anciens backups (> $RETENTION_DAYS jours)..."
    find "$BACKUP_DIR" -name "${APP_NAME}_*.sql.gz" -mtime +$RETENTION_DAYS -delete
    
    REMAINING=$(ls -1 "$BACKUP_DIR"/${APP_NAME}_*.sql.gz 2>/dev/null | wc -l)
    echo "   Backups restants: $REMAINING"
    
    echo ""
    echo "========================================="
    echo "✅ BACKUP TERMINÉ AVEC SUCCÈS"
    echo "========================================="
    
    exit 0
else
    # Échec
    echo "❌ ERREUR lors du backup!"
    echo "   Vérifiez les identifiants MySQL"
    echo ""
    echo "========================================="
    echo "❌ BACKUP ÉCHOUÉ"
    echo "========================================="
    
    # Supprimer le fichier vide si créé
    rm -f "$BACKUP_FILE"
    
    exit 1
fi

# ==================== AUTOMATISATION CRON ====================
#
# Pour automatiser ce backup quotidiennement à 2h du matin:
#
# 1. Éditer le crontab:
#    crontab -e
#
# 2. Ajouter cette ligne:
#    0 2 * * * /home/u123456789/backup_mysql.sh >> /home/u123456789/backups/backup.log 2>&1
#
# Explication:
#   0 2 * * * = Tous les jours à 2h00
#   Le résultat est enregistré dans backup.log
#
# 3. Vérifier que le cron est actif:
#    crontab -l
#
# ==================== RESTAURATION ====================
#
# Pour restaurer un backup:
#
# 1. Décompresser:
#    gunzip nyangabudget_20250126_020000.sql.gz
#
# 2. Restaurer dans MySQL:
#    mysql -h localhost -u u123456789_nyanga -p u123456789_nyangabudget < nyangabudget_20250126_020000.sql
#
# 3. Vérifier dans phpMyAdmin (hPanel > MySQL Databases > Manage)
