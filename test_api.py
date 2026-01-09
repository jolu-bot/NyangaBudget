"""
Script de test automatique pour l'API REST NyangaBudget
Teste tous les endpoints avec authentification JWT
"""

import requests
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000/api/v1"
# BASE_URL = "https://jolubot.pythonanywhere.com/api/v1"  # Pour production


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'


class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.test_depense_id = None
        self.test_revenu_id = None
        self.test_categorie_id = None

        self.tests_passed = 0
        self.tests_failed = 0

    def log(self, message, color=Colors.BLUE):
        print(f"{color}{message}{Colors.END}")

    def success(self, message):
        self.tests_passed += 1
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")

    def error(self, message):
        self.tests_failed += 1
        print(f"{Colors.RED}❌ {message}{Colors.END}")

    def test_register(self):
        """Test inscription"""
        self.log("\n[TEST 1] Inscription nouvel utilisateur")

        email = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@test.cm"

        response = requests.post(f"{self.base_url}/auth/register", json={
            "nom": "Test User",
            "email": email,
            "password": "test123"
        })

        if response.status_code == 201:
            data = response.json()
            self.user_id = data.get('user_id')
            self.success(f"Inscription réussie - User ID: {self.user_id}")
            return email
        else:
            self.error(f"Inscription échouée: {response.text}")
            return None

    def test_login(self, email, password="test123"):
        """Test connexion"""
        self.log("\n[TEST 2] Connexion utilisateur")

        response = requests.post(f"{self.base_url}/auth/login", json={
            "email": email,
            "password": password
        })

        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']
            self.success("Connexion réussie - Token reçu")
            return True
        else:
            self.error(f"Connexion échouée: {response.text}")
            return False

    def test_get_current_user(self):
        """Test récupération utilisateur courant"""
        self.log("\n[TEST 3] Récupération utilisateur connecté")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.base_url}/auth/me", headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.success(f"Utilisateur: {data['nom']} ({data['email']})")
            return True
        else:
            self.error(f"Échec récupération utilisateur: {response.text}")
            return False

    def test_create_categorie(self):
        """Test création catégorie"""
        self.log("\n[TEST 4] Création catégorie")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(f"{self.base_url}/categories",
                                 headers=headers,
                                 json={
                                     "nom": "Test Alimentation",
                                     "type": "depense",
                                     "couleur": "#ff6b6b",
                                     "icon": "bi-cart"
                                 })

        if response.status_code == 201:
            data = response.json()
            self.test_categorie_id = data['categorie_id']
            self.success(f"Catégorie créée - ID: {self.test_categorie_id}")
            return True
        else:
            self.error(f"Création catégorie échouée: {response.text}")
            return False

    def test_get_categories(self):
        """Test liste catégories"""
        self.log("\n[TEST 5] Liste des catégories")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.base_url}/categories", headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.success(f"Catégories récupérées: {len(data['items'])} catégorie(s)")
            return True
        else:
            self.error(f"Échec récupération catégories: {response.text}")
            return False

    def test_create_depense(self):
        """Test création dépense"""
        self.log("\n[TEST 6] Création dépense")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(f"{self.base_url}/depenses",
                                 headers=headers,
                                 json={
                                     "nom": "Test Courses",
                                     "montant": 15000,
                                     "date": datetime.now().strftime('%Y-%m-%d'),
                                     "categorie_id": self.test_categorie_id,
                                     "notes": "Dépense de test"
                                 })

        if response.status_code == 201:
            data = response.json()
            self.test_depense_id = data['depense_id']
            self.success(f"Dépense créée - ID: {self.test_depense_id}")
            return True
        else:
            self.error(f"Création dépense échouée: {response.text}")
            return False

    def test_get_depenses(self):
        """Test liste dépenses"""
        self.log("\n[TEST 7] Liste des dépenses (pagination)")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.base_url}/depenses?page=1&limit=10",
                                headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.success(f"Dépenses: {len(data['items'])} items, Total: {data['total']}")
            return True
        else:
            self.error(f"Échec récupération dépenses: {response.text}")
            return False

    def test_get_depense_detail(self):
        """Test détail dépense"""
        self.log("\n[TEST 8] Détails d'une dépense")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(
            f"{self.base_url}/depenses/{self.test_depense_id}",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            self.success(f"Détails: {data['nom']} - {data['montant']} FCFA")
            return True
        else:
            self.error(f"Échec récupération détail: {response.text}")
            return False

    def test_update_depense(self):
        """Test modification dépense"""
        self.log("\n[TEST 9] Modification dépense")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.put(
            f"{self.base_url}/depenses/{self.test_depense_id}",
            headers=headers,
            json={
                "nom": "Test Courses Modifié",
                "montant": 20000
            }
        )

        if response.status_code == 200:
            self.success("Dépense modifiée avec succès")
            return True
        else:
            self.error(f"Modification échouée: {response.text}")
            return False

    def test_create_revenu(self):
        """Test création revenu"""
        self.log("\n[TEST 10] Création revenu")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.post(f"{self.base_url}/revenus",
                                 headers=headers,
                                 json={
                                     "source": "Test Salaire",
                                     "montant": 500000,
                                     "date": datetime.now().strftime('%Y-%m-%d'),
                                     "recurrent": True
                                 })

        if response.status_code == 201:
            data = response.json()
            self.test_revenu_id = data['revenu_id']
            self.success(f"Revenu créé - ID: {self.test_revenu_id}")
            return True
        else:
            self.error(f"Création revenu échouée: {response.text}")
            return False

    def test_get_revenus(self):
        """Test liste revenus"""
        self.log("\n[TEST 11] Liste des revenus")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.base_url}/revenus", headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.success(f"Revenus: {len(data['items'])} items")
            return True
        else:
            self.error(f"Échec récupération revenus: {response.text}")
            return False

    def test_get_stats(self):
        """Test statistiques"""
        self.log("\n[TEST 12] Statistiques globales")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(f"{self.base_url}/stats", headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.success(f"Stats - Revenus: {data['total_revenus']}, Dépenses: {data['total_depenses']}, Solde: {data['solde']}")
            return True
        else:
            self.error(f"Échec récupération stats: {response.text}")
            return False

    def test_refresh_token(self):
        """Test rafraîchissement token"""
        self.log("\n[TEST 13] Rafraîchissement token")

        headers = {"Authorization": f"Bearer {self.refresh_token}"}
        response = requests.post(f"{self.base_url}/auth/refresh", headers=headers)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.success("Token rafraîchi avec succès")
            return True
        else:
            self.error(f"Rafraîchissement échoué: {response.text}")
            return False

    def test_delete_depense(self):
        """Test suppression dépense"""
        self.log("\n[TEST 14] Suppression dépense")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.delete(
            f"{self.base_url}/depenses/{self.test_depense_id}",
            headers=headers
        )

        if response.status_code == 200:
            self.success("Dépense supprimée")
            return True
        else:
            self.error(f"Suppression échouée: {response.text}")
            return False

    def test_delete_revenu(self):
        """Test suppression revenu"""
        self.log("\n[TEST 15] Suppression revenu")

        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.delete(
            f"{self.base_url}/revenus/{self.test_revenu_id}",
            headers=headers
        )

        if response.status_code == 200:
            self.success("Revenu supprimé")
            return True
        else:
            self.error(f"Suppression échouée: {response.text}")
            return False

    def run_all_tests(self):
        """Exécuter tous les tests"""
        print("\n" + "=" * 60)
        print("🧪 TESTS API REST - NyangaBudget")
        print("=" * 60)
        print(f"Base URL: {self.base_url}")
        print("=" * 60)

        # Test inscription et connexion
        email = self.test_register()
        if not email:
            self.log("\n⚠️  Impossible de continuer sans inscription", Colors.RED)
            return

        if not self.test_login(email):
            self.log("\n⚠️  Impossible de continuer sans connexion", Colors.RED)
            return

        # Tests avec authentification
        self.test_get_current_user()
        self.test_create_categorie()
        self.test_get_categories()
        self.test_create_depense()
        self.test_get_depenses()
        self.test_get_depense_detail()
        self.test_update_depense()
        self.test_create_revenu()
        self.test_get_revenus()
        self.test_get_stats()
        self.test_refresh_token()

        # Tests de suppression
        self.test_delete_depense()
        self.test_delete_revenu()

        # Résumé
        print("\n" + "=" * 60)
        print("📊 RÉSUMÉ DES TESTS")
        print("=" * 60)
        total = self.tests_passed + self.tests_failed
        success_rate = (self.tests_passed / total * 100) if total > 0 else 0

        print(f"{Colors.GREEN}✅ Tests réussis: {self.tests_passed}{Colors.END}")
        print(f"{Colors.RED}❌ Tests échoués: {self.tests_failed}{Colors.END}")
        print(f"📈 Taux de réussite: {success_rate:.1f}%")
        print("=" * 60)

        if self.tests_failed == 0:
            print(f"\n{Colors.GREEN}🎉 TOUS LES TESTS SONT PASSÉS !{Colors.END}\n")
        else:
            print(f"\n{Colors.YELLOW}⚠️  CERTAINS TESTS ONT ÉCHOUÉ{Colors.END}\n")


if __name__ == '__main__':
    import sys

    # Permettre de spécifier l'URL en argument
    base_url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL

    tester = APITester(base_url)
    tester.run_all_tests()
