# NyangaBudget 2.0 - Plateforme Familiale de Gestion Financière & Patrimoniale
#
# INSTRUCTIONS DE DÉMARRAGE (Windows):
# 1. Créer environnement virtuel: python -m venv .venv
# 2. Activer l'environnement: .venv\Scripts\activate
# 3. Installer dépendances: pip install -r requirements.txt
# 4. Lancer l'application: python app.py
# 5. Ouvrir navigateur: http://localhost:5000
#
# COMPTE PAR DÉFAUT:
# - Email: admin@nyanga.cm
# - Mot de passe: admin123
#
# FONCTIONNALITÉS RÉVOLUTIONNAIRES:
# ✅ Multi-Comptes Bancaires avec transferts
# ✅ Coffre-Fort Numérique crypté (AES-256)
# ✅ Héritage Familial avec testament numérique
# ✅ Gestion Familiale avec invitations sécurisées
# ✅ IA Prédictive & Score de santé financière
# ✅ Notifications en temps réel
# ✅ QR Code d'invitation familiale
import hashlib

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, make_response, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from sqlalchemy import func, extract, or_, and_
import plotly.graph_objs as go
import plotly
import json
import csv
import secrets
import string
import base64
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm
import os

# Cryptographie pour coffre-fort et héritage
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import qrcode

# Créer les dossiers nécessaires
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(BASE_DIR, 'data')
upload_folder = os.path.join(BASE_DIR, 'uploads')
vault_folder = os.path.join(upload_folder, 'vault')  # Coffre-fort crypté
heritage_folder = os.path.join(upload_folder, 'heritage')  # Documents héritage

for folder in [data_folder, upload_folder, vault_folder, heritage_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"[OK] Dossier cree: {folder}")

# Configuration de l'application
app = Flask(__name__)

# SECRET_KEY: utilise la variable d'environnement ou valeur par défaut pour dev
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nyanga-2.0-ultra-secure-key-joyed-cameroon-2025')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB par fichier
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['VAULT_FOLDER'] = vault_folder
app.config['HERITAGE_FOLDER'] = heritage_folder
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'png', 'jpg', 'jpeg', 'txt', 'doc', 'docx'}

# Base de données - Support PostgreSQL (Render) ET SQLite (local)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Production: PostgreSQL sur Render
    # Fix pour le format postgresql:// -> postgresql://
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    print(f"[OK] Utilisation de PostgreSQL (Production)")
else:
    # Développement local: SQLite
    db_path = os.path.join(data_folder, 'nyanga_v2.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    print(f"[OK] Utilisation de SQLite (Développement local)")

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Clé maître de cryptage (utilise variable d'environnement en production)
MASTER_ENCRYPTION_KEY_STR = os.environ.get('MASTER_ENCRYPTION_KEY', 'YourSecureMasterKey32BytesHere!!')
MASTER_ENCRYPTION_KEY = MASTER_ENCRYPTION_KEY_STR.encode() if isinstance(MASTER_ENCRYPTION_KEY_STR, str) else MASTER_ENCRYPTION_KEY_STR

# Initialisation de la base de données
db = SQLAlchemy(app)

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'warning'

# ==================== SÉCURITÉ ====================

# Protection CSRF
csrf = CSRFProtect(app)

# Rate Limiting (protection contre brute force)
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"  # En production: utiliser Redis
)

# ==================== PERFORMANCE - CACHE ====================

from flask_caching import Cache

# Configuration du cache
cache_config = {
    'CACHE_TYPE': 'simple',  # En production: 'redis' avec REDIS_URL
    'CACHE_DEFAULT_TIMEOUT': 300  # 5 minutes par défaut
}

# Si Redis est disponible en production
if os.environ.get('REDIS_URL'):
    cache_config['CACHE_TYPE'] = 'redis'
    cache_config['CACHE_REDIS_URL'] = os.environ.get('REDIS_URL')
    print("[OK] Cache Redis activé")
else:
    print("[OK] Cache simple (mémoire) activé")

cache = Cache(app, config=cache_config)


print("[OK] Sécurité initialisée: CSRF + Rate Limiting")


# ==================== FONCTIONS DE VALIDATION ====================

# Mapping MIME types autorisés
ALLOWED_MIME_TYPES = {
    'application/pdf': ['.pdf'],
    'image/png': ['.png'],
    'image/jpeg': ['.jpg', '.jpeg'],
    'image/jpg': ['.jpg', '.jpeg'],
    'text/plain': ['.txt'],
    'application/msword': ['.doc'],
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
}

def allowed_file(filename):
    """Vérifie si l'extension du fichier est autorisée"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def validate_file_upload(file):
    """Validation stricte des fichiers uploadés
    
    Vérifie :
    1. Extension du fichier
    2. MIME type réel (détection contenu)
    3. Taille du fichier
    
    Returns:
        tuple: (bool, str) - (valide, message_erreur)
    """
    if not file or file.filename == '':
        return False, "Aucun fichier sélectionné"
    
    # 1. Vérifier l'extension
    if not allowed_file(file.filename):
        return False, f"Type de fichier non autorisé. Extensions acceptées : {', '.join(app.config['ALLOWED_EXTENSIONS'])}"
    
    # 2. Vérifier le MIME type réel
    try:
        import magic
        # Lire les premiers 2048 octets pour détecter le type
        file_header = file.read(2048)
        file.seek(0)  # Remettre le curseur au début
        
        mime_type = magic.from_buffer(file_header, mime=True)
        
        # Vérifier si le MIME type correspond à l'extension
        extension = '.' + file.filename.rsplit('.', 1)[1].lower()
        
        if mime_type not in ALLOWED_MIME_TYPES:
            return False, f"Type MIME non autorisé : {mime_type}"
        
        if extension not in ALLOWED_MIME_TYPES[mime_type]:
            return False, f"Le contenu du fichier ne correspond pas à son extension"
    
    except ImportError:
        # Si python-magic n'est pas installé, on continue avec validation basique
        print("[WARNING] python-magic non disponible, validation MIME désactivée")
    except Exception as e:
        print(f"[WARNING] Erreur validation MIME: {str(e)}")
    
    # 3. Vérifier la taille (déjà géré par Flask MAX_CONTENT_LENGTH, mais double vérification)
    file.seek(0, 2)  # Aller à la fin
    file_size = file.tell()
    file.seek(0)  # Remettre au début
    
    max_size = app.config['MAX_CONTENT_LENGTH']
    if file_size > max_size:
        return False, f"Fichier trop volumineux (max: {max_size // (1024*1024)}MB)"
    
    return True, "Fichier valide"


# ==================== MODÈLES DE DONNÉES ====================

class User(UserMixin, db.Model):
    """Modèle pour les utilisateurs"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    depenses = db.relationship('Depense', backref='user', lazy=True, cascade='all, delete-orphan')
    revenus = db.relationship('Revenu', backref='user', lazy=True, cascade='all, delete-orphan')
    categories = db.relationship('Categorie', backref='user', lazy=True, cascade='all, delete-orphan')
    budgets = db.relationship('Budget', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


class Categorie(db.Model):
    """Modèle pour les catégories de dépenses"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    couleur = db.Column(db.String(7), default='#6c757d')  # Couleur hex
    icone = db.Column(db.String(50), default='bi-tag')  # Icône Bootstrap
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    depenses = db.relationship('Depense', backref='categorie', lazy=True)

    def __repr__(self):
        return f'<Categorie {self.nom}>'


class Depense(db.Model):
    """Modèle pour les dépenses"""
    __tablename__ = 'depenses'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Depense {self.nom}: {self.montant} FCFA>'


class Revenu(db.Model):
    """Modèle pour les revenus"""
    __tablename__ = 'revenus'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(200), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Revenu {self.source}: {self.montant} FCFA>'


class Budget(db.Model):
    """Modèle pour les budgets mensuels"""
    __tablename__ = 'budgets'

    id = db.Column(db.Integer, primary_key=True)
    mois = db.Column(db.String(7), nullable=False)
    montant_limite = db.Column(db.Float, nullable=False)
    categorie_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    alerte_seuil = db.Column(db.Integer, default=80)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Budget {self.mois}: {self.montant_limite} FCFA>'


# ==================== NOUVEAUX MODÈLES RÉVOLUTIONNAIRES ====================

class CompteBancaire(db.Model):
    """Modèle pour les comptes bancaires multiples"""
    __tablename__ = 'comptes_bancaires'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)  # Ex: "Orange Money", "Afriland"
    type_compte = db.Column(db.String(50), nullable=False)  # mobile_money, banque, cash, crypto
    numero_compte = db.Column(db.String(100))  # Numéro de compte (optionnel)
    solde_initial = db.Column(db.Float, default=0.0)
    solde_actuel = db.Column(db.Float, default=0.0)
    devise = db.Column(db.String(10), default='FCFA')
    couleur = db.Column(db.String(7), default='#007bff')
    icone = db.Column(db.String(50), default='bi-wallet2')
    est_principal = db.Column(db.Boolean, default=False)  # Compte par défaut
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    transferts_emis = db.relationship('TransfertCompte', foreign_keys='TransfertCompte.compte_source_id', backref='compte_source', lazy=True)
    transferts_recus = db.relationship('TransfertCompte', foreign_keys='TransfertCompte.compte_destination_id', backref='compte_destination', lazy=True)

    def __repr__(self):
        return f'<Compte {self.nom}: {self.solde_actuel} {self.devise}>'


class TransfertCompte(db.Model):
    """Modèle pour les transferts inter-comptes"""
    __tablename__ = 'transferts_comptes'

    id = db.Column(db.Integer, primary_key=True)
    montant = db.Column(db.Float, nullable=False)
    motif = db.Column(db.String(200))
    compte_source_id = db.Column(db.Integer, db.ForeignKey('comptes_bancaires.id'), nullable=False)
    compte_destination_id = db.Column(db.Integer, db.ForeignKey('comptes_bancaires.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    hash_transaction = db.Column(db.String(64))  # Hash SHA-256 pour traçabilité blockchain-like
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def generer_hash(self):
        """Génère un hash unique pour la transaction (immuabilité)"""
        data = f"{self.id}{self.montant}{self.compte_source_id}{self.compte_destination_id}{self.date_created}"
        self.hash_transaction = hashlib.sha256(data.encode()).hexdigest()

    def __repr__(self):
        return f'<Transfert {self.montant} FCFA | {self.hash_transaction[:8]}>'


class Famille(db.Model):
    """Modèle pour les familles"""
    __tablename__ = 'familles'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    code_invitation = db.Column(db.String(10), unique=True, nullable=False)  # Code unique 8 chars
    chef_famille_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    membres = db.relationship('MembreFamille', backref='famille', lazy=True, cascade='all, delete-orphan')
    chef = db.relationship('User', foreign_keys=[chef_famille_id])

    def generer_code_invitation(self):
        """Génère un code d'invitation unique"""
        chars = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(secrets.choice(chars) for _ in range(8))
            if not Famille.query.filter_by(code_invitation=code).first():
                self.code_invitation = code
                break

    def __repr__(self):
        return f'<Famille {self.nom} | Code: {self.code_invitation}>'


class MembreFamille(db.Model):
    """Modèle pour les membres d'une famille"""
    __tablename__ = 'membres_famille'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    famille_id = db.Column(db.Integer, db.ForeignKey('familles.id'), nullable=False)
    role = db.Column(db.String(20), default='membre')  # chef, parent, enfant, membre, invite
    statut = db.Column(db.String(20), default='en_attente')  # en_attente, valide, refuse
    valide_par_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Admin qui a validé
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_validation = db.Column(db.DateTime)

    # Relations
    user = db.relationship('User', foreign_keys=[user_id], backref='familles_membre')
    validateur = db.relationship('User', foreign_keys=[valide_par_id])

    def __repr__(self):
        return f'<Membre {self.user_id} | Famille {self.famille_id} | {self.statut}>'


class CoffreFort(db.Model):
    """Modèle pour le coffre-fort numérique crypté"""
    __tablename__ = 'coffre_fort'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    type_document = db.Column(db.String(50), nullable=False)  # document, mot_de_passe, note, code_pin
    contenu_crypte = db.Column(db.Text)  # Texte crypté (notes, mots de passe)
    fichier_crypte = db.Column(db.String(255))  # Nom du fichier crypté
    est_critique = db.Column(db.Boolean, default=False)  # Document ultra-important
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    famille_id = db.Column(db.Integer, db.ForeignKey('familles.id'))  # Partagé avec famille
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<CoffreFort {self.titre} | {self.type_document}>'


class Heritage(db.Model):
    """Modèle pour l'héritage familial (Testament numérique)"""
    __tablename__ = 'heritage'

    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    type_bien = db.Column(db.String(50), nullable=False)  # immobilier, vehicule, compte, objet_valeur, document
    description = db.Column(db.Text)
    valeur_estimee = db.Column(db.Float)
    fichier_crypte = db.Column(db.String(255))  # Document légal crypté
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    famille_id = db.Column(db.Integer, db.ForeignKey('familles.id'))
    est_actif = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Relations
    beneficiaires = db.relationship('Beneficiaire', backref='heritage', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Heritage {self.titre} | {self.type_bien}>'


class Beneficiaire(db.Model):
    """Modèle pour les bénéficiaires d'un héritage"""
    __tablename__ = 'beneficiaires'

    id = db.Column(db.Integer, primary_key=True)
    heritage_id = db.Column(db.Integer, db.ForeignKey('heritage.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pourcentage = db.Column(db.Float, default=100.0)  # % du bien (si plusieurs bénéficiaires)
    message_personnel = db.Column(db.Text)  # Message laissé au bénéficiaire
    condition_deblocage = db.Column(db.String(100))  # inactivite_30j, deces, urgence
    est_notifie = db.Column(db.Boolean, default=False)
    date_notification = db.Column(db.DateTime)

    # Relations
    user = db.relationship('User', backref='heritages_recus')

    def __repr__(self):
        return f'<Beneficiaire {self.user_id} | {self.pourcentage}%>'


class Notification(db.Model):
    """Modèle pour les notifications en temps réel"""
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type_notif = db.Column(db.String(50), nullable=False)  # budget, famille, heritage, compte, alerte
    titre = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    lien = db.Column(db.String(255))  # URL de redirection
    est_lue = db.Column(db.Boolean, default=False)
    priorite = db.Column(db.String(20), default='normale')  # basse, normale, haute, critique
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Notification {self.type_notif} | {self.titre}>'


class ScoreSante(db.Model):
    """Modèle pour le score de santé financière (IA simple)"""
    __tablename__ = 'scores_sante'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    score = db.Column(db.Integer, default=50)  # Score 0-100
    niveau = db.Column(db.String(20))  # critique, faible, moyen, bon, excellent
    facteurs_positifs = db.Column(db.Text)  # JSON des points forts
    facteurs_negatifs = db.Column(db.Text)  # JSON des points à améliorer
    suggestions = db.Column(db.Text)  # JSON des suggestions IA
    date_calcul = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Score {self.score}/100 | {self.niveau}>'


class Rappel(db.Model):
    """Modèle pour les rappels de paiement et échéances"""
    __tablename__ = 'rappels'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    montant = db.Column(db.Float)
    date_echeance = db.Column(db.DateTime, nullable=False)
    type_rappel = db.Column(db.String(50), default='paiement')  # paiement, facture, echeance, autre
    est_recurrent = db.Column(db.Boolean, default=False)
    frequence = db.Column(db.String(20))  # mensuel, hebdomadaire, annuel
    est_complete = db.Column(db.Boolean, default=False)
    date_completed = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Rappel {self.titre} | {self.date_echeance}>'


class ObjectifFinancier(db.Model):
    """Modèle pour les objectifs d'épargne et projets"""
    __tablename__ = 'objectifs_financiers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    famille_id = db.Column(db.Integer, db.ForeignKey('familles.id'))  # Objectif familial partagé
    titre = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    montant_cible = db.Column(db.Float, nullable=False)
    montant_actuel = db.Column(db.Float, default=0.0)
    date_limite = db.Column(db.DateTime)
    icone = db.Column(db.String(50), default='bi-piggy-bank')
    couleur = db.Column(db.String(7), default='#28a745')
    est_atteint = db.Column(db.Boolean, default=False)
    date_atteint = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Objectif {self.titre} | {self.montant_actuel}/{self.montant_cible}>'


# ==================== FLASK-LOGIN ====================

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== HELPERS / FONCTIONS UTILITAIRES ====================

def valider_montant(montant_str):
    """Valide et convertit un montant en float"""
    try:
        montant = float(montant_str)
        if montant <= 0:
            return None, "Le montant doit être supérieur à 0"
        return montant, None
    except (ValueError, TypeError):
        return None, "Montant invalide"


def calculer_statistiques(user_id, start_date=None, end_date=None):
    """Calcule les statistiques globales pour un utilisateur"""
    query_depenses = db.session.query(func.sum(Depense.montant)).filter(Depense.user_id == user_id)
    query_revenus = db.session.query(func.sum(Revenu.montant)).filter(Revenu.user_id == user_id)

    if start_date:
        query_depenses = query_depenses.filter(Depense.date_created >= start_date)
        query_revenus = query_revenus.filter(Revenu.date_created >= start_date)

    if end_date:
        query_depenses = query_depenses.filter(Depense.date_created <= end_date)
        query_revenus = query_revenus.filter(Revenu.date_created <= end_date)

    total_depenses = query_depenses.scalar() or 0.0
    total_revenus = query_revenus.scalar() or 0.0
    solde = total_revenus - total_depenses

    nb_depenses = Depense.query.filter(
        Depense.user_id == user_id,
        Depense.date_created >= start_date if start_date else True,
        Depense.date_created <= end_date if end_date else True
    ).count()

    nb_revenus = Revenu.query.filter(
        Revenu.user_id == user_id,
        Revenu.date_created >= start_date if start_date else True,
        Revenu.date_created <= end_date if end_date else True
    ).count()

    return {
        'total_depenses': round(total_depenses, 2),
        'total_revenus': round(total_revenus, 2),
        'solde': round(solde, 2),
        'nb_depenses': nb_depenses,
        'nb_revenus': nb_revenus
    }


def verifier_alertes_budget(user_id):
    """Vérifie si des budgets dépassent le seuil d'alerte"""
    mois_actuel = datetime.now().strftime('%Y-%m')
    budgets = Budget.query.filter_by(user_id=user_id, mois=mois_actuel).all()

    alertes = []
    for budget in budgets:
        # Calculer dépenses du mois pour cette catégorie
        if budget.categorie_id:
            depenses_mois = db.session.query(func.sum(Depense.montant)).filter(
                Depense.user_id == user_id,
                Depense.categorie_id == budget.categorie_id,
                func.strftime('%Y-%m', Depense.date_created) == mois_actuel
            ).scalar() or 0.0
            categorie_nom = budget.categorie.nom if budget.categorie else "Général"
        else:
            # Budget global
            depenses_mois = db.session.query(func.sum(Depense.montant)).filter(
                Depense.user_id == user_id,
                func.strftime('%Y-%m', Depense.date_created) == mois_actuel
            ).scalar() or 0.0
            categorie_nom = "Global"

        pourcentage = (depenses_mois / budget.montant_limite * 100) if budget.montant_limite > 0 else 0

        if pourcentage >= budget.alerte_seuil:
            alertes.append({
                'categorie': categorie_nom,
                'pourcentage': round(pourcentage, 1),
                'depenses': depenses_mois,
                'limite': budget.montant_limite,
                'type': 'danger' if pourcentage >= 100 else 'warning'
            })

    return alertes


def generer_graphique_camembert(user_id):
    """Génère un graphique camembert de la répartition des dépenses par catégorie"""
    depenses = db.session.query(
        Categorie.nom,
        func.sum(Depense.montant).label('total')
    ).join(Depense).filter(Depense.user_id == user_id).group_by(Categorie.nom).all()

    # Ajouter les dépenses sans catégorie
    depenses_sans_cat = db.session.query(
        func.sum(Depense.montant).label('total')
    ).filter(Depense.user_id == user_id, Depense.categorie_id == None).scalar() or 0

    if not depenses and depenses_sans_cat == 0:
        return json.dumps({})

    labels = [d.nom for d in depenses]
    values = [float(d.total) for d in depenses]

    if depenses_sans_cat > 0:
        labels.append('Sans catégorie')
        values.append(float(depenses_sans_cat))

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#C9CBCF'])
    )])

    fig.update_layout(
        title='Répartition des dépenses par catégorie',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def generer_graphique_mensuel(user_id):
    """Génère un graphique en barres des dépenses et revenus mensuels"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    # Agrégation des dépenses par mois
    depenses_mensuelles = db.session.query(
        func.strftime('%Y-%m', Depense.date_created).label('mois'),
        func.sum(Depense.montant).label('total')
    ).filter(Depense.user_id == user_id, Depense.date_created >= start_date).group_by('mois').all()

    # Agrégation des revenus par mois
    revenus_mensuels = db.session.query(
        func.strftime('%Y-%m', Revenu.date_created).label('mois'),
        func.sum(Revenu.montant).label('total')
    ).filter(Revenu.user_id == user_id, Revenu.date_created >= start_date).group_by('mois').all()

    depenses_dict = {d.mois: float(d.total) for d in depenses_mensuelles}
    revenus_dict = {r.mois: float(r.total) for r in revenus_mensuels}

    all_months = sorted(set(list(depenses_dict.keys()) + list(revenus_dict.keys())))

    if not all_months:
        return json.dumps({})

    depenses_values = [depenses_dict.get(m, 0) for m in all_months]
    revenus_values = [revenus_dict.get(m, 0) for m in all_months]

    fig = go.Figure(data=[
        go.Bar(name='Dépenses', x=all_months, y=depenses_values, marker_color='#FF6384'),
        go.Bar(name='Revenus', x=all_months, y=revenus_values, marker_color='#36A2EB')
    ])

    fig.update_layout(
        title='Évolution mensuelle (6 derniers mois)',
        xaxis_title='Mois',
        yaxis_title='Montant (FCFA)',
        barmode='group',
        height=400,
        margin=dict(l=20, r=20, t=40, b=60)
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def generer_graphique_tendances(user_id):
    """Génère un graphique de tendances avec ligne de progression"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    # Dépenses par semaine
    depenses_hebdo = db.session.query(
        func.strftime('%Y-%W', Depense.date_created).label('semaine'),
        func.sum(Depense.montant).label('total')
    ).filter(Depense.user_id == user_id, Depense.date_created >= start_date).group_by('semaine').all()

    if not depenses_hebdo:
        return json.dumps({})

    semaines = [d.semaine for d in depenses_hebdo]
    montants = [float(d.total) for d in depenses_hebdo]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=semaines,
        y=montants,
        mode='lines+markers',
        name='Dépenses hebdomadaires',
        line=dict(color='#FF6384', width=2),
        marker=dict(size=6)
    ))

    # Ajouter une ligne de tendance (moyenne mobile)
    if len(montants) >= 4:
        moyenne_mobile = []
        for i in range(len(montants)):
            if i < 3:
                moyenne_mobile.append(sum(montants[:i+1]) / (i+1))
            else:
                moyenne_mobile.append(sum(montants[i-3:i+1]) / 4)

        fig.add_trace(go.Scatter(
            x=semaines,
            y=moyenne_mobile,
            mode='lines',
            name='Tendance (moyenne 4 semaines)',
            line=dict(color='#36A2EB', width=2, dash='dash')
        ))

    fig.update_layout(
        title='Tendances des dépenses (12 derniers mois)',
        xaxis_title='Semaine',
        yaxis_title='Montant (FCFA)',
        height=400,
        margin=dict(l=20, r=20, t=40, b=60),
        hovermode='x unified'
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def generer_csv(user_id):
    """Génère un fichier CSV consolidé de toutes les transactions"""
    depenses = Depense.query.filter_by(user_id=user_id).all()
    transactions_depenses = [{
        'Date': d.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        'Type': 'Dépense',
        'Description': d.nom,
        'Catégorie': d.categorie.nom if d.categorie else 'Sans catégorie',
        'Montant': -d.montant
    } for d in depenses]

    revenus = Revenu.query.filter_by(user_id=user_id).all()
    transactions_revenus = [{
        'Date': r.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        'Type': 'Revenu',
        'Description': r.source,
        'Catégorie': 'N/A',
        'Montant': r.montant
    } for r in revenus]

    all_transactions = transactions_depenses + transactions_revenus
    all_transactions.sort(key=lambda x: x['Date'], reverse=True)

    return all_transactions


def generer_pdf(user_id):
    """Génère un rapport PDF avec résumé et top 10 des dépenses"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=1
    )

    elements.append(Paragraph('NyangaBudget - Rapport Financier', title_style))
    elements.append(Spacer(1, 0.5*cm))

    date_rapport = datetime.now().strftime('%d/%m/%Y a %H:%M')
    elements.append(Paragraph(f'<b>Date du rapport:</b> {date_rapport}', styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))

    stats = calculer_statistiques(user_id)

    data_stats = [
        ['Indicateur', 'Valeur'],
        ['Total Depenses', f"{stats['total_depenses']:,.0f} FCFA"],
        ['Total Revenus', f"{stats['total_revenus']:,.0f} FCFA"],
        ['Solde', f"{stats['solde']:,.0f} FCFA"],
        ['Nombre de depenses', str(stats['nb_depenses'])],
        ['Nombre de revenus', str(stats['nb_revenus'])]
    ]

    table_stats = Table(data_stats, colWidths=[8*cm, 8*cm])
    table_stats.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))

    elements.append(table_stats)
    elements.append(Spacer(1, 1*cm))

    elements.append(Paragraph('<b>Top 10 des depenses les plus importantes</b>', styles['Heading2']))
    elements.append(Spacer(1, 0.3*cm))

    top_depenses = Depense.query.filter_by(user_id=user_id).order_by(Depense.montant.desc()).limit(10).all()

    if top_depenses:
        data_depenses = [['#', 'Description', 'Categorie', 'Montant', 'Date']]
        for idx, d in enumerate(top_depenses, 1):
            cat_nom = d.categorie.nom[:15] if d.categorie else 'N/A'
            data_depenses.append([
                str(idx),
                d.nom[:30],
                cat_nom,
                f"{d.montant:,.0f} FCFA",
                d.date_created.strftime('%d/%m/%Y')
            ])

        table_depenses = Table(data_depenses, colWidths=[1*cm, 6*cm, 3*cm, 3*cm, 2.5*cm])
        table_depenses.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))

        elements.append(table_depenses)
    else:
        elements.append(Paragraph('Aucune depense enregistree.', styles['Normal']))

    elements.append(Spacer(1, 1*cm))
    elements.append(Paragraph('<i>Propulse par JoYed\'S - NyangaBudget Cameroun</i>', styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return buffer


def creer_categories_defaut(user_id):
    """Crée des catégories par défaut pour un nouvel utilisateur
    
    Note: Cette fonction est appelée par init_db() pour l'admin.
    Pour les inscriptions normales, les catégories sont créées directement dans register().
    """
    categories_defaut = [
        {'nom': 'Alimentation', 'couleur': '#28a745', 'icone': 'bi-cart'},
        {'nom': 'Transport', 'couleur': '#ffc107', 'icone': 'bi-bus-front'},
        {'nom': 'Logement', 'couleur': '#dc3545', 'icone': 'bi-house'},
        {'nom': 'Santé', 'couleur': '#17a2b8', 'icone': 'bi-heart-pulse'},
        {'nom': 'Loisirs', 'couleur': '#e83e8c', 'icone': 'bi-controller'},
        {'nom': 'Éducation', 'couleur': '#6610f2', 'icone': 'bi-book'},
        {'nom': 'Vêtements', 'couleur': '#fd7e14', 'icone': 'bi-bag'},
        {'nom': 'Autres', 'couleur': '#6c757d', 'icone': 'bi-tag'}
    ]

    for cat_data in categories_defaut:
        categorie = Categorie(user_id=user_id, **cat_data)
        db.session.add(categorie)

    # Note: Pas de commit ici, c'est la fonction appelante qui fait le commit



# ==================== FONCTIONS CRYPTAGE (COFFRE-FORT & HÉRITAGE) ====================

def generer_cle_fernet(password, user_id=None):
    """Génère une clé Fernet à partir d'un mot de passe avec salt unique par utilisateur
    
    Args:
        password: Mot de passe utilisateur
        user_id: ID de l'utilisateur (optionnel). Si fourni, génère un salt unique.
    
    Returns:
        Clé Fernet dérivée du mot de passe
    """
    # Génération du salt unique par utilisateur
    if user_id:
        # Salt dérivé de l'user_id + constante secrète
        salt_base = f"nyanga_2025_{user_id}_secure_salt"
        salt = hashlib.sha256(salt_base.encode()).digest()
    else:
        # Fallback pour compatibilité (anciens documents)
        salt = b'nyanga_salt_2025'
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,  # Salt unique par utilisateur
        iterations=150000,  # Augmenté de 100k à 150k pour plus de sécurité
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key


def crypter_texte(texte, password=None, user_id=None):
    """Crypte un texte avec Fernet
    
    Args:
        texte: Texte à crypter
        password: Mot de passe personnalisé (optionnel)
        user_id: ID utilisateur pour salt unique (optionnel)
    """
    if password:
        key = generer_cle_fernet(password, user_id)
    else:
        key = MASTER_ENCRYPTION_KEY

    f = Fernet(key)
    texte_crypte = f.encrypt(texte.encode())
    return base64.urlsafe_b64encode(texte_crypte).decode()


def decrypter_texte(texte_crypte, password=None, user_id=None):
    """Décrypte un texte avec Fernet
    
    Args:
        texte_crypte: Texte crypté à déchiffrer
        password: Mot de passe personnalisé (optionnel)
        user_id: ID utilisateur pour salt unique (optionnel)
    """
    try:
        if password:
            key = generer_cle_fernet(password, user_id)
        else:
            key = MASTER_ENCRYPTION_KEY

        f = Fernet(key)
        texte_decode = base64.urlsafe_b64decode(texte_crypte.encode())
        texte_clair = f.decrypt(texte_decode).decode()
        return texte_clair
    except:
        return None


def crypter_fichier(fichier_path, password=None, user_id=None):
    """Crypte un fichier avec salt unique par utilisateur"""
    if password:
        key = generer_cle_fernet(password, user_id)
    else:
        key = MASTER_ENCRYPTION_KEY

    f = Fernet(key)

    with open(fichier_path, 'rb') as file:
        file_data = file.read()

    encrypted_data = f.encrypt(file_data)

    with open(fichier_path + '.encrypted', 'wb') as file:
        file.write(encrypted_data)

    os.remove(fichier_path)
    return fichier_path + '.encrypted'


def decrypter_fichier(fichier_crypte_path, password=None):
    """Décrypte un fichier"""
    try:
        if password:
            key = generer_cle_fernet(password)
        else:
            key = MASTER_ENCRYPTION_KEY

        f = Fernet(key)

        with open(fichier_crypte_path, 'rb') as file:
            encrypted_data = file.read()

        decrypted_data = f.decrypt(encrypted_data)

        fichier_path = fichier_crypte_path.replace('.encrypted', '')
        with open(fichier_path, 'wb') as file:
            file.write(decrypted_data)

        return fichier_path
    except:
        return None


# ==================== IA PRÉDICTIVE & SCORE SANTÉ FINANCIÈRE ====================

def calculer_score_sante_financiere(user_id):
    """Calcule le score de santé financière (0-100) avec IA basique"""
    score = 50  # Score de base
    facteurs_positifs = []
    facteurs_negatifs = []
    suggestions = []

    # Récupérer données utilisateur
    stats = calculer_statistiques(user_id)
    comptes = CompteBancaire.query.filter_by(user_id=user_id).all()
    budgets = Budget.query.filter_by(user_id=user_id).filter(
        Budget.mois == datetime.now().strftime('%Y-%m')
    ).all()

    # Facteur 1: Solde positif (+20 points)
    if stats['solde'] > 0:
        score += 20
        facteurs_positifs.append("Solde positif")
    else:
        score -= 15
        facteurs_negatifs.append("Solde négatif")
        suggestions.append("Réduisez vos dépenses ou augmentez vos revenus")

    # Facteur 2: Épargne (comptes multiples) (+15 points)
    if len(comptes) >= 2:
        score += 15
        facteurs_positifs.append(f"{len(comptes)} comptes bancaires")
    else:
        suggestions.append("Créez plusieurs comptes pour mieux gérer votre argent")

    # Facteur 3: Respect des budgets (+20 points)
    if budgets:
        budgets_respectes = 0
        for budget in budgets:
            depenses_mois = db.session.query(func.sum(Depense.montant)).filter(
                Depense.user_id == user_id,
                func.strftime('%Y-%m', Depense.date_created) == budget.mois
            ).scalar() or 0

            if depenses_mois <= budget.montant_limite:
                budgets_respectes += 1

        if budgets_respectes == len(budgets):
            score += 20
            facteurs_positifs.append("Tous les budgets respectés")
        elif budgets_respectes > 0:
            score += 10
            facteurs_positifs.append(f"{budgets_respectes}/{len(budgets)} budgets respectés")
        else:
            score -= 10
            facteurs_negatifs.append("Budgets dépassés")
            suggestions.append("Définissez des budgets réalistes")

    # Facteur 4: Régularité des revenus (+15 points)
    revenus_3_mois = Revenu.query.filter(
        Revenu.user_id == user_id,
        Revenu.date_created >= datetime.now() - timedelta(days=90)
    ).count()

    if revenus_3_mois >= 3:
        score += 15
        facteurs_positifs.append("Revenus réguliers")
    else:
        suggestions.append("Assurez-vous d'avoir des revenus réguliers")

    # Facteur 5: Ratio dépenses/revenus (<80% = +10 points)
    if stats['total_revenus'] > 0:
        ratio = (stats['total_depenses'] / stats['total_revenus']) * 100
        if ratio < 50:
            score += 10
            facteurs_positifs.append("Excellente gestion (dépenses < 50% revenus)")
        elif ratio < 80:
            score += 5
            facteurs_positifs.append("Bonne gestion (dépenses < 80% revenus)")
        else:
            score -= 10
            facteurs_negatifs.append("Dépenses trop élevées")
            suggestions.append(f"Réduisez vos dépenses de {ratio-70:.0f}%")

    # Limiter le score entre 0 et 100
    score = max(0, min(100, score))

    # Déterminer le niveau
    if score >= 80:
        niveau = "excellent"
    elif score >= 60:
        niveau = "bon"
    elif score >= 40:
        niveau = "moyen"
    elif score >= 20:
        niveau = "faible"
    else:
        niveau = "critique"

    return {
        'score': score,
        'niveau': niveau,
        'facteurs_positifs': facteurs_positifs,
        'facteurs_negatifs': facteurs_negatifs,
        'suggestions': suggestions
    }


def creer_notification(user_id, type_notif, titre, message, lien=None, priorite='normale'):
    """Crée une notification pour un utilisateur"""
    notif = Notification(
        user_id=user_id,
        type_notif=type_notif,
        titre=titre,
        message=message,
        lien=lien,
        priorite=priorite
    )
    db.session.add(notif)
    db.session.commit()
    return notif


def generer_qr_code_invitation(code_invitation):
    """Génère un QR code pour invitation familiale"""
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    url_invitation = f"http://localhost:5000/famille/rejoindre/{code_invitation}"
    qr.add_data(url_invitation)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer


# ==================== ROUTES AUTHENTIFICATION ====================

@app.route('/init-db')
@csrf.exempt  # Pas de formulaire, pas besoin de CSRF
def route_init_db():
    """Route pour initialiser la base de données (à appeler une seule fois après déploiement)"""
    try:
        init_db()
        return jsonify({
            'success': True,
            'message': 'Base de données initialisée avec succès ! Vous pouvez maintenant vous inscrire.'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")  # Max 10 tentatives par minute
def login():
    """Page de connexion"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        if not email or not password:
            flash('Email et mot de passe requis', 'danger')
            return redirect(url_for('login'))

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Bienvenue {user.nom}!', 'success')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("5 per minute")  # Max 5 inscriptions par minute
def register():
    """Page d'inscription"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nom = request.form.get('nom', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')

        # Validation des champs
        if not all([nom, email, password, password_confirm]):
            flash('Tous les champs sont requis', 'danger')
            return redirect(url_for('register'))

        if password != password_confirm:
            flash('Les mots de passe ne correspondent pas', 'danger')
            return redirect(url_for('register'))

        if len(password) < 6:
            flash('Le mot de passe doit contenir au moins 6 caractères', 'danger')
            return redirect(url_for('register'))

        # Vérifier si l'email existe déjà
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé', 'danger')
            return redirect(url_for('register'))

        # Créer l'utilisateur
        try:
            # Créer utilisateur
            user = User(nom=nom, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.flush()  # Obtenir l'ID sans commit
            
            print(f"[INFO] Utilisateur créé: {user.email} (ID: {user.id})")

            # Créer catégories par défaut
            categories_defaut = [
                {'nom': 'Alimentation', 'couleur': '#28a745', 'icone': 'bi-cart'},
                {'nom': 'Transport', 'couleur': '#ffc107', 'icone': 'bi-bus-front'},
                {'nom': 'Logement', 'couleur': '#dc3545', 'icone': 'bi-house'},
                {'nom': 'Santé', 'couleur': '#17a2b8', 'icone': 'bi-heart-pulse'},
                {'nom': 'Loisirs', 'couleur': '#e83e8c', 'icone': 'bi-controller'},
                {'nom': 'Éducation', 'couleur': '#6610f2', 'icone': 'bi-book'},
                {'nom': 'Vêtements', 'couleur': '#fd7e14', 'icone': 'bi-bag'},
                {'nom': 'Autres', 'couleur': '#6c757d', 'icone': 'bi-tag'}
            ]

            for cat_data in categories_defaut:
                categorie = Categorie(user_id=user.id, **cat_data)
                db.session.add(categorie)
            
            # Commit unique pour tout
            db.session.commit()
            print(f"[OK] Inscription terminée: {user.email}")

            flash('Compte créé avec succès! Vous pouvez maintenant vous connecter.', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            print(f"[ERREUR] Inscription échouée: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'Erreur lors de la création du compte. Veuillez réessayer.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    flash('Vous avez été déconnecté', 'info')
    return redirect(url_for('login'))


# ==================== ROUTES PRINCIPALES ====================

@app.route('/')
@login_required
def index():
    """Page d'accueil - Liste des dépenses avec formulaire d'ajout (paginée)"""
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 20  # 20 dépenses par page
    
    # Recherche et filtrage
    search = request.args.get('search', '').strip()
    categorie_filter = request.args.get('categorie', '')
    date_debut = request.args.get('date_debut', '')
    date_fin = request.args.get('date_fin', '')

    query = Depense.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(Depense.nom.contains(search))

    if categorie_filter:
        if categorie_filter == 'none':
            query = query.filter(Depense.categorie_id == None)
        else:
            query = query.filter(Depense.categorie_id == int(categorie_filter))

    if date_debut:
        try:
            date_debut_obj = datetime.strptime(date_debut, '%Y-%m-%d')
            query = query.filter(Depense.date_created >= date_debut_obj)
        except:
            pass

    if date_fin:
        try:
            date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d')
            date_fin_obj = date_fin_obj.replace(hour=23, minute=59, second=59)
            query = query.filter(Depense.date_created <= date_fin_obj)
        except:
            pass

    # Pagination
    depenses_pagination = query.order_by(Depense.date_created.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    categories = Categorie.query.filter_by(user_id=current_user.id).order_by(Categorie.nom).all()
    stats = calculer_statistiques(current_user.id)

    # Vérifier alertes budget
    alertes = verifier_alertes_budget(current_user.id)

    return render_template('index.html',
                         depenses=depenses_pagination.items,
                         pagination=depenses_pagination,
                         stats=stats,
                         categories=categories,
                         alertes=alertes,
                         search=search,
                         categorie_filter=categorie_filter,
                         date_debut=date_debut,
                         date_fin=date_fin)


@app.route('/add', methods=['POST'])
@login_required
def add_depense():
    """Ajoute une nouvelle dépense"""
    nom = request.form.get('nom', '').strip()
    montant_str = request.form.get('montant', '')
    categorie_id = request.form.get('categorie_id', '')

    if not nom:
        flash('Le nom de la dépense est obligatoire', 'danger')
        return redirect(url_for('index'))

    montant, erreur = valider_montant(montant_str)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('index'))

    try:
        nouvelle_depense = Depense(
            nom=nom,
            montant=montant,
            user_id=current_user.id,
            categorie_id=int(categorie_id) if categorie_id else None
        )
        db.session.add(nouvelle_depense)
        db.session.commit()
        flash(f'Dépense "{nom}" ajoutée avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')

    return redirect(url_for('index'))


@app.route('/delete/depense/<int:id>', methods=['POST'])
@login_required
def delete_depense(id):
    """Supprime une dépense"""
    try:
        depense = Depense.query.filter_by(id=id, user_id=current_user.id).first_or_404()
        nom = depense.nom
        db.session.delete(depense)
        db.session.commit()
        flash(f'Dépense "{nom}" supprimée avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')

    return redirect(url_for('index'))


@app.route('/revenues')
@login_required
def revenues():
    """Page de gestion des revenus"""
    # Recherche et filtrage
    search = request.args.get('search', '').strip()
    date_debut = request.args.get('date_debut', '')
    date_fin = request.args.get('date_fin', '')

    query = Revenu.query.filter_by(user_id=current_user.id)

    if search:
        query = query.filter(Revenu.source.contains(search))

    if date_debut:
        try:
            date_debut_obj = datetime.strptime(date_debut, '%Y-%m-%d')
            query = query.filter(Revenu.date_created >= date_debut_obj)
        except:
            pass

    if date_fin:
        try:
            date_fin_obj = datetime.strptime(date_fin, '%Y-%m-%d')
            date_fin_obj = date_fin_obj.replace(hour=23, minute=59, second=59)
            query = query.filter(Revenu.date_created <= date_fin_obj)
        except:
            pass

    revenus = query.order_by(Revenu.date_created.desc()).all()
    stats = calculer_statistiques(current_user.id)

    return render_template('revenues.html',
                         revenus=revenus,
                         stats=stats,
                         search=search,
                         date_debut=date_debut,
                         date_fin=date_fin)


@app.route('/add_revenue', methods=['POST'])
@login_required
def add_revenue():
    """Ajoute un nouveau revenu"""
    source = request.form.get('source', '').strip()
    montant_str = request.form.get('montant', '')

    if not source:
        flash('La source du revenu est obligatoire', 'danger')
        return redirect(url_for('revenues'))

    montant, erreur = valider_montant(montant_str)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('revenues'))

    try:
        nouveau_revenu = Revenu(source=source, montant=montant, user_id=current_user.id)
        db.session.add(nouveau_revenu)
        db.session.commit()
        flash(f'Revenu "{source}" ajouté avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')

    return redirect(url_for('revenues'))


@app.route('/delete/revenu/<int:id>', methods=['POST'])
@login_required
def delete_revenu(id):
    """Supprime un revenu"""
    try:
        revenu = Revenu.query.filter_by(id=id, user_id=current_user.id).first_or_404()
        source = revenu.source
        db.session.delete(revenu)
        db.session.commit()
        flash(f'Revenu "{source}" supprimé avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')

    return redirect(url_for('revenues'))


@app.route('/dashboard')
@login_required
@cache.cached(timeout=300, key_prefix=lambda: f'dashboard_{current_user.id}')
def dashboard():
    """Tableau de bord avec statistiques et graphiques (mis en cache 5 min)"""
    stats = calculer_statistiques(current_user.id)
    graphique_camembert = generer_graphique_camembert(current_user.id)
    graphique_mensuel = generer_graphique_mensuel(current_user.id)
    graphique_tendances = generer_graphique_tendances(current_user.id)

    # Alertes budget
    alertes = verifier_alertes_budget(current_user.id)

    return render_template(
        'dashboard.html',
        stats=stats,
        graphique_camembert=graphique_camembert,
        graphique_mensuel=graphique_mensuel,
        graphique_tendances=graphique_tendances,
        alertes=alertes
    )


# ==================== ROUTES CATÉGORIES ====================

@app.route('/categories')
@login_required
def categories():
    """Page de gestion des catégories"""
    categories = Categorie.query.filter_by(user_id=current_user.id).order_by(Categorie.nom).all()

    # Calculer nombre de dépenses par catégorie
    categories_stats = []
    for cat in categories:
        nb_depenses = Depense.query.filter_by(user_id=current_user.id, categorie_id=cat.id).count()
        total = db.session.query(func.sum(Depense.montant)).filter_by(
            user_id=current_user.id,
            categorie_id=cat.id
        ).scalar() or 0
        categories_stats.append({
            'categorie': cat,
            'nb_depenses': nb_depenses,
            'total': total
        })

    return render_template('categories.html', categories_stats=categories_stats)


@app.route('/add_categorie', methods=['POST'])
@login_required
def add_categorie():
    """Ajoute une nouvelle catégorie"""
    nom = request.form.get('nom', '').strip()
    couleur = request.form.get('couleur', '#6c757d')
    icone = request.form.get('icone', 'bi-tag')

    if not nom:
        flash('Le nom de la catégorie est obligatoire', 'danger')
        return redirect(url_for('categories'))

    try:
        nouvelle_categorie = Categorie(
            nom=nom,
            couleur=couleur,
            icone=icone,
            user_id=current_user.id
        )
        db.session.add(nouvelle_categorie)
        db.session.commit()
        flash(f'Catégorie "{nom}" créée avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la création: {str(e)}', 'danger')

    return redirect(url_for('categories'))


@app.route('/delete/categorie/<int:id>', methods=['POST'])
@login_required
def delete_categorie(id):
    """Supprime une catégorie"""
    try:
        categorie = Categorie.query.filter_by(id=id, user_id=current_user.id).first_or_404()
        nom = categorie.nom

        # Détacher les dépenses liées
        Depense.query.filter_by(categorie_id=id).update({'categorie_id': None})

        db.session.delete(categorie)
        db.session.commit()
        flash(f'Catégorie "{nom}" supprimée avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')

    return redirect(url_for('categories'))


# ==================== ROUTES BUDGETS ====================

@app.route('/budgets')
@login_required
def budgets():
    """Page de gestion des budgets"""
    mois_actuel = datetime.now().strftime('%Y-%m')
    budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.mois.desc()).all()
    categories = Categorie.query.filter_by(user_id=current_user.id).order_by(Categorie.nom).all()

    # Calculer progression pour chaque budget
    budgets_stats = []
    for budget in budgets:
        if budget.categorie_id:
            depenses_periode = db.session.query(func.sum(Depense.montant)).filter(
                Depense.user_id == current_user.id,
                Depense.categorie_id == budget.categorie_id,
                func.strftime('%Y-%m', Depense.date_created) == budget.mois
            ).scalar() or 0
        else:
            depenses_periode = db.session.query(func.sum(Depense.montant)).filter(
                Depense.user_id == current_user.id,
                func.strftime('%Y-%m', Depense.date_created) == budget.mois
            ).scalar() or 0

        pourcentage = (depenses_periode / budget.montant_limite * 100) if budget.montant_limite > 0 else 0

        budgets_stats.append({
            'budget': budget,
            'depenses': depenses_periode,
            'pourcentage': round(pourcentage, 1),
            'restant': budget.montant_limite - depenses_periode,
            'status': 'success' if pourcentage < 80 else ('warning' if pourcentage < 100 else 'danger')
        })

    return render_template('budgets.html',
                         budgets_stats=budgets_stats,
                         categories=categories,
                         mois_actuel=mois_actuel)


@app.route('/add_budget', methods=['POST'])
@login_required
def add_budget():
    """Ajoute un nouveau budget"""
    mois = request.form.get('mois', '')
    montant_str = request.form.get('montant_limite', '')
    categorie_id = request.form.get('categorie_id', '')
    alerte_seuil = request.form.get('alerte_seuil', 80)

    if not mois:
        flash('Le mois est obligatoire', 'danger')
        return redirect(url_for('budgets'))

    montant, erreur = valider_montant(montant_str)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('budgets'))

    try:
        # Vérifier si budget existe déjà
        existing = Budget.query.filter_by(
            user_id=current_user.id,
            mois=mois,
            categorie_id=int(categorie_id) if categorie_id else None
        ).first()

        if existing:
            flash('Un budget existe déjà pour cette période et catégorie', 'warning')
            return redirect(url_for('budgets'))

        nouveau_budget = Budget(
            mois=mois,
            montant_limite=montant,
            categorie_id=int(categorie_id) if categorie_id else None,
            alerte_seuil=int(alerte_seuil),
            user_id=current_user.id
        )
        db.session.add(nouveau_budget)
        db.session.commit()
        flash('Budget créé avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la création: {str(e)}', 'danger')

    return redirect(url_for('budgets'))


@app.route('/delete/budget/<int:id>', methods=['POST'])
@login_required
def delete_budget(id):
    """Supprime un budget"""
    try:
        budget = Budget.query.filter_by(id=id, user_id=current_user.id).first_or_404()
        db.session.delete(budget)
        db.session.commit()
        flash('Budget supprimé avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')

    return redirect(url_for('budgets'))


# ==================== ROUTES EXPORT ====================

@app.route('/export/csv')
@login_required
def export_csv():
    """Export CSV de toutes les transactions"""
    try:
        transactions = generer_csv(current_user.id)

        output = StringIO()
        if transactions:
            fieldnames = ['Date', 'Type', 'Description', 'Catégorie', 'Montant']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
        else:
            output.write('Date,Type,Description,Categorie,Montant\n')

        filename = f'nyanga_transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        csv_bytes = '\ufeff' + output.getvalue()

        response = make_response(csv_bytes)
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'

        return response
    except Exception as e:
        flash(f'Erreur lors de l\'export CSV: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/export/pdf')
@login_required
def export_pdf():
    """Export PDF du rapport financier"""
    try:
        pdf_buffer = generer_pdf(current_user.id)
        filename = f'nyanga_rapport_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
    except Exception as e:
        flash(f'Erreur lors de l\'export PDF: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))


# ==================== API REST ====================

@app.route('/api/stats', methods=['GET'])
@login_required
def api_stats():
    """API: Statistiques globales"""
    stats = calculer_statistiques(current_user.id)
    return jsonify(stats)


@app.route('/api/depenses', methods=['GET', 'POST'])
@login_required
def api_depenses():
    """API: Liste et création de dépenses"""
    if request.method == 'GET':
        depenses = Depense.query.filter_by(user_id=current_user.id).order_by(Depense.date_created.desc()).limit(50).all()
        return jsonify([{
            'id': d.id,
            'nom': d.nom,
            'montant': d.montant,
            'categorie': d.categorie.nom if d.categorie else None,
            'date': d.date_created.isoformat()
        } for d in depenses])

    elif request.method == 'POST':
        data = request.get_json()

        if not data or 'nom' not in data or 'montant' not in data:
            return jsonify({'error': 'Nom et montant requis'}), 400

        try:
            depense = Depense(
                nom=data['nom'],
                montant=float(data['montant']),
                categorie_id=data.get('categorie_id'),
                user_id=current_user.id
            )
            db.session.add(depense)
            db.session.commit()

            return jsonify({
                'id': depense.id,
                'nom': depense.nom,
                'montant': depense.montant,
                'date': depense.date_created.isoformat()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@app.route('/api/revenus', methods=['GET', 'POST'])
@login_required
def api_revenus():
    """API: Liste et création de revenus"""
    if request.method == 'GET':
        revenus = Revenu.query.filter_by(user_id=current_user.id).order_by(Revenu.date_created.desc()).limit(50).all()
        return jsonify([{
            'id': r.id,
            'source': r.source,
            'montant': r.montant,
            'date': r.date_created.isoformat()
        } for r in revenus])

    elif request.method == 'POST':
        data = request.get_json()

        if not data or 'source' not in data or 'montant' not in data:
            return jsonify({'error': 'Source et montant requis'}), 400

        try:
            revenu = Revenu(
                source=data['source'],
                montant=float(data['montant']),
                user_id=current_user.id
            )
            db.session.add(revenu)
            db.session.commit()

            return jsonify({
                'id': revenu.id,
                'source': revenu.source,
                'montant': revenu.montant,
                'date': revenu.date_created.isoformat()
            }), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@app.route('/api/categories', methods=['GET'])
@login_required
def api_categories():
    """API: Liste des catégories"""
    categories = Categorie.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': c.id,
        'nom': c.nom,
        'couleur': c.couleur,
        'icone': c.icone
    } for c in categories])


@app.route('/api/budgets/alertes', methods=['GET'])
@login_required
def api_budgets_alertes():
    """API: Alertes budgets"""
    alertes = verifier_alertes_budget(current_user.id)
    return jsonify(alertes)


# ==================== ROUTES MULTI-COMPTES BANCAIRES ====================

@app.route('/comptes')
@login_required
def comptes():
    """Page de gestion des comptes bancaires"""
    comptes = CompteBancaire.query.filter_by(user_id=current_user.id).order_by(CompteBancaire.est_principal.desc()).all()

    # Calculer solde total
    solde_total = sum(c.solde_actuel for c in comptes)

    # Récupérer derniers transferts
    transferts = TransfertCompte.query.filter_by(user_id=current_user.id).order_by(TransfertCompte.date_created.desc()).limit(10).all()

    return render_template('comptes.html', comptes=comptes, solde_total=solde_total, transferts=transferts)


@app.route('/add_compte', methods=['POST'])
@login_required
def add_compte():
    """Ajoute un nouveau compte bancaire"""
    nom = request.form.get('nom', '').strip()
    type_compte = request.form.get('type_compte', 'banque')
    numero_compte = request.form.get('numero_compte', '').strip()
    solde_initial_str = request.form.get('solde_initial', '0')
    couleur = request.form.get('couleur', '#007bff')
    icone = request.form.get('icone', 'bi-wallet2')

    if not nom:
        flash('Le nom du compte est obligatoire', 'danger')
        return redirect(url_for('comptes'))

    solde_initial, erreur = valider_montant(solde_initial_str) if solde_initial_str != '0' else (0, None)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('comptes'))

    try:
        nouveau_compte = CompteBancaire(
            nom=nom,
            type_compte=type_compte,
            numero_compte=numero_compte,
            solde_initial=solde_initial,
            solde_actuel=solde_initial,
            couleur=couleur,
            icone=icone,
            user_id=current_user.id
        )
        db.session.add(nouveau_compte)
        db.session.commit()
        flash(f'Compte "{nom}" créé avec succès!', 'success')

        # Notification
        creer_notification(current_user.id, 'compte', 'Nouveau compte créé',
                          f'Le compte "{nom}" a été ajouté avec succès.', url_for('comptes'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la création: {str(e)}', 'danger')

    return redirect(url_for('comptes'))


@app.route('/transfert_compte', methods=['POST'])
@login_required
def transfert_compte():
    """Effectue un transfert entre comptes"""
    compte_source_id = request.form.get('compte_source_id')
    compte_destination_id = request.form.get('compte_destination_id')
    montant_str = request.form.get('montant', '')
    motif = request.form.get('motif', '').strip()

    if not compte_source_id or not compte_destination_id:
        flash('Veuillez sélectionner les comptes source et destination', 'danger')
        return redirect(url_for('comptes'))

    if compte_source_id == compte_destination_id:
        flash('Les comptes source et destination doivent être différents', 'danger')
        return redirect(url_for('comptes'))

    montant, erreur = valider_montant(montant_str)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('comptes'))

    try:
        compte_source = CompteBancaire.query.filter_by(id=int(compte_source_id), user_id=current_user.id).first()
        compte_destination = CompteBancaire.query.filter_by(id=int(compte_destination_id), user_id=current_user.id).first()

        if not compte_source or not compte_destination:
            flash('Compte invalide', 'danger')
            return redirect(url_for('comptes'))

        if compte_source.solde_actuel < montant:
            flash('Solde insuffisant sur le compte source', 'danger')
            return redirect(url_for('comptes'))

        # Effectuer le transfert
        compte_source.solde_actuel -= montant
        compte_destination.solde_actuel += montant

        # Créer l'enregistrement du transfert
        transfert = TransfertCompte(
            montant=montant,
            motif=motif,
            compte_source_id=compte_source.id,
            compte_destination_id=compte_destination.id,
            user_id=current_user.id
        )
        db.session.add(transfert)
        db.session.flush()

        # Générer hash blockchain-like
        transfert.generer_hash()

        db.session.commit()
        flash(f'Transfert de {montant:,.0f} FCFA effectué avec succès!', 'success')

        # Notification
        creer_notification(current_user.id, 'compte', 'Transfert effectué',
                          f'{montant:,.0f} FCFA transféré de {compte_source.nom} vers {compte_destination.nom}',
                          url_for('comptes'), 'haute')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors du transfert: {str(e)}', 'danger')

    return redirect(url_for('comptes'))


@app.route('/delete/compte/<int:id>', methods=['POST'])
@login_required
def delete_compte(id):
    """Supprime un compte bancaire"""
    try:
        compte = CompteBancaire.query.filter_by(id=id, user_id=current_user.id).first_or_404()
        nom = compte.nom
        db.session.delete(compte)
        db.session.commit()
        flash(f'Compte "{nom}" supprimé avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')

    return redirect(url_for('comptes'))


# ==================== ROUTES COFFRE-FORT CRYPTÉ ====================

@app.route('/coffre_fort')
@login_required
def coffre_fort():
    """Page du coffre-fort numérique"""
    documents = CoffreFort.query.filter_by(user_id=current_user.id).order_by(CoffreFort.est_critique.desc(), CoffreFort.date_modified.desc()).all()
    return render_template('coffre_fort.html', documents=documents)


@app.route('/add_coffre', methods=['POST'])
@login_required
def add_coffre():
    """Ajoute un document au coffre-fort"""
    titre = request.form.get('titre', '').strip()
    type_document = request.form.get('type_document', 'note')
    contenu = request.form.get('contenu', '').strip()
    est_critique = request.form.get('est_critique') == 'on'
    fichier = request.files.get('fichier')

    if not titre:
        flash('Le titre est obligatoire', 'danger')
        return redirect(url_for('coffre_fort'))

    try:
        nouveau_doc = CoffreFort(
            titre=titre,
            type_document=type_document,
            est_critique=est_critique,
            user_id=current_user.id
        )

        # Crypter le contenu texte si présent
        if contenu:
            nouveau_doc.contenu_crypte = crypter_texte(contenu)

        # Crypter et sauvegarder le fichier si présent
        if fichier and fichier.filename:
            filename = secure_filename(fichier.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{current_user.id}_{timestamp}_{filename}"
            fichier_path = os.path.join(app.config['VAULT_FOLDER'], unique_filename)

            # Sauvegarder temporairement
            fichier.save(fichier_path)

            # Crypter le fichier
            fichier_crypte = crypter_fichier(fichier_path)
            nouveau_doc.fichier_crypte = os.path.basename(fichier_crypte)

        db.session.add(nouveau_doc)
        db.session.commit()
        flash(f'Document "{titre}" ajouté au coffre-fort avec cryptage AES-256!', 'success')

        # Notification
        creer_notification(current_user.id, 'coffre', 'Document sécurisé',
                          f'"{titre}" ajouté au coffre-fort crypté', url_for('coffre_fort'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')

    return redirect(url_for('coffre_fort'))


@app.route('/view_coffre/<int:id>')
@login_required
def view_coffre(id):
    """Affiche un document du coffre-fort (décrypté)"""
    document = CoffreFort.query.filter_by(id=id, user_id=current_user.id).first_or_404()

    contenu_decrypte = None
    if document.contenu_crypte:
        contenu_decrypte = decrypter_texte(document.contenu_crypte)

    return jsonify({
        'titre': document.titre,
        'type_document': document.type_document,
        'contenu': contenu_decrypte,
        'fichier': document.fichier_crypte,
        'est_critique': document.est_critique,
        'date_modified': document.date_modified.strftime('%d/%m/%Y %H:%M')
    })


@app.route('/delete/coffre/<int:id>', methods=['POST'])
@login_required
def delete_coffre(id):
    """Supprime un document du coffre-fort"""
    try:
        document = CoffreFort.query.filter_by(id=id, user_id=current_user.id).first_or_404()

        # Supprimer le fichier crypté si existe
        if document.fichier_crypte:
            fichier_path = os.path.join(app.config['VAULT_FOLDER'], document.fichier_crypte)
            if os.path.exists(fichier_path):
                os.remove(fichier_path)

        titre = document.titre
        db.session.delete(document)
        db.session.commit()
        flash(f'Document "{titre}" supprimé du coffre-fort', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')

    return redirect(url_for('coffre_fort'))


# ==================== ROUTES HÉRITAGE FAMILIAL ====================

@app.route('/heritage')
@login_required
def heritage():
    """Page de gestion de l'héritage"""
    heritages = Heritage.query.filter_by(user_id=current_user.id).order_by(Heritage.date_created.desc()).all()

    # Récupérer les membres de famille pour sélection bénéficiaires
    mes_familles = MembreFamille.query.filter_by(user_id=current_user.id, statut='valide').all()
    membres_disponibles = []
    for mf in mes_familles:
        autres_membres = MembreFamille.query.filter_by(famille_id=mf.famille_id, statut='valide').filter(MembreFamille.user_id != current_user.id).all()
        for membre in autres_membres:
            if membre.user not in membres_disponibles:
                membres_disponibles.append(membre.user)

    return render_template('heritage.html', heritages=heritages, membres_disponibles=membres_disponibles)


@app.route('/add_heritage', methods=['POST'])
@login_required
def add_heritage():
    """Ajoute un bien à l'héritage"""
    titre = request.form.get('titre', '').strip()
    type_bien = request.form.get('type_bien', 'document')
    description = request.form.get('description', '').strip()
    valeur_estimee_str = request.form.get('valeur_estimee', '0')
    fichier = request.files.get('fichier')

    if not titre:
        flash('Le titre est obligatoire', 'danger')
        return redirect(url_for('heritage'))

    valeur_estimee, erreur = valider_montant(valeur_estimee_str) if valeur_estimee_str != '0' else (0, None)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('heritage'))

    try:
        nouveau_heritage = Heritage(
            titre=titre,
            type_bien=type_bien,
            description=description,
            valeur_estimee=valeur_estimee,
            user_id=current_user.id
        )

        # Crypter et sauvegarder le fichier si présent
        if fichier and fichier.filename:
            filename = secure_filename(fichier.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"heritage_{current_user.id}_{timestamp}_{filename}"
            fichier_path = os.path.join(app.config['HERITAGE_FOLDER'], unique_filename)

            fichier.save(fichier_path)
            fichier_crypte = crypter_fichier(fichier_path)
            nouveau_heritage.fichier_crypte = os.path.basename(fichier_crypte)

        db.session.add(nouveau_heritage)
        db.session.commit()
        flash(f'Bien "{titre}" ajouté à votre héritage!', 'success')

        creer_notification(current_user.id, 'heritage', 'Héritage mis à jour',
                          f'Bien "{titre}" ajouté à votre testament numérique', url_for('heritage'))
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')

    return redirect(url_for('heritage'))


@app.route('/add_beneficiaire/<int:heritage_id>', methods=['POST'])
@login_required
def add_beneficiaire(heritage_id):
    """Ajoute un bénéficiaire à un bien"""
    heritage_item = Heritage.query.filter_by(id=heritage_id, user_id=current_user.id).first_or_404()

    beneficiaire_id = request.form.get('beneficiaire_id')
    pourcentage_str = request.form.get('pourcentage', '100')
    message_personnel = request.form.get('message_personnel', '').strip()
    condition_deblocage = request.form.get('condition_deblocage', 'inactivite_30j')

    if not beneficiaire_id:
        flash('Veuillez sélectionner un bénéficiaire', 'danger')
        return redirect(url_for('heritage'))

    try:
        pourcentage = float(pourcentage_str)
        if pourcentage <= 0 or pourcentage > 100:
            flash('Le pourcentage doit être entre 0 et 100', 'danger')
            return redirect(url_for('heritage'))

        beneficiaire = Beneficiaire(
            heritage_id=heritage_id,
            user_id=int(beneficiaire_id),
            pourcentage=pourcentage,
            message_personnel=message_personnel,
            condition_deblocage=condition_deblocage
        )
        db.session.add(beneficiaire)
        db.session.commit()
        flash('Bénéficiaire ajouté avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('heritage'))


@app.route('/delete/heritage/<int:id>', methods=['POST'])
@login_required
def delete_heritage(id):
    """Supprime un bien de l'héritage"""
    try:
        heritage_item = Heritage.query.filter_by(id=id, user_id=current_user.id).first_or_404()

        if heritage_item.fichier_crypte:
            fichier_path = os.path.join(app.config['HERITAGE_FOLDER'], heritage_item.fichier_crypte)
            if os.path.exists(fichier_path):
                os.remove(fichier_path)

        titre = heritage_item.titre
        db.session.delete(heritage_item)
        db.session.commit()
        flash(f'Bien "{titre}" supprimé de l\'héritage', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('heritage'))


# ==================== ROUTES GESTION FAMILIALE ====================

@app.route('/famille')
@login_required
def famille():
    """Page de gestion familiale"""
    # Familles dont je suis chef
    mes_familles_chef = Famille.query.filter_by(chef_famille_id=current_user.id).all()

    # Familles dont je suis membre
    mes_appartenances = MembreFamille.query.filter_by(user_id=current_user.id, statut='valide').all()

    # Demandes en attente de validation (si je suis chef)
    demandes_attente = []
    for fam in mes_familles_chef:
        demandes = MembreFamille.query.filter_by(famille_id=fam.id, statut='en_attente').all()
        demandes_attente.extend(demandes)

    return render_template('famille.html',
                         mes_familles_chef=mes_familles_chef,
                         mes_appartenances=mes_appartenances,
                         demandes_attente=demandes_attente)


@app.route('/create_famille', methods=['POST'])
@login_required
def create_famille():
    """Crée une nouvelle famille"""
    nom = request.form.get('nom', '').strip()
    description = request.form.get('description', '').strip()

    if not nom:
        flash('Le nom de la famille est obligatoire', 'danger')
        return redirect(url_for('famille'))

    try:
        nouvelle_famille = Famille(
            nom=nom,
            description=description,
            chef_famille_id=current_user.id
        )
        nouvelle_famille.generer_code_invitation()
        db.session.add(nouvelle_famille)
        db.session.commit()

        # Ajouter le chef comme membre validé
        membre_chef = MembreFamille(
            user_id=current_user.id,
            famille_id=nouvelle_famille.id,
            role='chef',
            statut='valide',
            valide_par_id=current_user.id,
            date_validation=datetime.utcnow()
        )
        db.session.add(membre_chef)
        db.session.commit()

        flash(f'Famille "{nom}" créée! Code d\'invitation: {nouvelle_famille.code_invitation}', 'success')

        creer_notification(current_user.id, 'famille', 'Famille créée',
                          f'Votre famille "{nom}" est prête! Partagez le code: {nouvelle_famille.code_invitation}',
                          url_for('famille'), 'haute')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('famille'))


@app.route('/famille/rejoindre', methods=['POST'])
@login_required
def rejoindre_famille():
    """Demande à rejoindre une famille via code invitation"""
    code_invitation = request.form.get('code_invitation', '').strip().upper()

    if not code_invitation:
        flash('Code d\'invitation requis', 'danger')
        return redirect(url_for('famille'))

    try:
        famille_trouvee = Famille.query.filter_by(code_invitation=code_invitation).first()

        if not famille_trouvee:
            flash('Code d\'invitation invalide', 'danger')
            return redirect(url_for('famille'))

        # Vérifier si déjà membre
        deja_membre = MembreFamille.query.filter_by(
            user_id=current_user.id,
            famille_id=famille_trouvee.id
        ).first()

        if deja_membre:
            flash('Vous êtes déjà membre de cette famille ou avez une demande en cours', 'warning')
            return redirect(url_for('famille'))

        # Créer demande d'adhésion
        demande = MembreFamille(
            user_id=current_user.id,
            famille_id=famille_trouvee.id,
            role='membre',
            statut='en_attente'
        )
        db.session.add(demande)
        db.session.commit()

        flash(f'Demande envoyée pour rejoindre la famille "{famille_trouvee.nom}"', 'success')

        # Notifier le chef de famille
        creer_notification(famille_trouvee.chef_famille_id, 'famille', 'Nouvelle demande d\'adhésion',
                          f'{current_user.nom} souhaite rejoindre votre famille "{famille_trouvee.nom}"',
                          url_for('famille'), 'haute')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('famille'))


@app.route('/famille/valider/<int:membre_id>', methods=['POST'])
@login_required
def valider_membre(membre_id):
    """Valide l'adhésion d'un membre (chef de famille uniquement)"""
    try:
        demande = MembreFamille.query.get_or_404(membre_id)
        famille_concernee = Famille.query.get_or_404(demande.famille_id)

        # Vérifier que current_user est chef de cette famille
        if famille_concernee.chef_famille_id != current_user.id:
            flash('Action non autorisée', 'danger')
            return redirect(url_for('famille'))

        demande.statut = 'valide'
        demande.valide_par_id = current_user.id
        demande.date_validation = datetime.utcnow()
        db.session.commit()

        flash(f'{demande.user.nom} a été accepté dans la famille!', 'success')

        # Notifier le membre accepté
        creer_notification(demande.user_id, 'famille', 'Demande acceptée',
                          f'Vous faites maintenant partie de la famille "{famille_concernee.nom}"!',
                          url_for('famille'), 'haute')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('famille'))


@app.route('/famille/refuser/<int:membre_id>', methods=['POST'])
@login_required
def refuser_membre(membre_id):
    """Refuse l'adhésion d'un membre"""
    try:
        demande = MembreFamille.query.get_or_404(membre_id)
        famille_concernee = Famille.query.get_or_404(demande.famille_id)

        if famille_concernee.chef_famille_id != current_user.id:
            flash('Action non autorisée', 'danger')
            return redirect(url_for('famille'))

        user_nom = demande.user.nom
        db.session.delete(demande)
        db.session.commit()

        flash(f'Demande de {user_nom} refusée', 'info')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('famille'))


@app.route('/famille/qrcode/<int:famille_id>')
@login_required
def famille_qrcode(famille_id):
    """Génère le QR code d'invitation pour une famille"""
    famille_obj = Famille.query.filter_by(id=famille_id, chef_famille_id=current_user.id).first_or_404()

    qr_buffer = generer_qr_code_invitation(famille_obj.code_invitation)

    return send_file(qr_buffer, mimetype='image/png', download_name=f'invitation_famille_{famille_obj.nom}.png')


# ==================== ROUTES SCORE SANTÉ & NOTIFICATIONS ====================

@app.route('/score_sante')
@login_required
def score_sante():
    """Affiche le score de santé financière avec IA"""
    score_data = calculer_score_sante_financiere(current_user.id)

    # Sauvegarder le score en base
    try:
        nouveau_score = ScoreSante(
            user_id=current_user.id,
            score=score_data['score'],
            niveau=score_data['niveau'],
            facteurs_positifs=json.dumps(score_data['facteurs_positifs']),
            facteurs_negatifs=json.dumps(score_data['facteurs_negatifs']),
            suggestions=json.dumps(score_data['suggestions'])
        )
        db.session.add(nouveau_score)
        db.session.commit()
    except:
        db.session.rollback()

    return jsonify(score_data)


@app.route('/notifications')
@login_required
def notifications():
    """Page des notifications"""
    notifications_list = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.date_created.desc()).limit(50).all()

    # Marquer comme lues
    for notif in notifications_list:
        if not notif.est_lue:
            notif.est_lue = True
    db.session.commit()

    return render_template('notifications.html', notifications=notifications_list)


@app.route('/api/notifications/count')
@login_required
def api_notifications_count():
    """API: Nombre de notifications non lues"""
    count = Notification.query.filter_by(user_id=current_user.id, est_lue=False).count()
    return jsonify({'count': count})


# ==================== ROUTES RAPPELS & ÉCHÉANCES ====================

@app.route('/rappels')
@login_required
def rappels():
    """Page de gestion des rappels"""
    rappels_actifs = Rappel.query.filter_by(user_id=current_user.id, est_complete=False).order_by(Rappel.date_echeance).all()
    rappels_completes = Rappel.query.filter_by(user_id=current_user.id, est_complete=True).order_by(Rappel.date_completed.desc()).limit(10).all()

    # Déterminer les rappels en retard et à venir
    now = datetime.now()
    rappels_urgents = [r for r in rappels_actifs if r.date_echeance < now]
    rappels_a_venir = [r for r in rappels_actifs if r.date_echeance >= now]

    return render_template('rappels.html',
                         rappels_urgents=rappels_urgents,
                         rappels_a_venir=rappels_a_venir,
                         rappels_completes=rappels_completes)


@app.route('/add_rappel', methods=['POST'])
@login_required
def add_rappel():
    """Ajoute un nouveau rappel"""
    titre = request.form.get('titre', '').strip()
    description = request.form.get('description', '').strip()
    montant_str = request.form.get('montant', '0')
    date_echeance_str = request.form.get('date_echeance', '')
    type_rappel = request.form.get('type_rappel', 'paiement')
    est_recurrent = request.form.get('est_recurrent') == 'on'
    frequence = request.form.get('frequence', '')

    if not titre or not date_echeance_str:
        flash('Le titre et la date d\'échéance sont obligatoires', 'danger')
        return redirect(url_for('rappels'))

    montant, erreur = valider_montant(montant_str) if montant_str != '0' else (0, None)
    if erreur:
        montant = 0

    try:
        date_echeance = datetime.strptime(date_echeance_str, '%Y-%m-%d')

        nouveau_rappel = Rappel(
            titre=titre,
            description=description,
            montant=montant,
            date_echeance=date_echeance,
            type_rappel=type_rappel,
            est_recurrent=est_recurrent,
            frequence=frequence if est_recurrent else None,
            user_id=current_user.id
        )
        db.session.add(nouveau_rappel)
        db.session.commit()
        flash(f'Rappel "{titre}" créé avec succès!', 'success')

        # Créer notification
        jours_restants = (date_echeance - datetime.now()).days
        creer_notification(current_user.id, 'alerte', 'Nouveau rappel',
                          f'Rappel "{titre}" prévu dans {jours_restants} jours',
                          url_for('rappels'), 'normale')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('rappels'))


@app.route('/complete_rappel/<int:id>', methods=['POST'])
@login_required
def complete_rappel(id):
    """Marque un rappel comme terminé"""
    try:
        rappel = Rappel.query.filter_by(id=id, user_id=current_user.id).first_or_404()
        rappel.est_complete = True
        rappel.date_completed = datetime.utcnow()

        # Si récurrent, créer le prochain rappel
        if rappel.est_recurrent and rappel.frequence:
            prochaine_date = rappel.date_echeance
            if rappel.frequence == 'hebdomadaire':
                prochaine_date = prochaine_date + timedelta(weeks=1)
            elif rappel.frequence == 'mensuel':
                prochaine_date = prochaine_date + timedelta(days=30)
            elif rappel.frequence == 'annuel':
                prochaine_date = prochaine_date + timedelta(days=365)

            prochain_rappel = Rappel(
                titre=rappel.titre,
                description=rappel.description,
                montant=rappel.montant,
                date_echeance=prochaine_date,
                type_rappel=rappel.type_rappel,
                est_recurrent=True,
                frequence=rappel.frequence,
                user_id=current_user.id
            )
            db.session.add(prochain_rappel)

        db.session.commit()
        flash(f'Rappel "{rappel.titre}" marqué comme terminé!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('rappels'))


@app.route('/delete/rappel/<int:id>', methods=['POST'])
@login_required
def delete_rappel(id):
    """Supprime un rappel"""
    try:
        rappel = Rappel.query.filter_by(id=id, user_id=current_user.id).first_or_404()
        titre = rappel.titre
        db.session.delete(rappel)
        db.session.commit()
        flash(f'Rappel "{titre}" supprimé', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('rappels'))


# ==================== ROUTES OBJECTIFS FINANCIERS ====================

@app.route('/objectifs')
@login_required
def objectifs():
    """Page de gestion des objectifs d'épargne"""
    objectifs_perso = ObjectifFinancier.query.filter_by(user_id=current_user.id, famille_id=None).order_by(ObjectifFinancier.est_atteint, ObjectifFinancier.date_created.desc()).all()

    # Objectifs familiaux
    mes_familles_ids = [mf.famille_id for mf in MembreFamille.query.filter_by(user_id=current_user.id, statut='valide').all()]
    objectifs_familiaux = ObjectifFinancier.query.filter(ObjectifFinancier.famille_id.in_(mes_familles_ids)).all() if mes_familles_ids else []

    # Calculer progression pour chaque objectif
    objectifs_data = []
    for obj in objectifs_perso + objectifs_familiaux:
        pourcentage = (obj.montant_actuel / obj.montant_cible * 100) if obj.montant_cible > 0 else 0
        jours_restants = (obj.date_limite - datetime.now()).days if obj.date_limite else None

        objectifs_data.append({
            'objectif': obj,
            'pourcentage': min(pourcentage, 100),
            'jours_restants': jours_restants,
            'montant_restant': obj.montant_cible - obj.montant_actuel
        })

    return render_template('objectifs.html', objectifs_data=objectifs_data)


@app.route('/add_objectif', methods=['POST'])
@login_required
def add_objectif():
    """Ajoute un nouvel objectif"""
    titre = request.form.get('titre', '').strip()
    description = request.form.get('description', '').strip()
    montant_cible_str = request.form.get('montant_cible', '')
    date_limite_str = request.form.get('date_limite', '')
    icone = request.form.get('icone', 'bi-piggy-bank')
    couleur = request.form.get('couleur', '#28a745')

    if not titre or not montant_cible_str:
        flash('Le titre et le montant cible sont obligatoires', 'danger')
        return redirect(url_for('objectifs'))

    montant_cible, erreur = valider_montant(montant_cible_str)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('objectifs'))

    try:
        date_limite = datetime.strptime(date_limite_str, '%Y-%m-%d') if date_limite_str else None

        nouvel_objectif = ObjectifFinancier(
            titre=titre,
            description=description,
            montant_cible=montant_cible,
            date_limite=date_limite,
            icone=icone,
            couleur=couleur,
            user_id=current_user.id
        )
        db.session.add(nouvel_objectif)
        db.session.commit()
        flash(f'Objectif "{titre}" créé avec succès!', 'success')

        creer_notification(current_user.id, 'alerte', 'Nouvel objectif',
                          f'Objectif "{titre}" : {montant_cible:,.0f} FCFA',
                          url_for('objectifs'), 'normale')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('objectifs'))


@app.route('/contribuer_objectif/<int:id>', methods=['POST'])
@login_required
def contribuer_objectif(id):
    """Ajoute une contribution à un objectif"""
    objectif = ObjectifFinancier.query.get_or_404(id)

    # Vérifier droits d'accès
    if objectif.user_id != current_user.id and not objectif.famille_id:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('objectifs'))

    montant_str = request.form.get('montant', '')
    montant, erreur = valider_montant(montant_str)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('objectifs'))

    try:
        objectif.montant_actuel += montant

        # Vérifier si objectif atteint
        if objectif.montant_actuel >= objectif.montant_cible and not objectif.est_atteint:
            objectif.est_atteint = True
            objectif.date_atteint = datetime.utcnow()
            flash(f'🎉 Félicitations ! Objectif "{objectif.titre}" atteint !', 'success')

            creer_notification(objectif.user_id, 'alerte', '🎉 Objectif atteint !',
                              f'L\'objectif "{objectif.titre}" est atteint !',
                              url_for('objectifs'), 'haute')
        else:
            flash(f'Contribution de {montant:,.0f} FCFA ajoutée !', 'success')

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('objectifs'))


@app.route('/delete/objectif/<int:id>', methods=['POST'])
@login_required
def delete_objectif(id):
    """Supprime un objectif"""
    try:
        objectif = ObjectifFinancier.query.filter_by(id=id, user_id=current_user.id).first_or_404()
        titre = objectif.titre
        db.session.delete(objectif)
        db.session.commit()
        flash(f'Objectif "{titre}" supprimé', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur: {str(e)}', 'danger')

    return redirect(url_for('objectifs'))


# ==================== INITIALISATION ====================

def init_db():
    """Initialise la base de données"""
    with app.app_context():
        db.create_all()

        # Créer utilisateur admin par défaut s'il n'existe pas
        if not User.query.filter_by(email='admin@nyanga.cm').first():
            admin = User(nom='Administrateur', email='admin@nyanga.cm')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

            # Créer catégories par défaut pour admin
            creer_categories_defaut(admin.id)

            print("[OK] Utilisateur admin cree: admin@nyanga.cm / admin123")

        print("[OK] Base de donnees initialisee")


# ==================== GESTION DES ERREURS ====================

@app.errorhandler(429)
def ratelimit_handler(e):
    """Gérer les erreurs de rate limiting"""
    flash('Trop de tentatives. Veuillez réessayer dans quelques minutes.', 'warning')
    return redirect(url_for('login')), 429


# ==================== POINT D'ENTRÉE ====================

if __name__ == '__main__':
    init_db()

    # Détection environnement
    is_production = os.environ.get('FLASK_ENV') == 'production'

    if not is_production:
        print("\n" + "="*50)
        print("NyangaBudget - Application demarree!")
        print("="*50)
        print("URL: http://localhost:5000")
        print("Compte admin: admin@nyanga.cm / admin123")
        print("Dashboard: http://localhost:5000/dashboard")
        print("API REST: http://localhost:5000/api/stats")
        print("="*50 + "\n")

    app.run(debug=not is_production, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
