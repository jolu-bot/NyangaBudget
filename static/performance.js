/* ==================== OPTIMISATIONS PERFORMANCE ==================== */

class PerformanceOptimizer {
    constructor() {
        this.lazyLoadObserver = null;
        this.init();
    }

    init() {
        // Lazy loading des images
        this.initLazyLoading();
        
        // Pagination dynamique
        this.initInfiniteScroll();
        
        // Préchargement intelligent
        this.preloadCriticalResources();
        
        // Monitoring des performances
        this.monitorPerformance();
    }

    // ==================== LAZY LOADING ====================
    initLazyLoading() {
        // Support navigateur pour IntersectionObserver
        if ('IntersectionObserver' in window) {
            this.lazyLoadObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadImage(entry.target);
                        observer.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            // Observer toutes les images lazy
            this.observeLazyImages();
        } else {
            // Fallback pour anciens navigateurs
            this.loadAllImages();
        }
    }

    observeLazyImages() {
        const lazyImages = document.querySelectorAll('img[data-src], img[loading="lazy"]');
        lazyImages.forEach(img => {
            if (img.dataset.src) {
                this.lazyLoadObserver.observe(img);
            }
        });
    }

    loadImage(img) {
        const src = img.dataset.src || img.src;
        const srcset = img.dataset.srcset;
        
        if (src) {
            // Créer une nouvelle image pour précharger
            const tempImg = new Image();
            tempImg.onload = () => {
                img.src = src;
                if (srcset) {
                    img.srcset = srcset;
                }
                img.classList.add('loaded');
                img.removeAttribute('data-src');
            };
            tempImg.onerror = () => {
                img.src = '/static/images/placeholder.png';
                img.classList.add('error');
            };
            tempImg.src = src;
            
            // Placeholder pendant le chargement
            if (!img.src || img.src.includes('placeholder')) {
                img.style.backgroundColor = '#f0f0f0';
            }
        }
    }

    loadAllImages() {
        const lazyImages = document.querySelectorAll('img[data-src]');
        lazyImages.forEach(img => this.loadImage(img));
    }

    // ==================== INFINITE SCROLL / PAGINATION ====================
    initInfiniteScroll() {
        const paginatedContainers = document.querySelectorAll('[data-pagination]');
        
        paginatedContainers.forEach(container => {
            const config = JSON.parse(container.dataset.pagination || '{}');
            this.setupInfiniteScroll(container, config);
        });
    }

    setupInfiniteScroll(container, config) {
        const {
            endpoint = '/api/load-more',
            itemsPerPage = 20,
            scrollThreshold = 200
        } = config;

        let page = 1;
        let loading = false;
        let hasMore = true;

        const loadMore = async () => {
            if (loading || !hasMore) return;

            loading = true;
            this.showLoadingSpinner(container);

            try {
                const response = await fetch(`${endpoint}?page=${page}&limit=${itemsPerPage}`);
                const data = await response.json();

                if (data.items && data.items.length > 0) {
                    this.appendItems(container, data.items);
                    page++;
                    hasMore = data.hasMore !== false;
                } else {
                    hasMore = false;
                    this.showEndMessage(container);
                }
            } catch (error) {
                console.error('Erreur chargement:', error);
                this.showErrorMessage(container);
            } finally {
                loading = false;
                this.hideLoadingSpinner(container);
            }
        };

        // Scroll event avec throttle
        let scrollTimeout;
        window.addEventListener('scroll', () => {
            clearTimeout(scrollTimeout);
            scrollTimeout = setTimeout(() => {
                const scrollPosition = window.innerHeight + window.scrollY;
                const threshold = document.documentElement.scrollHeight - scrollThreshold;

                if (scrollPosition >= threshold) {
                    loadMore();
                }
            }, 100);
        });
    }

    appendItems(container, items) {
        const fragment = document.createDocumentFragment();
        
        items.forEach(item => {
            const element = this.createItemElement(item);
            fragment.appendChild(element);
        });
        
        container.appendChild(fragment);
        
        // Observer les nouvelles images lazy
        this.observeLazyImages();
    }

    createItemElement(item) {
        const div = document.createElement('div');
        div.className = 'list-item fade-in';
        div.innerHTML = item.html || '';
        return div;
    }

    showLoadingSpinner(container) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner text-center p-3';
        spinner.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Chargement...</span>
            </div>
        `;
        spinner.id = 'pagination-spinner';
        container.appendChild(spinner);
    }

    hideLoadingSpinner(container) {
        const spinner = container.querySelector('#pagination-spinner');
        if (spinner) spinner.remove();
    }

    showEndMessage(container) {
        const msg = document.createElement('div');
        msg.className = 'text-center text-muted p-3';
        msg.innerHTML = '<i class="bi bi-check-circle"></i> Tous les éléments chargés';
        container.appendChild(msg);
    }

    showErrorMessage(container) {
        const msg = document.createElement('div');
        msg.className = 'alert alert-warning text-center';
        msg.innerHTML = '<i class="bi bi-exclamation-triangle"></i> Erreur de chargement';
        container.appendChild(msg);
    }

    // ==================== PRÉCHARGEMENT ====================
    preloadCriticalResources() {
        // Précharger les ressources critiques
        const criticalResources = [
            '/static/images/logo.png',
            '/static/style.css',
            '/static/modern-ui.css'
        ];

        criticalResources.forEach(url => {
            const link = document.createElement('link');
            link.rel = 'preload';
            link.as = this.getResourceType(url);
            link.href = url;
            document.head.appendChild(link);
        });
    }

    getResourceType(url) {
        if (url.endsWith('.css')) return 'style';
        if (url.endsWith('.js')) return 'script';
        if (/\.(jpg|jpeg|png|gif|webp)$/.test(url)) return 'image';
        return 'fetch';
    }

    // ==================== COMPRESSION IMAGES ====================
    async compressImage(file, maxWidth = 1920, quality = 0.8) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            
            reader.onload = (e) => {
                const img = new Image();
                
                img.onload = () => {
                    const canvas = document.createElement('canvas');
                    let width = img.width;
                    let height = img.height;

                    // Redimensionner si nécessaire
                    if (width > maxWidth) {
                        height = (height * maxWidth) / width;
                        width = maxWidth;
                    }

                    canvas.width = width;
                    canvas.height = height;

                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(img, 0, 0, width, height);

                    canvas.toBlob(
                        (blob) => {
                            const compressedFile = new File([blob], file.name, {
                                type: 'image/jpeg',
                                lastModified: Date.now()
                            });
                            
                            console.log(`Image compressée: ${(file.size / 1024).toFixed(0)}KB → ${(compressedFile.size / 1024).toFixed(0)}KB`);
                            resolve(compressedFile);
                        },
                        'image/jpeg',
                        quality
                    );
                };

                img.onerror = reject;
                img.src = e.target.result;
            };

            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    // Ajouter compression automatique aux inputs file
    setupImageCompression() {
        const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
        
        imageInputs.forEach(input => {
            input.addEventListener('change', async (e) => {
                const files = Array.from(e.target.files);
                const compressedFiles = [];

                for (const file of files) {
                    if (file.size > 500 * 1024) { // > 500KB
                        try {
                            const compressed = await this.compressImage(file);
                            compressedFiles.push(compressed);
                        } catch (error) {
                            console.error('Erreur compression:', error);
                            compressedFiles.push(file);
                        }
                    } else {
                        compressedFiles.push(file);
                    }
                }

                // Remplacer les fichiers
                const dataTransfer = new DataTransfer();
                compressedFiles.forEach(file => dataTransfer.items.add(file));
                input.files = dataTransfer.files;
            });
        });
    }

    // ==================== CACHE LOCAL ====================
    initLocalCache() {
        // Cache des données avec localStorage/IndexedDB
        if ('caches' in window) {
            this.setupServiceWorkerCache();
        }
    }

    async setupServiceWorkerCache() {
        try {
            const cache = await caches.open('nyanga-cache-v1');
            
            // Mettre en cache les ressources statiques
            const resourcesToCache = [
                '/',
                '/static/style.css',
                '/static/modern-ui.css',
                '/static/charts.js',
                '/static/search.js',
                '/static/notifications.js',
                '/static/performance.js'
            ];

            await cache.addAll(resourcesToCache);
            console.log('✅ Ressources mises en cache');
        } catch (error) {
            console.error('Erreur cache:', error);
        }
    }

    // ==================== MONITORING ====================
    monitorPerformance() {
        if ('PerformanceObserver' in window) {
            // Observer les métriques Web Vitals
            this.observeLCP();
            this.observeFID();
            this.observeCLS();
        }

        // Mesures navigation
        window.addEventListener('load', () => {
            setTimeout(() => {
                const perfData = performance.getEntriesByType('navigation')[0];
                if (perfData) {
                    console.log('📊 Performance:', {
                        'DOM Chargé': `${perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart}ms`,
                        'Chargement Total': `${perfData.loadEventEnd - perfData.loadEventStart}ms`,
                        'TTFB': `${perfData.responseStart - perfData.requestStart}ms`
                    });
                }
            }, 0);
        });
    }

    observeLCP() {
        const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries();
            const lastEntry = entries[entries.length - 1];
            console.log('📊 LCP (Largest Contentful Paint):', `${lastEntry.renderTime || lastEntry.loadTime}ms`);
        });
        observer.observe({ entryTypes: ['largest-contentful-paint'] });
    }

    observeFID() {
        const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries();
            entries.forEach(entry => {
                console.log('📊 FID (First Input Delay):', `${entry.processingStart - entry.startTime}ms`);
            });
        });
        observer.observe({ entryTypes: ['first-input'] });
    }

    observeCLS() {
        let clsScore = 0;
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (!entry.hadRecentInput) {
                    clsScore += entry.value;
                    console.log('📊 CLS (Cumulative Layout Shift):', clsScore.toFixed(4));
                }
            }
        });
        observer.observe({ entryTypes: ['layout-shift'] });
    }

    // ==================== DEBOUNCE/THROTTLE UTILS ====================
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
}

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', () => {
    window.perfOptimizer = new PerformanceOptimizer();
    
    // Exposer les utilitaires
    window.compressImage = (file) => window.perfOptimizer.compressImage(file);
});

// Export pour utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = PerformanceOptimizer;
}
