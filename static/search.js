/* ==================== RECHERCHE GLOBALE MODERNE ==================== */

class GlobalSearch {
    constructor() {
        this.searchInput = null;
        this.searchResults = null;
        this.debounceTimer = null;
        this.init();
    }

    init() {
        // Créer la barre de recherche
        this.createSearchBar();
        
        // Raccourci clavier: Ctrl+K ou Cmd+K
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                this.searchInput.focus();
            }
            
            // Échap pour fermer
            if (e.key === 'Escape') {
                this.closeResults();
            }
        });
    }

    createSearchBar() {
        // Chercher si existe déjà
        let searchContainer = document.querySelector('.global-search-container');
        
        if (!searchContainer) {
            // Créer le conteneur
            searchContainer = document.createElement('div');
            searchContainer.className = 'search-modern global-search-container';
            searchContainer.innerHTML = `
                <input type="text" 
                       id="global-search-input" 
                       placeholder="Rechercher... (Ctrl+K)"
                       autocomplete="off">
                <i class="bi bi-search search-icon"></i>
                <div id="global-search-results" class="search-results" style="display: none;"></div>
            `;
            
            // Insérer après la navbar
            const navbar = document.querySelector('.navbar');
            if (navbar && navbar.nextSibling) {
                navbar.parentNode.insertBefore(searchContainer, navbar.nextSibling);
            }
        }
        
        this.searchInput = document.getElementById('global-search-input');
        this.searchResults = document.getElementById('global-search-results');
        
        // Événements
        this.searchInput.addEventListener('input', (e) => this.handleSearch(e.target.value));
        this.searchInput.addEventListener('focus', () => {
            if (this.searchInput.value.length > 0) {
                this.searchResults.style.display = 'block';
            }
        });
        
        // Fermer au clic extérieur
        document.addEventListener('click', (e) => {
            if (!searchContainer.contains(e.target)) {
                this.closeResults();
            }
        });
    }

    handleSearch(query) {
        clearTimeout(this.debounceTimer);
        
        if (query.length < 2) {
            this.closeResults();
            return;
        }
        
        // Debounce de 300ms
        this.debounceTimer = setTimeout(() => {
            this.performSearch(query);
        }, 300);
    }

    async performSearch(query) {
        try {
            // Afficher le loader
            this.showLoading();
            
            const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (!response.ok) throw new Error('Erreur de recherche');
            
            const data = await response.json();
            this.displayResults(data);
            
        } catch (error) {
            console.error('Erreur de recherche:', error);
            this.displayError();
        }
    }

    showLoading() {
        this.searchResults.innerHTML = `
            <div class="search-loading">
                <div class="spinner-border spinner-border-sm text-primary" role="status">
                    <span class="visually-hidden">Recherche...</span>
                </div>
                <span class="ms-2">Recherche en cours...</span>
            </div>
        `;
        this.searchResults.style.display = 'block';
    }

    displayResults(data) {
        if (data.total === 0) {
            this.searchResults.innerHTML = `
                <div class="search-no-results">
                    <i class="bi bi-inbox"></i>
                    <p>Aucun résultat trouvé</p>
                </div>
            `;
            return;
        }
        
        let html = '';
        
        // Dépenses
        if (data.depenses && data.depenses.length > 0) {
            html += '<div class="search-section">';
            html += '<h6 class="search-section-title"><i class="bi bi-cart"></i> Dépenses</h6>';
            data.depenses.forEach(item => {
                html += `
                    <a href="/depenses" class="search-result-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>${this.highlightQuery(item.nom, data.query)}</strong>
                                <small class="d-block text-muted">${item.categorie || 'Sans catégorie'}</small>
                            </div>
                            <span class="badge bg-danger">${this.formatCurrency(item.montant)}</span>
                        </div>
                    </a>
                `;
            });
            html += '</div>';
        }
        
        // Revenus
        if (data.revenus && data.revenus.length > 0) {
            html += '<div class="search-section">';
            html += '<h6 class="search-section-title"><i class="bi bi-wallet2"></i> Revenus</h6>';
            data.revenus.forEach(item => {
                html += `
                    <a href="/revenues" class="search-result-item">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <strong>${this.highlightQuery(item.source, data.query)}</strong>
                                <small class="d-block text-muted">${item.date}</small>
                            </div>
                            <span class="badge bg-success">${this.formatCurrency(item.montant)}</span>
                        </div>
                    </a>
                `;
            });
            html += '</div>';
        }
        
        // Catégories
        if (data.categories && data.categories.length > 0) {
            html += '<div class="search-section">';
            html += '<h6 class="search-section-title"><i class="bi bi-tag"></i> Catégories</h6>';
            data.categories.forEach(item => {
                html += `
                    <a href="/categories" class="search-result-item">
                        <div>
                            <strong>${this.highlightQuery(item.nom, data.query)}</strong>
                            <small class="d-block text-muted">${item.icon || '📁'} ${item.count || 0} éléments</small>
                        </div>
                    </a>
                `;
            });
            html += '</div>';
        }
        
        // Footer avec total
        html += `
            <div class="search-footer">
                <small class="text-muted">${data.total} résultat(s) trouvé(s)</small>
            </div>
        `;
        
        this.searchResults.innerHTML = html;
        this.searchResults.style.display = 'block';
    }

    displayError() {
        this.searchResults.innerHTML = `
            <div class="search-error">
                <i class="bi bi-exclamation-triangle"></i>
                <p>Une erreur est survenue</p>
            </div>
        `;
    }

    highlightQuery(text, query) {
        if (!query) return text;
        const regex = new RegExp(`(${query})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('fr-FR', { 
            style: 'currency', 
            currency: 'XAF',
            maximumFractionDigits: 0
        }).format(amount);
    }

    closeResults() {
        if (this.searchResults) {
            this.searchResults.style.display = 'none';
        }
    }
}

// Initialiser au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.globalSearch = new GlobalSearch();
});

// Styles CSS pour la recherche (à ajouter dans modern-ui.css ou inline)
const searchStyles = `
.global-search-container {
    padding: 20px 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    position: relative;
    z-index: 1000;
}

.search-results {
    position: absolute;
    top: calc(100% + 10px);
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    max-width: 600px;
    max-height: 500px;
    overflow-y: auto;
    background: white;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    z-index: 1001;
}

.search-section {
    padding: 15px;
    border-bottom: 1px solid #f0f0f0;
}

.search-section:last-child {
    border-bottom: none;
}

.search-section-title {
    font-size: 0.85rem;
    text-transform: uppercase;
    color: #667eea;
    margin-bottom: 10px;
    font-weight: 700;
}

.search-result-item {
    display: block;
    padding: 10px;
    margin-bottom: 5px;
    border-radius: 8px;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s;
}

.search-result-item:hover {
    background: #f8f9fa;
    transform: translateX(5px);
}

.search-result-item strong {
    display: block;
    margin-bottom: 2px;
}

.search-result-item mark {
    background: #fff3cd;
    padding: 2px 4px;
    border-radius: 3px;
}

.search-loading,
.search-no-results,
.search-error {
    padding: 40px;
    text-align: center;
    color: #6c757d;
}

.search-loading i,
.search-no-results i,
.search-error i {
    font-size: 3rem;
    display: block;
    margin-bottom: 15px;
    opacity: 0.5;
}

.search-footer {
    padding: 10px 15px;
    background: #f8f9fa;
    border-top: 1px solid #e9ecef;
    text-align: center;
}

body.dark-mode .search-results {
    background: #2a2a2a;
    color: #e0e0e0;
}

body.dark-mode .search-result-item:hover {
    background: #333;
}

body.dark-mode .search-footer {
    background: #1a1a1a;
    border-top-color: #424242;
}
`;

// Injecter les styles
if (!document.getElementById('global-search-styles')) {
    const styleElement = document.createElement('style');
    styleElement.id = 'global-search-styles';
    styleElement.textContent = searchStyles;
    document.head.appendChild(styleElement);
}
