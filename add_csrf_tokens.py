#!/usr/bin/env python3
"""
Script pour ajouter automatiquement les tokens CSRF dans tous les templates
Usage: python add_csrf_tokens.py
"""
import os
import re

TEMPLATES_DIR = 'templates'
CSRF_TOKEN = '<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>'

def add_csrf_to_template(filepath):
    """Ajoute le token CSRF après chaque balise <form method="POST">"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si le fichier contient déjà des tokens CSRF
    if 'csrf_token()' in content:
        print(f"  ✓ {os.path.basename(filepath)} - Déjà protégé")
        return False
    
    # Pattern pour trouver les formulaires POST
    pattern = r'(<form[^>]*method=["\']POST["\'][^>]*>)'
    
    def replacer(match):
        form_tag = match.group(1)
        return f"{form_tag}\n                                {CSRF_TOKEN}"
    
    new_content, count = re.subn(pattern, replacer, content, flags=re.IGNORECASE)
    
    if count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✅ {os.path.basename(filepath)} - {count} formulaire(s) protégé(s)")
        return True
    else:
        print(f"  ⊘ {os.path.basename(filepath)} - Aucun formulaire POST trouvé")
        return False

def main():
    print("\n" + "="*60)
    print(" 🔐 Ajout automatique des tokens CSRF")
    print("="*60 + "\n")
    
    if not os.path.exists(TEMPLATES_DIR):
        print(f"❌ Dossier '{TEMPLATES_DIR}' introuvable!")
        return
    
    modified_count = 0
    total_count = 0
    
    for filename in os.listdir(TEMPLATES_DIR):
        if filename.endswith('.html'):
            filepath = os.path.join(TEMPLATES_DIR, filename)
            total_count += 1
            if add_csrf_to_template(filepath):
                modified_count += 1
    
    print(f"\n" + "="*60)
    print(f" ✅ Terminé : {modified_count}/{total_count} templates modifiés")
    print("="*60 + "\n")

if __name__ == '__main__':
    main()
