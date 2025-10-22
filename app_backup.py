# NyangaBudget - Application de gestion budgétaire personnelle
#
# INSTRUCTIONS DE DÉMARRAGE (Windows):
# 1. Créer environnement virtuel: python -m venv .venv
# 2. Activer l'environnement: .venv\Scripts\activate
# 3. Installer dépendances: pip install -r requirements.txt
# 4. Lancer l'application: python app.py
# 5. Ouvrir navigateur: http://localhost:5000
#
# EXPORTS DISPONIBLES:
# - CSV: http://localhost:5000/export/csv
# - PDF: http://localhost:5000/export/pdf

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import func, extract
import plotly.graph_objs as go
import plotly
import json
import csv
from io import BytesIO, StringIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import cm
import os

# Créer le dossier data si nécessaire (avant initialisation Flask)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(BASE_DIR, 'data')
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
    print(f"[OK] Dossier 'data' cree: {data_folder}")

# Configuration de l'application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'nyanga-budget-secret-key-2025'
# Utiliser un chemin absolu pour la base de données SQLite
db_path = os.path.join(data_folder, 'nyanga.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db = SQLAlchemy(app)

# ==================== MODÈLES DE DONNÉES ====================

class Depense(db.Model):
    """Modèle pour les dépenses"""
    __tablename__ = 'depenses'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(200), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Depense {self.nom}: {self.montant}€>'


class Revenu(db.Model):
    """Modèle pour les revenus"""
    __tablename__ = 'revenus'

    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(200), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Revenu {self.source}: {self.montant}€>'


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


def calculer_statistiques(start_date=None, end_date=None):
    """Calcule les statistiques globales (avec filtrage optionnel par date)"""
    query_depenses = db.session.query(func.sum(Depense.montant))
    query_revenus = db.session.query(func.sum(Revenu.montant))

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
        Depense.date_created >= start_date if start_date else True,
        Depense.date_created <= end_date if end_date else True
    ).count()

    nb_revenus = Revenu.query.filter(
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


def generer_graphique_camembert():
    """Génère un graphique camembert de la répartition des dépenses par nom"""
    depenses = db.session.query(
        Depense.nom,
        func.sum(Depense.montant).label('total')
    ).group_by(Depense.nom).all()

    if not depenses:
        return json.dumps({})

    labels = [d.nom for d in depenses]
    values = [float(d.total) for d in depenses]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker=dict(colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'])
    )])

    fig.update_layout(
        title='Répartition des dépenses par catégorie',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def generer_graphique_mensuel():
    """Génère un graphique en barres des dépenses et revenus mensuels"""
    # Récupération des 6 derniers mois
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)

    # Agrégation des dépenses par mois
    depenses_mensuelles = db.session.query(
        func.strftime('%Y-%m', Depense.date_created).label('mois'),
        func.sum(Depense.montant).label('total')
    ).filter(Depense.date_created >= start_date).group_by('mois').all()

    # Agrégation des revenus par mois
    revenus_mensuels = db.session.query(
        func.strftime('%Y-%m', Revenu.date_created).label('mois'),
        func.sum(Revenu.montant).label('total')
    ).filter(Revenu.date_created >= start_date).group_by('mois').all()

    # Création des dictionnaires
    depenses_dict = {d.mois: float(d.total) for d in depenses_mensuelles}
    revenus_dict = {r.mois: float(r.total) for r in revenus_mensuels}

    # Liste de tous les mois
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


def generer_csv():
    """Génère un fichier CSV consolidé de toutes les transactions"""
    # Récupération des dépenses
    depenses = Depense.query.all()
    transactions_depenses = [{
        'Date': d.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        'Type': 'Dépense',
        'Description': d.nom,
        'Montant': -d.montant  # Négatif pour les dépenses
    } for d in depenses]

    # Récupération des revenus
    revenus = Revenu.query.all()
    transactions_revenus = [{
        'Date': r.date_created.strftime('%Y-%m-%d %H:%M:%S'),
        'Type': 'Revenu',
        'Description': r.source,
        'Montant': r.montant
    } for r in revenus]

    # Consolidation
    all_transactions = transactions_depenses + transactions_revenus

    # Tri par date (décroissant)
    all_transactions.sort(key=lambda x: x['Date'], reverse=True)

    return all_transactions


def generer_pdf():
    """Génère un rapport PDF avec résumé et top 10 des dépenses"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()

    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2C3E50'),
        spaceAfter=30,
        alignment=1  # Centré
    )

    # Titre
    elements.append(Paragraph('NyangaBudget - Rapport Financier', title_style))
    elements.append(Spacer(1, 0.5*cm))

    # Date du rapport
    date_rapport = datetime.now().strftime('%d/%m/%Y à %H:%M')
    elements.append(Paragraph(f'<b>Date du rapport:</b> {date_rapport}', styles['Normal']))
    elements.append(Spacer(1, 0.5*cm))

    # Statistiques globales
    stats = calculer_statistiques()

    data_stats = [
        ['Indicateur', 'Valeur'],
        ['Total Dépenses', f"{stats['total_depenses']:.2f} €"],
        ['Total Revenus', f"{stats['total_revenus']:.2f} €"],
        ['Solde', f"{stats['solde']:.2f} €"],
        ['Nombre de dépenses', str(stats['nb_depenses'])],
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

    # Top 10 des dépenses
    elements.append(Paragraph('<b>Top 10 des dépenses les plus importantes</b>', styles['Heading2']))
    elements.append(Spacer(1, 0.3*cm))

    top_depenses = Depense.query.order_by(Depense.montant.desc()).limit(10).all()

    if top_depenses:
        data_depenses = [['#', 'Description', 'Montant', 'Date']]
        for idx, d in enumerate(top_depenses, 1):
            data_depenses.append([
                str(idx),
                d.nom[:40],  # Limite à 40 caractères
                f"{d.montant:.2f} €",
                d.date_created.strftime('%d/%m/%Y')
            ])

        table_depenses = Table(data_depenses, colWidths=[1*cm, 9*cm, 3*cm, 3*cm])
        table_depenses.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E74C3C')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))

        elements.append(table_depenses)
    else:
        elements.append(Paragraph('Aucune dépense enregistrée.', styles['Normal']))

    # Construction du PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Page d'accueil - Liste des dépenses avec formulaire d'ajout"""
    depenses = Depense.query.order_by(Depense.date_created.desc()).all()
    stats = calculer_statistiques()
    return render_template('index.html', depenses=depenses, stats=stats)


@app.route('/add', methods=['POST'])
def add_depense():
    """Ajoute une nouvelle dépense"""
    nom = request.form.get('nom', '').strip()
    montant_str = request.form.get('montant', '')

    # Validation du nom
    if not nom:
        flash('Le nom de la dépense est obligatoire', 'danger')
        return redirect(url_for('index'))

    # Validation du montant
    montant, erreur = valider_montant(montant_str)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('index'))

    # Ajout en base de données
    try:
        nouvelle_depense = Depense(nom=nom, montant=montant)
        db.session.add(nouvelle_depense)
        db.session.commit()
        flash(f'Dépense "{nom}" ajoutée avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')

    return redirect(url_for('index'))


@app.route('/delete/depense/<int:id>', methods=['POST'])
def delete_depense(id):
    """Supprime une dépense"""
    try:
        depense = Depense.query.get_or_404(id)
        nom = depense.nom
        db.session.delete(depense)
        db.session.commit()
        flash(f'Dépense "{nom}" supprimée avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')

    return redirect(url_for('index'))


@app.route('/revenues')
def revenues():
    """Page de gestion des revenus"""
    revenus = Revenu.query.order_by(Revenu.date_created.desc()).all()
    stats = calculer_statistiques()
    return render_template('revenues.html', revenus=revenus, stats=stats)


@app.route('/add_revenue', methods=['POST'])
def add_revenue():
    """Ajoute un nouveau revenu"""
    source = request.form.get('source', '').strip()
    montant_str = request.form.get('montant', '')

    # Validation de la source
    if not source:
        flash('La source du revenu est obligatoire', 'danger')
        return redirect(url_for('revenues'))

    # Validation du montant
    montant, erreur = valider_montant(montant_str)
    if erreur:
        flash(erreur, 'danger')
        return redirect(url_for('revenues'))

    # Ajout en base de données
    try:
        nouveau_revenu = Revenu(source=source, montant=montant)
        db.session.add(nouveau_revenu)
        db.session.commit()
        flash(f'Revenu "{source}" ajouté avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'ajout: {str(e)}', 'danger')

    return redirect(url_for('revenues'))


@app.route('/delete/revenu/<int:id>', methods=['POST'])
def delete_revenu(id):
    """Supprime un revenu"""
    try:
        revenu = Revenu.query.get_or_404(id)
        source = revenu.source
        db.session.delete(revenu)
        db.session.commit()
        flash(f'Revenu "{source}" supprimé avec succès!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression: {str(e)}', 'danger')

    return redirect(url_for('revenues'))


@app.route('/dashboard')
def dashboard():
    """Tableau de bord avec statistiques et graphiques"""
    # Calcul des statistiques globales
    stats = calculer_statistiques()

    # Génération des graphiques
    graphique_camembert = generer_graphique_camembert()
    graphique_mensuel = generer_graphique_mensuel()

    return render_template(
        'dashboard.html',
        stats=stats,
        graphique_camembert=graphique_camembert,
        graphique_mensuel=graphique_mensuel
    )


@app.route('/export/csv')
def export_csv():
    """Export CSV de toutes les transactions"""
    try:
        transactions = generer_csv()

        # Création du fichier CSV en mémoire
        output = StringIO()
        if transactions:
            # Écrire les en-têtes
            fieldnames = ['Date', 'Type', 'Description', 'Montant']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(transactions)
        else:
            # Fichier vide avec juste les en-têtes
            output.write('Date,Type,Description,Montant\n')

        # Nom du fichier avec date
        filename = f'nyanga_transactions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'

        # Encoder en UTF-8 avec BOM pour Excel
        csv_bytes = '\ufeff' + output.getvalue()

        response = make_response(csv_bytes)
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        response.headers['Content-Type'] = 'text/csv; charset=utf-8'

        return response
    except Exception as e:
        flash(f'Erreur lors de l\'export CSV: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))


@app.route('/export/pdf')
def export_pdf():
    """Export PDF du rapport financier"""
    try:
        pdf_buffer = generer_pdf()

        # Nom du fichier avec date
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


# ==================== INITIALISATION ====================

def init_db():
    """Initialise la base de données et crée le dossier data si nécessaire"""
    with app.app_context():
        db.create_all()
        print("[OK] Base de donnees initialisee")


# ==================== POINT D'ENTRÉE ====================

if __name__ == '__main__':
    init_db()
    print("\n" + "="*50)
    print("NyangaBudget - Application demarree!")
    print("="*50)
    print("URL: http://localhost:5000")
    print("Dashboard: http://localhost:5000/dashboard")
    print("Export CSV: http://localhost:5000/export/csv")
    print("Export PDF: http://localhost:5000/export/pdf")
    print("="*50 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
