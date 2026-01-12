// ==================== MODERN NAVBAR FUNCTIONALITY ====================

document.addEventListener('DOMContentLoaded', function() {
    
    // ==================== DROPDOWN SECURITY MENU ====================
    const dropdowns = document.querySelectorAll('.dropdown-modern');
    
    dropdowns.forEach(dropdown => {
        const button = dropdown.querySelector('.nav-link-modern');
        const menu = dropdown.querySelector('.dropdown-menu-modern');
        let timeoutId;
        
        if (button && menu) {
            // Show dropdown on hover
            const showDropdown = () => {
                clearTimeout(timeoutId);
                menu.style.opacity = '1';
                menu.style.visibility = 'visible';
                menu.style.transform = 'translateY(0)';
                menu.style.pointerEvents = 'auto';
                menu.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            };
            
            // Hide dropdown with delay
            const hideDropdown = () => {
                timeoutId = setTimeout(() => {
                    menu.style.opacity = '0';
                    menu.style.visibility = 'hidden';
                    menu.style.transform = 'translateY(-10px)';
                    menu.style.pointerEvents = 'none';
                    menu.style.transition = 'opacity 0.3s ease, transform 0.3s ease, visibility 0s linear 0.3s';
                }, 300);
            };
            
            dropdown.addEventListener('mouseenter', showDropdown);
            dropdown.addEventListener('mouseleave', hideDropdown);
            button.addEventListener('mouseenter', showDropdown);
            menu.addEventListener('mouseenter', () => clearTimeout(timeoutId));
            menu.addEventListener('mouseleave', hideDropdown);
        }
    });
    
    // ==================== MOBILE MENU TOGGLE ====================
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            mobileMenu.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
        });

        // Close mobile menu when clicking on a link
        const mobileLinks = mobileMenu.querySelectorAll('.mobile-nav-link');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenuToggle.classList.remove('active');
                mobileMenu.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // ==================== SEARCH MODAL ====================
    const searchModal = document.getElementById('searchModal');
    const searchToggle = document.getElementById('searchToggle');
    const searchModalClose = document.getElementById('searchModalClose');
    const globalSearchInput = document.getElementById('globalSearch');
    
    if (searchToggle && searchModal) {
        searchToggle.addEventListener('click', () => {
            searchModal.classList.add('active');
            document.body.style.overflow = 'hidden';
            setTimeout(() => {
                if (globalSearchInput) globalSearchInput.focus();
            }, 300);
        });
    }
    
    if (searchModalClose && searchModal) {
        searchModalClose.addEventListener('click', () => {
            searchModal.classList.remove('active');
            document.body.style.overflow = '';
        });
    }
    
    // Close modal on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && searchModal && searchModal.classList.contains('active')) {
            searchModal.classList.remove('active');
            document.body.style.overflow = '';
        }
    });
    
    // Close modal on outside click
    if (searchModal) {
        searchModal.addEventListener('click', (e) => {
            if (e.target === searchModal) {
                searchModal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    }

    // ==================== SEARCH FUNCTIONALITY ====================
    const searchResults = document.querySelector('.search-results');
    let searchTimeout;

    function performSearch(query) {
        if (query.length < 2) {
            if (searchResults) searchResults.classList.remove('show');
            return;
        }

        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(async () => {
            try {
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                if (!response.ok) throw new Error('Search failed');
                
                const results = await response.json();
                displaySearchResults(results);
            } catch (error) {
                console.error('Search error:', error);
                if (searchResults) {
                    searchResults.innerHTML = '<div class="p-3 text-muted">Erreur lors de la recherche</div>';
                    searchResults.classList.add('show');
                }
            }
        }, 300);
    }

    function displaySearchResults(results) {
        if (!searchResults) return;

        if (!results || Object.keys(results).length === 0) {
            searchResults.innerHTML = '<div class="p-3 text-muted">Aucun résultat trouvé</div>';
            searchResults.classList.add('show');
            return;
        }

        let html = '<div class="p-2">';
        
        // Revenus
        if (results.revenus && results.revenus.length > 0) {
            html += '<div class="search-category mb-2"><div class="fw-bold px-2 py-1 text-muted small">REVENUS</div>';
            results.revenus.forEach(item => {
                html += `
                    <a href="/revenues" class="search-item d-block p-2 rounded text-decoration-none">
                        <div class="d-flex align-items-center gap-2">
                            <i class="bi bi-cash-coin text-success"></i>
                            <div>
                                <div class="fw-medium">${item.montant}€ - ${item.source}</div>
                                <div class="small text-muted">${new Date(item.date).toLocaleDateString()}</div>
                            </div>
                        </div>
                    </a>`;
            });
            html += '</div>';
        }

        // Dépenses
        if (results.depenses && results.depenses.length > 0) {
            html += '<div class="search-category mb-2"><div class="fw-bold px-2 py-1 text-muted small">DÉPENSES</div>';
            results.depenses.forEach(item => {
                html += `
                    <a href="/comptes" class="search-item d-block p-2 rounded text-decoration-none">
                        <div class="d-flex align-items-center gap-2">
                            <i class="bi bi-cart text-danger"></i>
                            <div>
                                <div class="fw-medium">${item.montant}€ - ${item.categorie}</div>
                                <div class="small text-muted">${item.description || ''}</div>
                            </div>
                        </div>
                    </a>`;
            });
            html += '</div>';
        }

        // Budgets
        if (results.budgets && results.budgets.length > 0) {
            html += '<div class="search-category mb-2"><div class="fw-bold px-2 py-1 text-muted small">BUDGETS</div>';
            results.budgets.forEach(item => {
                html += `
                    <a href="/budgets" class="search-item d-block p-2 rounded text-decoration-none">
                        <div class="d-flex align-items-center gap-2">
                            <i class="bi bi-wallet2 text-primary"></i>
                            <div>
                                <div class="fw-medium">${item.categorie}</div>
                                <div class="small text-muted">Budget: ${item.montant_prevu}€</div>
                            </div>
                        </div>
                    </a>`;
            });
            html += '</div>';
        }

        // Objectifs
        if (results.objectifs && results.objectifs.length > 0) {
            html += '<div class="search-category mb-2"><div class="fw-bold px-2 py-1 text-muted small">OBJECTIFS</div>';
            results.objectifs.forEach(item => {
                html += `
                    <a href="/objectifs" class="search-item d-block p-2 rounded text-decoration-none">
                        <div class="d-flex align-items-center gap-2">
                            <i class="bi bi-trophy text-warning"></i>
                            <div>
                                <div class="fw-medium">${item.nom}</div>
                                <div class="small text-muted">Objectif: ${item.montant_cible}€</div>
                            </div>
                        </div>
                    </a>`;
            });
            html += '</div>';
        }

        html += '</div>';
        searchResults.innerHTML = html;
        searchResults.classList.add('show');

        // Add hover styles to search items
        const searchItems = searchResults.querySelectorAll('.search-item');
        searchItems.forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.background = 'rgba(102, 126, 234, 0.1)';
            });
            item.addEventListener('mouseleave', function() {
                this.style.background = 'transparent';
            });
        });
    }

    // Attach search event listeners
    if (globalSearchInput) {
        globalSearchInput.addEventListener('input', (e) => performSearch(e.target.value));
        globalSearchInput.addEventListener('focus', function() {
            if (this.value.length >= 2) {
                performSearch(this.value);
            }
        });
    }

    const searchInputMobile = document.querySelector('.mobile-search .search-input');
    if (searchInputMobile) {
        searchInputMobile.addEventListener('input', (e) => performSearch(e.target.value));
    }

    // Close search results when clicking outside
    document.addEventListener('click', function(e) {
        if (searchResults && 
            !searchResults.contains(e.target) && 
            e.target !== globalSearchInput && 
            e.target !== searchInputMobile) {
            searchResults.classList.remove('show');
        }
    });

    // ==================== NAVBAR SCROLL EFFECT ====================
    const navbar = document.querySelector('.modern-navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });

    // ==================== ACTIVE LINK HIGHLIGHTING ====================
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link-modern, .mobile-nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });

    // ==================== NOTIFICATION BELL ANIMATION ====================
    const notificationBtn = document.querySelector('.action-btn[href*="notifications"]');
    if (notificationBtn) {
        notificationBtn.addEventListener('mouseenter', function() {
            const icon = this.querySelector('i');
            if (icon) {
                icon.style.animation = 'swing 0.6s ease-in-out';
                setTimeout(() => {
                    icon.style.animation = '';
                }, 600);
            }
        });
    }
});

// ==================== NOTIFICATION BELL SWING ANIMATION ====================
const style = document.createElement('style');
style.textContent = `
    @keyframes swing {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(15deg); }
        50% { transform: rotate(-15deg); }
        75% { transform: rotate(10deg); }
    }
`;
document.head.appendChild(style);
