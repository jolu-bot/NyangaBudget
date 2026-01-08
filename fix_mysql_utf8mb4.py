#!/usr/bin/env python3
"""
Script de conversion des tables MySQL en utf8mb4 pour support complet des émojis
"""
import os
import pymysql

# Configuration depuis DATABASE_URL
DATABASE_URL = os.environ.get('DATABASE_URL', 
    'mysql+pymysql://Jolubot:Jody%21%40%3EYed@Jolubot.mysql.pythonanywhere-services.com/Jolubot$nyangabudget')

# Parser l'URL
if 'mysql+pymysql://' in DATABASE_URL:
    parts = DATABASE_URL.replace('mysql+pymysql://', '').split('@')
    user_pass = parts[0].split(':')
    host_db = parts[1].split('/')
    
    username = user_pass[0]
    # Décoder le mot de passe URL-encodé
    password = user_pass[1].replace('%21', '!').replace('%40', '@').replace('%3E', '>')
    host = host_db[0]
    database = host_db[1]
    
    print(f"🔄 Connexion à MySQL...")
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
