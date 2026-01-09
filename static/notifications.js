/* ==================== SYSTÈME DE NOTIFICATIONS TOAST ==================== */

class ToastNotificationSystem {
    constructor() {
        this.container = null;
        this.notifications = [];
        this.init();
    }

    init() {
        // Créer le conteneur de notifications
        this.createContainer();
        
        // Demander permission pour notifications navigateur
        this.requestNotificationPermission();
        
        // Vérifier les nouveaux rappels toutes les minutes
        setInterval(() => this.checkReminders(), 60000);
    }

    createContainer() {
        if (!document.getElementById('toast-container')) {
            const container = document.createElement('div');
            container.id = 'toast-container';
            container.className = 'toast-container position-fixed top-0 end-0 p-3';
            container.style.zIndex = '9999';
            document.body.appendChild(container);
            this.container = container;
        } else {
            this.container = document.getElementById('toast-container');
        }
    }

    show(message, type = 'info', duration = 5000) {
        const toast = this.createToast(message, type, duration);
        this.container.appendChild(toast);
        
        // Animation d'entrée
        setTimeout(() => {
            toast.classList.add('show');
        }, 10);
        
        // Auto-fermeture
        if (duration > 0) {
            setTimeout(() => {
                this.hide(toast);
            }, duration);
        }
        
        return toast;
    }

    createToast(message, type, duration) {
        const id = `toast-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
        
        const icons = {
            success: 'bi-check-circle-fill',
            error: 'bi-x-circle-fill',
            warning: 'bi-exclamation-triangle-fill',
            info: 'bi-info-circle-fill'
        };
        
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };
        
        const toast = document.createElement('div');
        toast.id = id;
        toast.className = `toast align-items-center border-0 fade modern-toast toast-${type}`;
        toast.setAttribute('role', 'alert');
        toast.setAttribute('aria-live', 'assertive');
        toast.setAttribute('aria-atomic', 'true');
        toast.style.setProperty('--toast-color', colors[type] || colors.info);
        
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body d-flex align-items-center">
                    <i class="bi ${icons[type] || icons.info} me-2" style="font-size: 1.5rem; color: var(--toast-color);"></i>
                    <span>${message}</span>
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" onclick="window.toastSystem.hide(document.getElementById('${id}'))"></button>
            </div>
        `;
        
        // Ajouter barre de progression si durée définie
        if (duration > 0) {
            const progressBar = document.createElement('div');
            progressBar.className = 'toast-progress';
            progressBar.style.animation = `toastProgress ${duration}ms linear`;
            toast.appendChild(progressBar);
        }
        
        return toast;
    }

    hide(toast) {
        toast.classList.remove('show');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    success(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    error(message, duration = 7000) {
        return this.show(message, 'error', duration);
    }

    warning(message, duration = 6000) {
        return this.show(message, 'warning', duration);
    }

    info(message, duration = 5000) {
        return this.show(message, 'info', duration);
    }

    async requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            try {
                const permission = await Notification.requestPermission();
                if (permission === 'granted') {
                    this.success('Notifications activées !');
                }
            } catch (error) {
                console.error('Erreur permission notifications:', error);
            }
        }
    }

    sendBrowserNotification(title, options = {}) {
        if ('Notification' in window && Notification.permission === 'granted') {
            const notification = new Notification(title, {
                icon: '/static/images/logo.png',
                badge: '/static/images/logo.png',
                ...options
            });
            
            notification.onclick = () => {
                window.focus();
                notification.close();
            };
            
            return notification;
        }
    }

    async checkReminders() {
        try {
            const response = await fetch('/api/check-reminders', {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });
            
            if (!response.ok) return;
            
            const data = await response.json();
            
            if (data.reminders && data.reminders.length > 0) {
                data.reminders.forEach(reminder => {
                    this.warning(`⏰ Rappel: ${reminder.titre}`, 0);
                    this.sendBrowserNotification('Rappel NyangaBudget', {
                        body: reminder.titre,
                        tag: `reminder-${reminder.id}`
                    });
                });
            }
        } catch (error) {
            console.error('Erreur vérification rappels:', error);
        }
    }
}

// Styles CSS pour les toasts modernes
const toastStyles = `
.modern-toast {
    min-width: 300px;
    max-width: 400px;
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(10px);
    border-radius: 12px !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    overflow: hidden;
    position: relative;
}

.modern-toast .toast-body {
    padding: 15px;
    font-weight: 500;
}

.toast-progress {
    position: absolute;
    bottom: 0;
    left: 0;
    height: 4px;
    width: 100%;
    background: var(--toast-color);
    opacity: 0.7;
}

@keyframes toastProgress {
    from { width: 100%; }
    to { width: 0%; }
}

.toast-success {
    border-left: 4px solid #10b981;
}

.toast-error {
    border-left: 4px solid #ef4444;
}

.toast-warning {
    border-left: 4px solid #f59e0b;
}

.toast-info {
    border-left: 4px solid #3b82f6;
}

body.dark-mode .modern-toast {
    background: rgba(42, 42, 42, 0.95) !important;
    color: #e0e0e0;
}

/* Animation slide in from right */
.toast.show {
    animation: slideInRight 0.3s ease-out;
}

@keyframes slideInRight {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
`;

// Injecter les styles
if (!document.getElementById('toast-notification-styles')) {
    const styleElement = document.createElement('style');
    styleElement.id = 'toast-notification-styles';
    styleElement.textContent = toastStyles;
    document.head.appendChild(styleElement);
}

// Initialiser le système de notifications
document.addEventListener('DOMContentLoaded', () => {
    window.toastSystem = new ToastNotificationSystem();
    
    // Convertir les flash messages Flask en toasts
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(alert => {
        const type = alert.classList.contains('alert-success') ? 'success' :
                     alert.classList.contains('alert-danger') ? 'error' :
                     alert.classList.contains('alert-warning') ? 'warning' : 'info';
        
        const message = alert.textContent.trim();
        if (message) {
            window.toastSystem.show(message, type);
        }
        
        // Masquer l'alert d'origine
        alert.style.display = 'none';
    });
});

// API publique pour utilisation dans les templates
window.notify = {
    success: (msg) => window.toastSystem.success(msg),
    error: (msg) => window.toastSystem.error(msg),
    warning: (msg) => window.toastSystem.warning(msg),
    info: (msg) => window.toastSystem.info(msg)
};
