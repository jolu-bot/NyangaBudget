/* ==================== IMPORT CSV/EXCEL ==================== */

class ImportModule {
    constructor() {
        this.file = null;
        this.data = [];
        this.headers = [];
        this.mapping = {};
        this.init();
    }

    init() {
        // Bouton d'import dans la navbar ou dashboard
        this.createImportButton();
    }

    createImportButton() {
        // Chercher où ajouter le bouton (dashboard ou navbar)
        const container = document.querySelector('.dashboard-actions') || document.querySelector('.navbar-nav');
        
        if (container && !document.getElementById('import-btn')) {
            const btn = document.createElement('button');
            btn.id = 'import-btn';
            btn.className = 'btn btn-outline-success btn-sm';
            btn.innerHTML = '<i class="bi bi-upload"></i> Importer';
            btn.onclick = () => this.showImportModal();
            
            container.appendChild(btn);
        }
    }

    showImportModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'import-modal';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content glass-card">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="bi bi-upload"></i> Importer des données
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <!-- Étape 1: Sélection fichier -->
                        <div id="step-1" class="import-step">
                            <h6>1. Sélectionner un fichier</h6>
                            <div class="mb-3">
                                <label class="form-label">Type d'import</label>
                                <select id="import-type" class="form-select">
                                    <option value="depenses">Dépenses</option>
                                    <option value="revenus">Revenus</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="file-input" class="form-label">Fichier CSV ou Excel</label>
                                <input type="file" 
                                       id="file-input" 
                                       class="form-control" 
                                       accept=".csv,.xlsx,.xls">
                                <small class="text-muted">Formats supportés: CSV, Excel (.xlsx, .xls)</small>
                            </div>
                            <button class="btn btn-primary" id="parse-btn" disabled>
                                Analyser le fichier <i class="bi bi-arrow-right"></i>
                            </button>
                        </div>

                        <!-- Étape 2: Mapping colonnes -->
                        <div id="step-2" class="import-step" style="display: none;">
                            <h6>2. Mapper les colonnes</h6>
                            <p class="text-muted">Associez les colonnes de votre fichier aux champs requis</p>
                            <div id="mapping-container"></div>
                            <button class="btn btn-secondary me-2" onclick="window.importModule.goToStep(1)">
                                <i class="bi bi-arrow-left"></i> Retour
                            </button>
                            <button class="btn btn-primary" id="validate-btn">
                                Valider les données <i class="bi bi-arrow-right"></i>
                            </button>
                        </div>

                        <!-- Étape 3: Validation et preview -->
                        <div id="step-3" class="import-step" style="display: none;">
                            <h6>3. Validation et aperçu</h6>
                            <div id="validation-summary"></div>
                            <div id="preview-table" class="table-responsive mt-3"></div>
                            <button class="btn btn-secondary me-2" onclick="window.importModule.goToStep(2)">
                                <i class="bi bi-arrow-left"></i> Retour
                            </button>
                            <button class="btn btn-success" id="import-confirm-btn">
                                <i class="bi bi-check-circle"></i> Confirmer l'import
                            </button>
                        </div>

                        <!-- Étape 4: Import en cours -->
                        <div id="step-4" class="import-step text-center" style="display: none;">
                            <div class="spinner-border text-primary mb-3" role="status">
                                <span class="visually-hidden">Import en cours...</span>
                            </div>
                            <p>Import en cours...</p>
                            <div class="progress">
                                <div id="import-progress" 
                                     class="progress-bar progress-bar-striped progress-bar-animated" 
                                     role="progressbar" 
                                     style="width: 0%"></div>
                            </div>
                        </div>

                        <!-- Étape 5: Résultat -->
                        <div id="step-5" class="import-step" style="display: none;">
                            <div id="import-result"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
        
        // Cleanup au close
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
        
        // Event listeners
        this.setupEventListeners();
    }

    setupEventListeners() {
        const fileInput = document.getElementById('file-input');
        const parseBtn = document.getElementById('parse-btn');
        const validateBtn = document.getElementById('validate-btn');
        const importConfirmBtn = document.getElementById('import-confirm-btn');
        
        fileInput.addEventListener('change', (e) => {
            this.file = e.target.files[0];
            parseBtn.disabled = !this.file;
        });
        
        parseBtn.addEventListener('click', () => this.parseFile());
        validateBtn.addEventListener('click', () => this.validateData());
        importConfirmBtn.addEventListener('click', () => this.confirmImport());
    }

    async parseFile() {
        if (!this.file) return;
        
        const fileType = this.file.name.split('.').pop().toLowerCase();
        
        try {
            if (fileType === 'csv') {
                await this.parseCSV();
            } else if (['xlsx', 'xls'].includes(fileType)) {
                await this.parseExcel();
            }
            
            this.goToStep(2);
            this.renderMapping();
            
        } catch (error) {
            console.error('Erreur parsing:', error);
            window.notify.error('Erreur lors de la lecture du fichier');
        }
    }

    async parseCSV() {
        const text = await this.file.text();
        const lines = text.split('\n').filter(l => l.trim());
        
        this.headers = lines[0].split(',').map(h => h.trim());
        this.data = lines.slice(1).map(line => {
            const values = line.split(',');
            const row = {};
            this.headers.forEach((header, i) => {
                row[header] = values[i]?.trim() || '';
            });
            return row;
        });
    }

    async parseExcel() {
        // Pour Excel, utiliser une bibliothèque comme SheetJS
        window.notify.warning('Import Excel: Utilisez la librairie SheetJS côté client ou envoyez à l\'API');
        // Alternative: envoyer le fichier à l'API Python qui utilisera pandas
        const formData = new FormData();
        formData.append('file', this.file);
        
        const response = await fetch('/api/parse-excel', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        this.headers = result.headers;
        this.data = result.data;
    }

    renderMapping() {
        const importType = document.getElementById('import-type').value;
        const requiredFields = importType === 'depenses' 
            ? ['nom', 'montant', 'date', 'categorie']
            : ['source', 'montant', 'date'];
        
        const container = document.getElementById('mapping-container');
        container.innerHTML = '';
        
        requiredFields.forEach(field => {
            const div = document.createElement('div');
            div.className = 'mb-3';
            div.innerHTML = `
                <label class="form-label">
                    ${field.charAt(0).toUpperCase() + field.slice(1)} 
                    <span class="text-danger">*</span>
                </label>
                <select class="form-select mapping-select" data-field="${field}">
                    <option value="">-- Sélectionner --</option>
                    ${this.headers.map((h, i) => `
                        <option value="${i}" ${this.autoMap(field, h) ? 'selected' : ''}>
                            ${h}
                        </option>
                    `).join('')}
                </select>
            `;
            container.appendChild(div);
        });
        
        // Sauvegarder le mapping
        document.querySelectorAll('.mapping-select').forEach(select => {
            select.addEventListener('change', (e) => {
                const field = e.target.dataset.field;
                const headerIndex = parseInt(e.target.value);
                this.mapping[field] = this.headers[headerIndex];
            });
        });
    }

    autoMap(field, header) {
        // Auto-mapping intelligent
        const mappings = {
            'nom': ['nom', 'name', 'libelle', 'libellé', 'description'],
            'montant': ['montant', 'amount', 'prix', 'price', 'valeur'],
            'date': ['date', 'jour', 'timestamp'],
            'categorie': ['categorie', 'catégorie', 'category', 'type'],
            'source': ['source', 'origine', 'provenance']
        };
        
        const normalizedHeader = header.toLowerCase();
        return mappings[field]?.some(m => normalizedHeader.includes(m));
    }

    validateData() {
        // TODO: Implémenter validation
        const validRows = this.data.filter(row => {
            // Vérifier que tous les champs requis sont présents
            return Object.values(this.mapping).every(header => row[header]);
        });
        
        if (validRows.length === 0) {
            window.notify.error('Aucune donnée valide trouvée');
            return;
        }
        
        this.goToStep(3);
        this.renderPreview(validRows);
    }

    renderPreview(rows) {
        const container = document.getElementById('preview-table');
        const summary = document.getElementById('validation-summary');
        
        summary.innerHTML = `
            <div class="alert alert-info">
                <i class="bi bi-info-circle"></i>
                ${rows.length} ligne(s) valide(s) sur ${this.data.length}
            </div>
        `;
        
        let html = '<table class="table table-sm table-striped"><thead><tr>';
        Object.keys(this.mapping).forEach(field => {
            html += `<th>${field}</th>`;
        });
        html += '</tr></thead><tbody>';
        
        rows.slice(0, 10).forEach(row => {
            html += '<tr>';
            Object.values(this.mapping).forEach(header => {
                html += `<td>${row[header]}</td>`;
            });
            html += '</tr>';
        });
        
        html += '</tbody></table>';
        if (rows.length > 10) {
            html += `<small class="text-muted">... et ${rows.length - 10} autres lignes</small>`;
        }
        
        container.innerHTML = html;
    }

    async confirmImport() {
        this.goToStep(4);
        
        const importType = document.getElementById('import-type').value;
        const mappedData = this.data.map(row => {
            const mapped = {};
            Object.entries(this.mapping).forEach(([field, header]) => {
                mapped[field] = row[header];
            });
            return mapped;
        });
        
        try {
            const response = await fetch('/api/import', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: importType,
                    data: mappedData
                })
            });
            
            const result = await response.json();
            
            this.goToStep(5);
            this.showResult(result);
            
        } catch (error) {
            console.error('Erreur import:', error);
            this.goToStep(5);
            this.showResult({ success: false, error: error.message });
        }
    }

    showResult(result) {
        const container = document.getElementById('import-result');
        
        if (result.success) {
            container.innerHTML = `
                <div class="alert alert-success">
                    <h5><i class="bi bi-check-circle"></i> Import réussi !</h5>
                    <p>${result.imported} élément(s) importé(s)</p>
                    ${result.errors ? `<p class="text-warning">${result.errors} erreur(s)</p>` : ''}
                </div>
                <button class="btn btn-primary" onclick="location.reload()">
                    Actualiser la page
                </button>
            `;
        } else {
            container.innerHTML = `
                <div class="alert alert-danger">
                    <h5><i class="bi bi-x-circle"></i> Erreur d'import</h5>
                    <p>${result.error || 'Une erreur est survenue'}</p>
                </div>
                <button class="btn btn-secondary" onclick="window.importModule.goToStep(1)">
                    Réessayer
                </button>
            `;
        }
    }

    goToStep(step) {
        document.querySelectorAll('.import-step').forEach((el, i) => {
            el.style.display = (i + 1) === step ? 'block' : 'none';
        });
    }
}

// Initialiser
document.addEventListener('DOMContentLoaded', () => {
    window.importModule = new ImportModule();
});
