"""
Migration: Ajout colonnes blockchain_hash et prev_hash
Date: 2025-11-01
Description: Ajoute les colonnes blockchain pour traçabilité immuable
"""

from sqlalchemy import text

def upgrade(db):
    """Ajoute les colonnes blockchain_hash et prev_hash aux tables"""
    
    # Depenses
    try:
        db.session.execute(text("""
            ALTER TABLE depenses 
            ADD COLUMN IF NOT EXISTS blockchain_hash VARCHAR(64),
            ADD COLUMN IF NOT EXISTS prev_hash VARCHAR(64)
        """))
        print("[OK] Colonnes blockchain ajoutées à depenses")
    except Exception as e:
        print(f"[INFO] Depenses: {e}")
    
    # Revenus
    try:
        db.session.execute(text("""
            ALTER TABLE revenus 
            ADD COLUMN IF NOT EXISTS blockchain_hash VARCHAR(64),
            ADD COLUMN IF NOT EXISTS prev_hash VARCHAR(64)
        """))
        print("[OK] Colonnes blockchain ajoutées à revenus")
    except Exception as e:
        print(f"[INFO] Revenus: {e}")
    
    db.session.commit()
    print("[OK] Migration blockchain terminée")

if __name__ == "__main__":
    print("Cette migration doit être exécutée depuis l'application Flask")
