"""
API REST pour NyangaBudget - Documentation Swagger
Authentification JWT pour applications mobiles
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    JWTManager, create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from werkzeug.security import check_password_hash
from datetime import timedelta

# Blueprint API v1
api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')

def init_jwt(app, db, User, Depense, Revenu, Categorie, Compte):
    """
    Initialiser JWT et créer les routes API

    Args:
        app: Flask app
        db: SQLAlchemy instance
        User, Depense, Revenu, Categorie, Compte: Modèles SQLAlchemy
    """

    # Configuration JWT
    app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)

    jwt = JWTManager(app)

    # ==================== AUTHENTIFICATION ====================

    @api_v1.route('/auth/register', methods=['POST'])

    def register():
        """
        Inscription d'un nouvel utilisateur

        Body:
            {
                "nom": "string",
                "email": "string",
                "password": "string"
            }

        Returns:
            {
                "success": true,
                "message": "Inscription réussie",
                "user_id": 123
            }
        """
        data = request.get_json()

        if not all(k in data for k in ['nom', 'email', 'password']):
            return jsonify({'error': 'Champs manquants'}), 400

        # Vérifier email existant
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email déjà utilisé'}), 409

        from werkzeug.security import generate_password_hash

        new_user = User(
            nom=data['nom'],
            email=data['email'],
            password=generate_password_hash(data['password'])
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Inscription réussie',
            'user_id': new_user.id
        }), 201

    @api_v1.route('/auth/login', methods=['POST'])

    def login():
        """
        Connexion et génération tokens JWT

        Body:
            {
                "email": "string",
                "password": "string"
            }

        Returns:
            {
                "access_token": "string",
                "refresh_token": "string",
                "user": {
                    "id": 123,
                    "nom": "string",
                    "email": "string"
                }
            }
        """
        data = request.get_json()

        if not all(k in data for k in ['email', 'password']):
            return jsonify({'error': 'Email et mot de passe requis'}), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Identifiants invalides'}), 401

        # Générer tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': {
                'id': user.id,
                'nom': user.nom,
                'email': user.email
            }
        }), 200

    @api_v1.route('/auth/refresh', methods=['POST'])
    @jwt_required(refresh=True)

    def refresh():
        """
        Rafraîchir l'access token

        Headers:
            Authorization: Bearer <refresh_token>

        Returns:
            {
                "access_token": "string"
            }
        """
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)

        return jsonify({'access_token': access_token}), 200

    @api_v1.route('/auth/me', methods=['GET'])
    @jwt_required()

    def get_current_user():
        """
        Obtenir les infos de l'utilisateur connecté

        Headers:
            Authorization: Bearer <access_token>

        Returns:
            {
                "id": 123,
                "nom": "string",
                "email": "string",
                "date_inscription": "2026-01-09"
            }
        """
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        return jsonify({
            'id': user.id,
            'nom': user.nom,
            'email': user.email,
            'date_inscription': user.date_inscription.strftime('%Y-%m-%d')
        }), 200

    # ==================== DÉPENSES ====================

    @api_v1.route('/depenses', methods=['GET'])
    @jwt_required()

    def get_depenses():
        """
        Liste des dépenses avec pagination

        Query Params:
            page: int (default: 1)
            limit: int (default: 20)
            categorie_id: int (optional)
            date_debut: date (optional, format: YYYY-MM-DD)
            date_fin: date (optional)

        Returns:
            {
                "items": [...],
                "total": 123,
                "page": 1,
                "pages": 7
            }
        """
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        categorie_id = request.args.get('categorie_id', type=int)

        query = Depense.query.filter_by(user_id=user_id)

        if categorie_id:
            query = query.filter_by(categorie_id=categorie_id)

        # Filtres de dates
        date_debut = request.args.get('date_debut')
        date_fin = request.args.get('date_fin')

        if date_debut:
            from datetime import datetime
            query = query.filter(Depense.date >= datetime.strptime(date_debut, '%Y-%m-%d'))
        if date_fin:
            from datetime import datetime
            query = query.filter(Depense.date <= datetime.strptime(date_fin, '%Y-%m-%d'))

        # Pagination
        paginated = query.order_by(Depense.date.desc()).paginate(
            page=page, per_page=limit, error_out=False
        )

        items = [{
            'id': d.id,
            'nom': d.nom,
            'montant': float(d.montant),
            'date': d.date.strftime('%Y-%m-%d'),
            'categorie': {
                'id': d.categorie.id,
                'nom': d.categorie.nom
            } if d.categorie else None,
            'compte': {
                'id': d.compte.id,
                'nom': d.compte.nom
            } if d.compte else None
        } for d in paginated.items]

        return jsonify({
            'items': items,
            'total': paginated.total,
            'page': page,
            'pages': paginated.pages
        }), 200

    @api_v1.route('/depenses/<int:depense_id>', methods=['GET'])
    @jwt_required()

    def get_depense(depense_id):
        """Détails d'une dépense"""
        user_id = get_jwt_identity()
        depense = Depense.query.filter_by(id=depense_id, user_id=user_id).first()

        if not depense:
            return jsonify({'error': 'Dépense non trouvée'}), 404

        return jsonify({
            'id': depense.id,
            'nom': depense.nom,
            'montant': float(depense.montant),
            'date': depense.date.strftime('%Y-%m-%d'),
            'notes': depense.notes,
            'categorie': {
                'id': depense.categorie.id,
                'nom': depense.categorie.nom
            } if depense.categorie else None,
            'compte': {
                'id': depense.compte.id,
                'nom': depense.compte.nom
            } if depense.compte else None
        }), 200

    @api_v1.route('/depenses', methods=['POST'])
    @jwt_required()

    def create_depense():
        """
        Créer une nouvelle dépense

        Body:
            {
                "nom": "string",
                "montant": 1000,
                "date": "2026-01-09",
                "categorie_id": 1,
                "compte_id": 1,
                "notes": "string (optional)"
            }
        """
        user_id = get_jwt_identity()
        data = request.get_json()

        if not all(k in data for k in ['nom', 'montant', 'date']):
            return jsonify({'error': 'Champs obligatoires manquants'}), 400

        from datetime import datetime

        nouvelle_depense = Depense(
            user_id=user_id,
            nom=data['nom'],
            montant=float(data['montant']),
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            categorie_id=data.get('categorie_id'),
            compte_id=data.get('compte_id'),
            notes=data.get('notes')
        )

        db.session.add(nouvelle_depense)
        db.session.commit()

        return jsonify({
            'success': True,
            'depense_id': nouvelle_depense.id,
            'message': 'Dépense créée'
        }), 201

    @api_v1.route('/depenses/<int:depense_id>', methods=['PUT'])
    @jwt_required()

    def update_depense(depense_id):
        """Modifier une dépense"""
        user_id = get_jwt_identity()
        depense = Depense.query.filter_by(id=depense_id, user_id=user_id).first()

        if not depense:
            return jsonify({'error': 'Dépense non trouvée'}), 404

        data = request.get_json()

        if 'nom' in data:
            depense.nom = data['nom']
        if 'montant' in data:
            depense.montant = float(data['montant'])
        if 'date' in data:
            from datetime import datetime
            depense.date = datetime.strptime(data['date'], '%Y-%m-%d')
        if 'categorie_id' in data:
            depense.categorie_id = data['categorie_id']
        if 'compte_id' in data:
            depense.compte_id = data['compte_id']
        if 'notes' in data:
            depense.notes = data['notes']

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Dépense mise à jour'
        }), 200

    @api_v1.route('/depenses/<int:depense_id>', methods=['DELETE'])
    @jwt_required()

    def delete_depense(depense_id):
        """Supprimer une dépense"""
        user_id = get_jwt_identity()
        depense = Depense.query.filter_by(id=depense_id, user_id=user_id).first()

        if not depense:
            return jsonify({'error': 'Dépense non trouvée'}), 404

        db.session.delete(depense)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Dépense supprimée'
        }), 200

    # ==================== REVENUS ====================

    @api_v1.route('/revenus', methods=['GET'])
    @jwt_required()

    def get_revenus():
        """Liste des revenus avec pagination"""
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)

        paginated = Revenu.query.filter_by(user_id=user_id).order_by(
            Revenu.date.desc()
        ).paginate(page=page, per_page=limit, error_out=False)

        items = [{
            'id': r.id,
            'source': r.source,
            'montant': float(r.montant),
            'date': r.date.strftime('%Y-%m-%d'),
            'recurrent': r.recurrent
        } for r in paginated.items]

        return jsonify({
            'items': items,
            'total': paginated.total,
            'page': page,
            'pages': paginated.pages
        }), 200

    @api_v1.route('/revenus', methods=['POST'])
    @jwt_required()

    def create_revenu():
        """Créer un nouveau revenu"""
        user_id = get_jwt_identity()
        data = request.get_json()

        if not all(k in data for k in ['source', 'montant', 'date']):
            return jsonify({'error': 'Champs obligatoires manquants'}), 400

        from datetime import datetime

        nouveau_revenu = Revenu(
            user_id=user_id,
            source=data['source'],
            montant=float(data['montant']),
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            recurrent=data.get('recurrent', False)
        )

        db.session.add(nouveau_revenu)
        db.session.commit()

        return jsonify({
            'success': True,
            'revenu_id': nouveau_revenu.id,
            'message': 'Revenu créé'
        }), 201

    @api_v1.route('/revenus/<int:revenu_id>', methods=['DELETE'])
    @jwt_required()

    def delete_revenu(revenu_id):
        """Supprimer un revenu"""
        user_id = get_jwt_identity()
        revenu = Revenu.query.filter_by(id=revenu_id, user_id=user_id).first()

        if not revenu:
            return jsonify({'error': 'Revenu non trouvé'}), 404

        db.session.delete(revenu)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Revenu supprimé'
        }), 200

    # ==================== CATÉGORIES ====================

    @api_v1.route('/categories', methods=['GET'])
    @jwt_required()

    def get_categories():
        """Liste des catégories"""
        user_id = get_jwt_identity()
        categories = Categorie.query.filter_by(user_id=user_id).all()

        items = [{
            'id': c.id,
            'nom': c.nom,
            'type': c.type,
            'couleur': c.couleur,
            'icon': c.icon
        } for c in categories]

        return jsonify({'items': items}), 200

    @api_v1.route('/categories', methods=['POST'])
    @jwt_required()

    def create_categorie():
        """Créer une catégorie"""
        user_id = get_jwt_identity()
        data = request.get_json()

        if 'nom' not in data:
            return jsonify({'error': 'Nom requis'}), 400

        nouvelle_categorie = Categorie(
            user_id=user_id,
            nom=data['nom'],
            type=data.get('type', 'depense'),
            couleur=data.get('couleur', '#6c757d'),
            icon=data.get('icon', 'bi-tag')
        )

        db.session.add(nouvelle_categorie)
        db.session.commit()

        return jsonify({
            'success': True,
            'categorie_id': nouvelle_categorie.id
        }), 201

    # ==================== STATISTIQUES ====================

    @api_v1.route('/stats', methods=['GET'])
    @jwt_required()

    def get_stats():
        """Statistiques globales"""
        user_id = get_jwt_identity()

        from sqlalchemy import func

        total_depenses = db.session.query(func.sum(Depense.montant)).filter_by(
            user_id=user_id
        ).scalar() or 0

        total_revenus = db.session.query(func.sum(Revenu.montant)).filter_by(
            user_id=user_id
        ).scalar() or 0

        nb_depenses = Depense.query.filter_by(user_id=user_id).count()
        nb_revenus = Revenu.query.filter_by(user_id=user_id).count()

        return jsonify({
            'total_depenses': float(total_depenses),
            'total_revenus': float(total_revenus),
            'solde': float(total_revenus - total_depenses),
            'nb_depenses': nb_depenses,
            'nb_revenus': nb_revenus
        }), 200

    # Enregistrer le blueprint
    app.register_blueprint(api_v1)

    return jwt

# ==================== DOCUMENTATION SWAGGER ====================

SWAGGER_CONFIG = {
    "openapi": "3.0.0",
    "info": {
        "title": "NyangaBudget API",
        "version": "1.0.0",
        "description": "API REST pour application mobile NyangaBudget"
    },
    "servers": [
        {
            "url": "https://jolubot.pythonanywhere.com/api/v1",
            "description": "Production"
        },
        {
            "url": "http://localhost:5000/api/v1",
            "description": "Développement"
        }
    ],
    "components": {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    }
}
