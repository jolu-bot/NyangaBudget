#!/usr/bin/env python3
"""
Script de conversion des tables MySQL en utf8mb4 pour support complet des émojis
"""
import os
import pymysql
from urllib.parse import unquote

# Configuration depuis DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL', 
    'mysql+pymysql://Jolubot:Jody%21%40%3EYed@Jolubot.mysql.pythonanywhere-services.com/Jolubot$nyangabudget')

# Parser l'URL
if 'mysql+pymysql://' in DATABASE_URL:
    # Supprimer le préfixe
    url = DATABASE_URL.replace('mysql+pymysql://', '')
    
    # Séparer credentials et host/db (utiliser rsplit pour éviter les @ dans le mot de passe)
    if '@' in url:
        credentials, host_and_db = url.rsplit('@', 1)  # Split par le DERNIER @
        
        # Parser credentials
        if ':' in credentials:
            username, password_encoded = credentials.split(':', 1)
            # Décoder le mot de passe URL-encodé
            password = unquote(password_encoded)
        else:
            username = credentials
            password = ''
        
        # Parser host et database
        if '/' in host_and_db:
            host, database_with_params = host_and_db.split('/', 1)
            # Retirer les paramètres éventuels (?charset=...)
            database = database_with_params.split('?')[0] if '?' in database_with_params else database_with_params
        else:
            host = host_and_db
            database = ''
            host = host_and_db
            database = ''
    
    if not database:
        print("❌ Impossible d'extraire le nom de la base de données de DATABASE_URL")
        exit(1)
    
    print(f"🔄 Connexion à MySQL...")
    print(f"👤 Utilisateur: {username}")
    print(f"🌐 Hôte: {host}")
    print(f"📍 Base: {database}")
    
    try:
        # Connexion MySQL
        connection = pymysql.connect(
            host=host,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # Convertir la base de données
        print(f"\n🔧 Conversion de la base de données en utf8mb4...")
        cursor.execute(f"ALTER DATABASE `{database}` CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci")
        print(f"✅ Base de données convertie")
        
        # Lister toutes les tables
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\n📋 Tables trouvées: {len(tables)}")
        
        # Convertir chaque table
        for table in tables:
            try:
                print(f"   🔄 Conversion de {table}...", end=' ')
                cursor.execute(f"ALTER TABLE `{table}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
                print(f"✅")
            except Exception as e:
                print(f"❌ Erreur: {e}")
        
        connection.commit()
        
        print(f"\n✅ Toutes les tables ont été converties en utf8mb4!")
        print(f"🎉 Support complet des émojis activé!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print(f"\nVérifiez DATABASE_URL dans .env")
else:
    print("❌ DATABASE_URL invalide ou non trouvée")
    print("Définissez DATABASE_URL avec la chaîne de connexion MySQL")
