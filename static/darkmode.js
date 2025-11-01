/**
 * NyangaBudget - Dark Mode Toggle Script
 * Gestion du mode sombre avec sauvegarde en localStorage
 */

(function() {
    'use strict';

    // Sélecteurs DOM
    const toggleButton = document.getElementById('darkModeToggle');
    const toggleIcon = document.getElementById('darkModeIcon');
    const body = document.body;

    // Clé de stockage localStorage
    const STORAGE_KEY = 'nyangaBudgetDarkMode';

    /**
     * Active le mode sombre
     */
    function enableDarkMode() {
        body.classList.add('dark-mode');
        toggleIcon.classList.remove('bi-moon-stars-fill');
        toggleIcon.classList.add('bi-sun-fill');
        localStorage.setItem(STORAGE_KEY, 'enabled');
    }

    /**
     * Désactive le mode sombre
     */
    function disableDarkMode() {
        body.classList.remove('dark-mode');
        toggleIcon.classList.remove('bi-sun-fill');
        toggleIcon.classList.add('bi-moon-stars-fill');
        localStorage.setItem(STORAGE_KEY, 'disabled');
    }

    /**
     * Bascule entre mode sombre et mode clair
     */
    function toggleDarkMode() {
        if (body.classList.contains('dark-mode')) {
            disableDarkMode();
        } else {
            enableDarkMode();
        }
    }

    /**
     * Détecte si c'est la nuit selon l'heure locale
     * Nuit = entre 18h00 et 6h00
     */
    function isNightTime() {
        const now = new Date();
        const hour = now.getHours();
        return hour >= 18 || hour < 6;
    }

    /**
     * Initialise le mode sombre au chargement de la page
     */
    function initDarkMode() {
        // Vérifie la préférence sauvegardée
        const savedMode = localStorage.getItem(STORAGE_KEY);

        if (savedMode === 'enabled') {
            enableDarkMode();
        } else if (savedMode === 'disabled') {
            disableDarkMode();
        } else {
            // Si aucune préférence sauvegardée, utilise préférence système OU heure locale
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                enableDarkMode();
            } else if (isNightTime()) {
                // Auto-activation basée sur l'heure (18h-6h)
                enableDarkMode();
                console.log('🌙 Dark mode auto-activé (mode nuit 18h-6h)');
            } else {
                disableDarkMode();
            }
        }
    }

    /**
     * Écoute les changements de préférence système
     */
    function watchSystemPreference() {
        if (window.matchMedia) {
            const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');

            // Écoute les changements (pour les navigateurs modernes)
            if (darkModeQuery.addEventListener) {
                darkModeQuery.addEventListener('change', (e) => {
                    // Ne change que si l'utilisateur n'a pas de préférence sauvegardée
                    if (!localStorage.getItem(STORAGE_KEY)) {
                        if (e.matches) {
                            enableDarkMode();
                        } else {
                            disableDarkMode();
                        }
                    }
                });
            }
        }
    }

    /**
     * Vérifie toutes les heures si le mode doit changer (18h → dark, 6h → light)
     */
    function watchTimeOfDay() {
        // Vérifie toutes les 30 minutes
        setInterval(() => {
            const savedMode = localStorage.getItem(STORAGE_KEY);
            
            // Ne change automatiquement que si l'utilisateur n'a pas de préférence explicite
            if (!savedMode) {
                const shouldBeDark = isNightTime();
                const isDarkNow = body.classList.contains('dark-mode');

                if (shouldBeDark && !isDarkNow) {
                    enableDarkMode();
                    console.log('🌙 Auto-switch vers dark mode (18h)');
                } else if (!shouldBeDark && isDarkNow) {
                    disableDarkMode();
                    console.log('☀️ Auto-switch vers light mode (6h)');
                }
            }
        }, 30 * 60 * 1000); // 30 minutes
    }

    // Initialisation au chargement du DOM
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initDarkMode();
            watchSystemPreference();
            watchTimeOfDay(); // Nouveau: surveillance heure locale
        });
    } else {
        // DOM déjà chargé
        initDarkMode();
        watchSystemPreference();
        watchTimeOfDay(); // Nouveau: surveillance heure locale
    }

    // Événement de clic sur le bouton toggle
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleDarkMode);
    }

    /**
     * Ajoute une animation de transition fluide
     */
    function addTransitionClass() {
        body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    }

    addTransitionClass();

    /**
     * Raccourci clavier optionnel (Ctrl/Cmd + D)
     */
    document.addEventListener('keydown', (e) => {
        // Ctrl+D (Windows/Linux) ou Cmd+D (Mac)
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            toggleDarkMode();
        }
    });

    // Animation de rotation sur le bouton au survol
    if (toggleButton) {
        toggleButton.addEventListener('mouseenter', () => {
            toggleIcon.style.transition = 'transform 0.3s ease';
            toggleIcon.style.transform = 'rotate(180deg)';
        });

        toggleButton.addEventListener('mouseleave', () => {
            toggleIcon.style.transform = 'rotate(0deg)';
        });
    }

    /**
     * Console log pour debug (peut être retiré en production)
     */
    console.log('🌙 NyangaBudget Dark Mode initialized');
    console.log('💡 Tip: Press Ctrl+D to toggle dark mode quickly!');

})();
