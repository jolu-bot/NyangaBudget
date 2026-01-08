#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour initialiser la base de données MySQL sur PythonAnywhere
"""
import os
import sys

# Définir explicitement la connexion MySQL
os.environ['DATABASE_URL'] = 'mysql+pymysql://Jolubot:Jody%21%40%3EYed@Jolubot.mysql.pythonanywhere-services.com/Jolubot$nyangabudget'

# Importer après avoir défini la variable d'environnement
from app import app, db

def init_database():
    """Initialiser toutes les tables MySQL"""
    try:
        with app.app_context():
            print("🔄 Connexion à MySQL...")
            print(f"📍 Base: Jolubot$nyangabudget")
            
            # Créer toutes les tables
            db.create_all()
            
            print("✅ Toutes les tables MySQL ont été créées avec succès!")
            print("\n📋 Tables créées:")
            
            # Lister les tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            for i, table in enumerate(tables, 1):
                print(f"   {i}. {table}")
            
            print(f"\n🎉 Total: {len(tables)} tables")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        return False

if __name__ == '__main__':
    success = init_database()
    sys.exit(0 if success else 1)
