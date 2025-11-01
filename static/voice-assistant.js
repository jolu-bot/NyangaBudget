/**
 * NyangaBudget - Assistant Vocal Simplifié
 * Utilise Web Speech API (intégrée aux navigateurs modernes)
 */

(function() {
    'use strict';

    // Vérifier support Web Speech API
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.warn('⚠️ Web Speech API non supportée par ce navigateur');
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = 'fr-FR';
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    let isListening = false;

    /**
     * Initialise l'assistant vocal sur tous les formulaires
     */
    function initVoiceAssistant() {
        // Ajouter bouton micro sur formulaire de dépenses
        const depenseForm = document.querySelector('form[action*="add/depense"]') || 
                           document.querySelector('form[method="POST"]');
        
        if (depenseForm && !depenseForm.querySelector('.voice-btn')) {
            addVoiceButton(depenseForm);
        }

        // Ajouter bouton sur formulaire de revenus
        const revenuForm = document.querySelector('form[action*="add/revenu"]');
        if (revenuForm && !revenuForm.querySelector('.voice-btn')) {
            addVoiceButton(revenuForm, 'revenu');
        }
    }

    /**
     * Ajoute un bouton micro à un formulaire
     */
    function addVoiceButton(form, type = 'depense') {
        const voiceBtn = document.createElement('button');
        voiceBtn.type = 'button';
        voiceBtn.className = 'btn btn-outline-primary voice-btn ms-2';
        voiceBtn.innerHTML = '<i class="bi bi-mic-fill"></i>';
        voiceBtn.title = 'Commande vocale (ex: "Ajoute 5000 francs en alimentation")';
        
        // Trouver où insérer le bouton (à côté du bouton submit)
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn && submitBtn.parentElement) {
            submitBtn.parentElement.appendChild(voiceBtn);
        }

        // Event listener
        voiceBtn.addEventListener('click', () => startListening(form, type, voiceBtn));
    }

    /**
     * Démarre l'écoute vocale
     */
    function startListening(form, type, button) {
        if (isListening) {
            recognition.stop();
            return;
        }

        isListening = true;
        button.classList.add('btn-danger');
        button.classList.remove('btn-outline-primary');
        button.innerHTML = '<i class="bi bi-mic-fill"></i> <span class="spinner-border spinner-border-sm"></span>';
        
        // Afficher indication
        showVoiceIndicator('🎤 Parlez maintenant...');

        recognition.start();
    }

    /**
     * Gestion de la reconnaissance vocale
     */
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript.toLowerCase();
        console.log('🎤 Commande vocale:', transcript);
        
        // Parser la commande
        const command = parseVoiceCommand(transcript);
        
        if (command) {
            applyCommand(command);
            showVoiceIndicator(`✅ Compris: ${command.description}`, 'success');
        } else {
            showVoiceIndicator('❌ Commande non reconnue. Essayez: "Ajoute 5000 en alimentation"', 'danger');
        }
    };

    recognition.onerror = (event) => {
        console.error('Erreur reconnaissance vocale:', event.error);
        showVoiceIndicator('❌ Erreur: ' + event.error, 'danger');
        resetButton();
    };

    recognition.onend = () => {
        isListening = false;
        resetButton();
    };

    /**
     * Parse une commande vocale en données structurées
     * Formats supportés:
     * - "Ajoute 5000 en alimentation"
     * - "Ajoute dépense de 3000 francs"
     * - "Revenu de 50000"
     */
    function parseVoiceCommand(text) {
        // Nettoyer le texte
        text = text.toLowerCase()
            .replace(/euros?/gi, '')
            .replace(/francs?/gi, '')
            .replace(/fcfa/gi, '')
            .replace(/cfa/gi, '')
            .trim();

        // Pattern 1: "ajoute [montant] en [catégorie]"
        let match = text.match(/ajoute?\s+(\d+)\s+(?:en|pour|dans)?\s+(.+)/i);
        if (match) {
            return {
                type: 'depense',
                montant: match[1],
                categorie: match[2].trim(),
                description: `Dépense ${match[1]} FCFA - ${match[2]}`
            };
        }

        // Pattern 2: "ajoute dépense de [montant]"
        match = text.match(/ajoute?\s+d[ée]pense\s+de\s+(\d+)/i);
        if (match) {
            return {
                type: 'depense',
                montant: match[1],
                description: `Dépense ${match[1]} FCFA`
            };
        }

        // Pattern 3: "revenu de [montant]"
        match = text.match(/revenu\s+de\s+(\d+)/i);
        if (match) {
            return {
                type: 'revenu',
                montant: match[1],
                description: `Revenu ${match[1]} FCFA`
            };
        }

        // Pattern 4: Simple "[montant] [catégorie]"
        match = text.match(/(\d+)\s+(.+)/);
        if (match) {
            return {
                type: 'depense',
                montant: match[1],
                categorie: match[2].trim(),
                description: `Dépense ${match[1]} FCFA - ${match[2]}`
            };
        }

        return null;
    }

    /**
     * Applique la commande vocale au formulaire
     */
    function applyCommand(command) {
        if (command.type === 'depense') {
            // Remplir formulaire dépense
            const montantInput = document.querySelector('input[name="montant"]');
            const nomInput = document.querySelector('input[name="nom"]');
            const categorieSelect = document.querySelector('select[name="categorie_id"]');

            if (montantInput) {
                montantInput.value = command.montant;
                montantInput.classList.add('is-valid');
            }

            if (nomInput && command.categorie) {
                nomInput.value = `Commande vocale: ${command.categorie}`;
                nomInput.classList.add('is-valid');
            }

            // Essayer de sélectionner la catégorie correspondante
            if (categorieSelect && command.categorie) {
                const options = Array.from(categorieSelect.options);
                const matchingOption = options.find(opt => 
                    opt.text.toLowerCase().includes(command.categorie.toLowerCase())
                );
                if (matchingOption) {
                    categorieSelect.value = matchingOption.value;
                    categorieSelect.classList.add('is-valid');
                }
            }
        } else if (command.type === 'revenu') {
            // Remplir formulaire revenu
            const montantInput = document.querySelector('input[name="montant"]');
            const sourceInput = document.querySelector('input[name="source"]');

            if (montantInput) {
                montantInput.value = command.montant;
                montantInput.classList.add('is-valid');
            }

            if (sourceInput) {
                sourceInput.value = 'Commande vocale';
                sourceInput.classList.add('is-valid');
            }
        }

        // Animation de succès
        const form = document.querySelector('form');
        if (form) {
            form.classList.add('border', 'border-success');
            setTimeout(() => {
                form.classList.remove('border', 'border-success');
            }, 2000);
        }
    }

    /**
     * Affiche un indicateur visuel
     */
    function showVoiceIndicator(message, type = 'info') {
        // Supprimer ancien indicateur
        const oldIndicator = document.getElementById('voice-indicator');
        if (oldIndicator) {
            oldIndicator.remove();
        }

        const indicator = document.createElement('div');
        indicator.id = 'voice-indicator';
        indicator.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        indicator.style.cssText = 'top: 80px; right: 20px; z-index: 9999; min-width: 300px;';
        indicator.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(indicator);

        // Auto-fermeture après 5 secondes
        setTimeout(() => {
            if (indicator.parentElement) {
                indicator.remove();
            }
        }, 5000);
    }

    /**
     * Réinitialise le bouton micro
     */
    function resetButton() {
        const voiceBtns = document.querySelectorAll('.voice-btn');
        voiceBtns.forEach(btn => {
            btn.classList.remove('btn-danger');
            btn.classList.add('btn-outline-primary');
            btn.innerHTML = '<i class="bi bi-mic-fill"></i>';
        });
    }

    /**
     * Ajoute un tutoriel d'aide
     */
    function addVoiceTutorial() {
        // Vérifier si on est sur la page d'accueil
        if (window.location.pathname === '/' || window.location.pathname.includes('index')) {
            const container = document.querySelector('.container');
            if (container && !document.getElementById('voice-tutorial')) {
                const tutorial = document.createElement('div');
                tutorial.id = 'voice-tutorial';
                tutorial.className = 'alert alert-info alert-dismissible fade show mt-3';
                tutorial.innerHTML = `
                    <strong><i class="bi bi-mic me-2"></i>Assistant Vocal Activé!</strong>
                    <p class="mb-0 mt-2">Exemples de commandes:</p>
                    <ul class="mb-0 mt-1">
                        <li>"Ajoute 5000 en alimentation"</li>
                        <li>"Ajoute dépense de 3000 francs"</li>
                        <li>"10000 transport"</li>
                    </ul>
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                `;
                container.insertBefore(tutorial, container.firstChild);
            }
        }
    }

    // Initialisation au chargement
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            initVoiceAssistant();
            addVoiceTutorial();
        });
    } else {
        initVoiceAssistant();
        addVoiceTutorial();
    }

    // Réinitialiser après navigation AJAX (si applicable)
    if (window.addEventListener) {
        window.addEventListener('popstate', initVoiceAssistant);
    }

    console.log('🎤 Assistant Vocal NyangaBudget initialisé');

})();
