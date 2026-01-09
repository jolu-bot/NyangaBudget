"""
Script de migration pour ajouter les champs manquants au modèle Rappel
- date_rappel: Date du rappel avant échéance
- notifie: Indicateur pour éviter les notifications multiples

Usage: python migrate_rappel_fields.py
"""

import pymysql
from urllib.parse import unquote

# Configuration MySQL PythonAnywhere
MYSQL_HOST = 'Jolubot.mysql.pythonanywhere-services.com'
MYSQL_USER = 'Jolubot'
MYSQL_PASSWORD = unquote('Jody%21%40%3EYed')  # Jody!@>Yed
MYSQL_DB = 'Jolubot$nyangabudget'


def migrate_rappel_fields():
    """Ajouter les champs date_rappel et notifie à la table rappels"""
    
    try:
        # Connexion MySQL
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        print(f"[INFO] Connexion à MySQL: {MYSQL_DB}")
        
        with connection.cursor() as cursor:
            # Vérifier si les colonnes existent déjà
            cursor.execute("""
                SELECT COLUMN_NAME 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = %s 
                  AND TABLE_NAME = 'rappels'
                  AND COLUMN_NAME IN ('date_rappel', 'notifie')
            """, (MYSQL_DB,))
            
            existing_columns = [row['COLUMN_NAME'] for row in cursor.fetchall()]
            
            # Ajouter date_rappel si elle n'existe pas
            if 'date_rappel' not in existing_columns:
                print("[INFO] Ajout de la colonne date_rappel...")
                cursor.execute("""
                    ALTER TABLE rappels 
                    ADD COLUMN date_rappel DATETIME DEFAULT NULL 
                    AFTER date_echeance
                """)
                print("  ✅ Colonne date_rappel ajoutée")
                
                # Initialiser date_rappel = date_echeance - 1 jour pour les rappels existants
                cursor.execute("""
                    UPDATE rappels 
                    SET date_rappel = DATE_SUB(date_echeance, INTERVAL 1 DAY)
                    WHERE date_rappel IS NULL
                """)
                print("  ✅ Dates de rappel initialisées (échéance - 1 jour)")
            else:
                print("[INFO] Colonne date_rappel existe déjà")
            
            # Ajouter notifie si elle n'existe pas
            if 'notifie' not in existing_columns:
                print("[INFO] Ajout de la colonne notifie...")
                cursor.execute("""
                    ALTER TABLE rappels 
                    ADD COLUMN notifie TINYINT(1) DEFAULT 0 
                    AFTER est_complete
                """)
                print("  ✅ Colonne notifie ajoutée")
            else:
                print("[INFO] Colonne notifie existe déjà")
            
            # Commit des modifications
            connection.commit()
            
            # Vérifier la structure finale
            cursor.execute("""
                SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s 
                  AND TABLE_NAME = 'rappels'
                ORDER BY ORDINAL_POSITION
            """, (MYSQL_DB,))
            
            print("\n[INFO] Structure finale de la table rappels:")
            print("-" * 70)
            for col in cursor.fetchall():
                nullable = "NULL" if col['IS_NULLABLE'] == 'YES' else "NOT NULL"
                default = f"DEFAULT {col['COLUMN_DEFAULT']}" if col['COLUMN_DEFAULT'] else ""
                print(f"  {col['COLUMN_NAME']:20} {col['COLUMN_TYPE']:20} {nullable:10} {default}")
            print("-" * 70)
            
            print("\n[SUCCESS] Migration terminée avec succès ! ✅")
        
        connection.close()
        
    except Exception as e:
        print(f"\n[ERROR] Erreur lors de la migration: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    print("=" * 70)
    print(" MIGRATION BASE DE DONNÉES - Ajout champs Rappel")
    print("=" * 70)
    print()
    
    success = migrate_rappel_fields()
    
    if success:
        print("\n✅ Migration réussie !")
        print("   Les champs date_rappel et notifie ont été ajoutés à la table rappels")
    else:
        print("\n❌ Échec de la migration")
        print("   Vérifiez les logs ci-dessus pour plus de détails")
