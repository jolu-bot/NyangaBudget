# 🏦 NyangaBudget 2.0

**Plateforme Familiale Révolutionnaire de Gestion Financière & Patrimoniale**

Une application Flask complète pour gérer votre budget familial avec des fonctionnalités innovantes jamais vues sur le marché : coffre-fort crypté militaire (AES-256), testament numérique, IA de scoring financier, et gestion familiale collaborative par QR code.

---

## 🌟 Fonctionnalités Révolutionnaires

### 💰 Gestion Financière Classique
- ✅ **Dépenses & Revenus** - Suivi détaillé avec catégories personnalisables
- ✅ **Budgets Mensuels** - Alertes intelligentes par seuils configurables
- ✅ **Catégories Colorées** - Organisation visuelle avec icônes Bootstrap
- ✅ **Dashboard Interactif** - Graphiques Plotly (camembert, barres, tendances)
- ✅ **Export PDF & CSV** - Rapports professionnels générés automatiquement

### 🏦 Multi-Comptes Bancaires ⭐
- Gestion illimitée de comptes (Mobile Money, Banque, Épargne, Cash, Crypto)
- Solde global consolidé en temps réel
- Transferts inter-comptes avec **hash SHA-256 blockchain-like**
- Historique immutable et traçable
- Personnalisation complète (couleurs, icônes)

### 🔐 Coffre-Fort Crypté AES-256 ⭐
- Stockage ultra-sécurisé de documents sensibles
- Cryptage militaire AES-256 avec bibliothèque `cryptography`
- Types supportés : Documents, Mots de passe, Notes, Codes PIN
- Upload et cryptage automatique de fichiers
- Marquage des documents critiques
- Décryptage à la demande uniquement

### 🎁 Héritage Familial & Testament Numérique ⭐
- Enregistrement des biens (immobilier, véhicule, comptes, objets de valeur)
- Ajout de bénéficiaires avec pourcentages de répartition
- **Messages personnels posthumes** cryptés
- Conditions de déblocage intelligentes (inactivité 30j, décès, urgence)
- Stockage crypté des documents légaux

### 👨‍👩‍👧‍👦 Gestion Familiale Collaborative ⭐
- Création de familles avec codes d'invitation uniques (8 caractères)
- **Génération de QR codes** pour invitations instantanées
- Système de validation par chef de famille
- Rôles hiérarchiques : Chef, Parent, Enfant, Membre, Invité
- Demandes d'adhésion avec workflow d'acceptation/refus

### 🤖 IA Prédictive & Score de Santé Financière ⭐
- **Algorithme de scoring intelligent (0-100)**
- Analyse de 5 facteurs clés :
  * Solde positif/négatif
  * Diversification des comptes
  * Respect des budgets
  * Régularité des revenus
  * Ratio dépenses/revenus
- Niveaux : Critique → Faible → Moyen → Bon → Excellent
- Suggestions personnalisées basées sur l'IA
- Affichage en un clic via bouton navbar

### 🔔 Notifications en Temps Réel ⭐
- Système complet de notifications pour tous les événements
- Badge de compteur dynamique (mise à jour toutes les 30s)
- 4 niveaux de priorité (basse, normale, haute, critique)
- Types : budget, famille, heritage, compte, coffre, alerte
- Liens directs vers les pages concernées

### ⏰ Rappels & Échéances ⭐ NEW
- Création de rappels de paiement et échéances
- **Rappels récurrents** (hebdomadaire, mensuel, annuel)
- Notifications automatiques avant échéance
- Distinction visuelle : urgents (rouge) vs à venir (bleu)
- Historique des rappels complétés

### 🎯 Objectifs d'Épargne ⭐ NEW
- Définition d'objectifs financiers personnels et familiaux
- Suivi visuel avec barres de progression animées
- Contributions progressives avec célébration à l'atteinte
- Partage d'objectifs entre membres de la famille
- Calcul automatique du temps restant

---

## 🚀 Installation Locale (Windows)

### Prérequis
- Python 3.11+ (testé sur 3.11 et 3.13)
- Git (optionnel)

### Étapes d'Installation

```bash
# 1. Cloner le dépôt (ou télécharger le ZIP)
git clone https://github.com/votre-username/NyangaBudget.git
cd NyangaBudget

# 2. Créer un environnement virtuel
python -m venv .venv

# 3. Activer l'environnement
.venv\Scripts\activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
python app.py

# 6. Ouvrir dans le navigateur
http://localhost:5000
```

### Compte de Test par Défaut
```
Email : admin@nyanga.cm
Mot de passe : admin123
```

---

## 📦 Déploiement sur Render

### Méthode Rapide (recommandée)

1. **Créer un compte sur Render.com**
   - Aller sur https://render.com
   - S'inscrire gratuitement

2. **Connecter votre dépôt GitHub**
   - Pusher le code sur GitHub
   - Sur Render : New → Web Service
   - Connecter votre repository

3. **Configuration Automatique**
   - Render détectera automatiquement `render.yaml`
   - Build Command : `pip install -r requirements.txt`
   - Start Command : `gunicorn app:app`
   - Instance Type : Free

4. **Variables d'Environnement (optionnel)**
   - `SECRET_KEY` : Généré automatiquement par Render
   - `PYTHON_VERSION` : 3.11.0

5. **Déployer**
   - Cliquer sur "Create Web Service"
   - Attendre 3-5 minutes
   - Votre app est en ligne ! 🎉

### URL de Production
```
https://nyangabudget.onrender.com
```

**Note :** Le plan gratuit de Render met l'app en veille après 15 min d'inactivité. Le premier chargement peut prendre 30-60 secondes.

---

## 🗂️ Structure du Projet

```
NyangaBudget/
├── app.py                    # Application Flask principale (2500+ lignes)
├── requirements.txt          # Dépendances Python
├── Procfile                  # Configuration Gunicorn
├── render.yaml              # Configuration Render
├── README.md                # Ce fichier
├── .gitignore               # Fichiers à ignorer par Git
│
├── data/
│   └── nyanga_v2.db         # Base de données SQLite (auto-créée)
│
├── uploads/
│   ├── vault/               # Fichiers cryptés du coffre-fort
│   └── heritage/            # Documents héritage cryptés
│
├── static/
│   ├── style.css            # Styles personnalisés + dark mode
│   └── darkmode.js          # Script pour le mode sombre
│
└── templates/               # Templates Jinja2 (16 fichiers)
    ├── base.html            # Template de base avec navbar
    ├── login.html           # Page de connexion
    ├── register.html        # Page d'inscription
    ├── index.html           # Gestion des dépenses
    ├── revenues.html        # Gestion des revenus
    ├── comptes.html         # Multi-comptes bancaires ⭐
    ├── categories.html      # Catégories personnalisées
    ├── budgets.html         # Budgets mensuels
    ├── coffre_fort.html     # Coffre-fort crypté ⭐
    ├── heritage.html        # Testament numérique ⭐
    ├── famille.html         # Gestion familiale ⭐
    ├── rappels.html         # Rappels & échéances ⭐
    ├── objectifs.html       # Objectifs d'épargne ⭐
    ├── notifications.html   # Centre de notifications ⭐
    ├── dashboard.html       # Graphiques et stats
    └── report.html          # Rapport PDF
```

---

## 🛠️ Technologies Utilisées

### Backend
- **Flask 3.0** - Framework web Python
- **Flask-SQLAlchemy 3.1** - ORM pour gestion de base de données
- **Flask-Login 0.6** - Gestion d'authentification
- **SQLite** - Base de données (production : PostgreSQL recommandé)

### Sécurité & Cryptographie
- **cryptography 41.0** - Cryptage AES-256 pour coffre-fort et héritage
- **Werkzeug** - Hachage de mots de passe avec bcrypt
- **qrcode 7.4** - Génération de QR codes d'invitation
- **Pillow 10.0** - Support des images QR

### Visualisation & Exports
- **Plotly 5.18** - Graphiques interactifs (pie, bar, line charts)
- **ReportLab 4.0** - Génération de PDF professionnels
- **openpyxl 3.1** - Export Excel (bonus)

### Déploiement
- **Gunicorn 21.2** - Serveur WSGI pour production
- **Render** - Plateforme de déploiement cloud

---

## 🔐 Sécurité Implémentée

1. **Cryptage AES-256** pour coffre-fort et documents héritage
2. **Hash SHA-256** pour traçabilité blockchain-like des transferts
3. **Hachage bcrypt** des mots de passe utilisateurs
4. **Validation admin obligatoire** pour adhésions familiales
5. **Codes d'invitation uniques** (8 caractères alphanumériques)
6. **QR codes sécurisés** pour invitations familiales
7. **Isolation complète des données** par utilisateur
8. **Protection CSRF** sur tous les formulaires
9. **Sessions Flask-Login** sécurisées

---

## 💡 Innovations Uniques au Marché

1. **Testament numérique avec déblocage d'urgence** - Système unique de gestion d'héritage avec messages posthumes cryptés
2. **Coffre-fort familial crypté AES-256** - Partage sécurisé de documents ultra-sensibles entre membres de la famille
3. **Invitations familiales par QR code** - Onboarding simplifié pour membres non-tech-savvy
4. **IA de scoring financier 0-100** - Évaluation intelligente avec suggestions personnalisées
5. **Hash blockchain pour transferts** - Traçabilité et immutabilité des transactions inter-comptes
6. **Multi-comptes avec vision globale** - Consolidation automatique de tous vos comptes financiers
7. **Rappels récurrents intelligents** - Automation des échéances répétitives
8. **Objectifs d'épargne collaboratifs** - Projets familiaux partagés

---

## 🌍 Localisation

### Devise : FCFA (Franc CFA - Cameroun)
- Format : `1 000 000 FCFA` (séparateurs de milliers)
- Champs numériques : `step="1"` (pas de centimes)
- Symbole : FCFA (après le montant)

### Langue : Français
- Interface entièrement en français
- Messages d'erreur et notifications en français

---

## 📊 Modèles de Base de Données (15 tables)

### Utilisateurs & Auth
- `User` - Utilisateurs avec authentification
- `Categorie` - Catégories personnalisées

### Finances Classiques
- `Depense` - Dépenses avec catégories
- `Revenu` - Sources de revenus
- `Budget` - Budgets mensuels avec alertes

### Innovations Révolutionnaires
- `CompteBancaire` - Comptes multiples
- `TransfertCompte` - Transferts inter-comptes avec hash
- `Famille` - Familles avec codes d'invitation
- `MembreFamille` - Relations familiales avec rôles
- `CoffreFort` - Documents cryptés
- `Heritage` - Biens testamentaires
- `Beneficiaire` - Héritiers avec pourcentages
- `Notification` - Système de notifications
- `ScoreSante` - Historique des scores financiers
- `Rappel` - Rappels et échéances
- `ObjectifFinancier` - Objectifs d'épargne

---

## 👨‍💻 Développement

### Lancer en mode Debug
```bash
python app.py
# L'application se lance sur http://localhost:5000
# Le mode debug est activé par défaut (rechargement auto)
```

### Variables d'Environnement
```bash
# .env (créer si production)
SECRET_KEY=votre-cle-secrete-ultra-longue-et-aleatoire
DATABASE_URL=postgresql://user:pass@host:5432/dbname  # Si PostgreSQL
MASTER_ENCRYPTION_KEY=cle-32-bytes-pour-cryptage-fernet
```

### Tests Manuels Recommandés
1. ✅ Créer un utilisateur
2. ✅ Ajouter des dépenses/revenus
3. ✅ Créer 2 comptes bancaires et faire un transfert
4. ✅ Créer une famille et générer le QR code
5. ✅ Ajouter un document au coffre-fort
6. ✅ Créer un bien d'héritage avec bénéficiaire
7. ✅ Vérifier le score de santé financière
8. ✅ Créer un rappel récurrent
9. ✅ Définir un objectif d'épargne

---

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

## 📝 License

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

---

## 👤 Auteur

**Propulsé par JoYed'S**

- Application développée avec Claude Code (Anthropic)
- Destinée au marché camerounais et africain
- Focus sur l'inclusion financière familiale

---

## 🆘 Support & Contact

- 📧 Email : support@nyangabudget.cm
- 🐛 Issues : [GitHub Issues](https://github.com/votre-username/NyangaBudget/issues)
- 📖 Documentation : Ce README + commentaires dans le code

---

## 🎉 Remerciements

- **Communauté Flask** pour le framework robuste
- **Anthropic Claude** pour l'assistance au développement
- **Bootstrap** pour l'UI responsive
- **Plotly** pour les graphiques interactifs
- **Cameroun** 🇨🇲 pour l'inspiration

---

**⭐ Si ce projet vous plaît, n'oubliez pas de lui donner une étoile sur GitHub !**

---

_Dernière mise à jour : Janvier 2025_
