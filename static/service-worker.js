/**
 * NyangaBudget 2.0 - Service Worker PWA
 * Permet le fonctionnement hors ligne avec cache intelligent
 */

const CACHE_VERSION = 'nyanga-v2.0.1';
const CACHE_NAME = `nyangabudget-${CACHE_VERSION}`;

// Fichiers à mettre en cache lors de l'installation
const STATIC_ASSETS = [
    '/',
    '/static/style.css',
    '/static/darkmode.js',
    '/static/manifest.json',
    '/static/images/logo.png',
    '/static/images/logo-white.png',
    // Bootstrap CDN (cache pour hors ligne)
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css'
];

// Routes API à mettre en cache (stratégie Network First)
const API_ROUTES = [
    '/api/stats',
    '/api/predictions'
];

// Routes dynamiques (pages HTML)
const DYNAMIC_ROUTES = [
    '/dashboard',
    '/login',
    '/register',
    '/'
];

/**
 * Installation du Service Worker
 */
self.addEventListener('install', (event) => {
    console.log('[ServiceWorker] Installation en cours...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[ServiceWorker] Cache ouvert');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('[ServiceWorker] Assets statiques mis en cache');
                return self.skipWaiting(); // Active immédiatement
            })
            .catch((error) => {
                console.error('[ServiceWorker] Erreur mise en cache:', error);
            })
    );
});

/**
 * Activation du Service Worker
 */
self.addEventListener('activate', (event) => {
    console.log('[ServiceWorker] Activation en cours...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => {
                        // Supprimer les anciens caches
                        if (cacheName !== CACHE_NAME) {
                            console.log('[ServiceWorker] Suppression ancien cache:', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('[ServiceWorker] Activé et prêt');
                return self.clients.claim(); // Prend le contrôle immédiatement
            })
    );
});

/**
 * Interception des requêtes (stratégies de cache)
 */
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Ignorer les requêtes non-GET
    if (request.method !== 'GET') {
        return;
    }

    // Ignorer les requêtes externes (sauf CDN)
    if (url.origin !== location.origin && !isCDNRequest(url)) {
        return;
    }

    // Stratégie 1: Cache First (assets statiques)
    if (isStaticAsset(url)) {
        event.respondWith(cacheFirst(request));
        return;
    }

    // Stratégie 2: Network First (API)
    if (isAPIRequest(url)) {
        event.respondWith(networkFirst(request));
        return;
    }

    // Stratégie 3: Network First with fallback (pages HTML)
    if (isDynamicPage(url)) {
        event.respondWith(networkFirstWithFallback(request));
        return;
    }

    // Par défaut: Network First
    event.respondWith(networkFirst(request));
});

/**
 * Stratégie Cache First: Vérifier cache d'abord, puis réseau
 */
async function cacheFirst(request) {
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
        console.log('[ServiceWorker] Cache hit:', request.url);
        return cachedResponse;
    }

    console.log('[ServiceWorker] Cache miss, fetch réseau:', request.url);
    try {
        const networkResponse = await fetch(request);
        
        // Mettre en cache la nouvelle réponse
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.error('[ServiceWorker] Fetch échoué:', error);
        return new Response('Hors ligne - Contenu non disponible', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: new Headers({
                'Content-Type': 'text/plain'
            })
        });
    }
}

/**
 * Stratégie Network First: Réseau d'abord, cache en fallback
 */
async function networkFirst(request) {
    try {
        const networkResponse = await fetch(request);
        
        // Mettre en cache la réponse si succès
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('[ServiceWorker] Réseau échoué, utilisation cache:', request.url);
        const cachedResponse = await caches.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        return new Response(JSON.stringify({
            error: 'Hors ligne',
            message: 'Impossible de récupérer les données'
        }), {
            status: 503,
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        });
    }
}

/**
 * Stratégie Network First avec fallback page hors ligne
 */
async function networkFirstWithFallback(request) {
    try {
        const networkResponse = await fetch(request);
        
        // Mettre en cache la page si succès
        if (networkResponse.ok) {
            const cache = await caches.open(CACHE_NAME);
            cache.put(request, networkResponse.clone());
        }
        
        return networkResponse;
    } catch (error) {
        console.log('[ServiceWorker] Affichage version cachée:', request.url);
        const cachedResponse = await caches.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Fallback: rediriger vers page d'accueil cachée
        const homeCached = await caches.match('/');
        if (homeCached) {
            return homeCached;
        }
        
        return new Response(`
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>NyangaBudget - Hors Ligne</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        text-align: center;
                    }
                    .offline-container {
                        max-width: 500px;
                        padding: 2rem;
                    }
                    h1 { font-size: 3rem; margin-bottom: 1rem; }
                    p { font-size: 1.2rem; }
                    .icon { font-size: 5rem; margin-bottom: 1rem; }
                </style>
            </head>
            <body>
                <div class="offline-container">
                    <div class="icon">📡</div>
                    <h1>Hors Ligne</h1>
                    <p>NyangaBudget nécessite une connexion Internet pour cette page.</p>
                    <p><small>Veuillez vérifier votre connexion et réessayer.</small></p>
                </div>
            </body>
            </html>
        `, {
            status: 503,
            headers: new Headers({
                'Content-Type': 'text/html'
            })
        });
    }
}

/**
 * Vérifie si la requête est un asset statique
 */
function isStaticAsset(url) {
    return url.pathname.startsWith('/static/') ||
           url.pathname.endsWith('.css') ||
           url.pathname.endsWith('.js') ||
           url.pathname.endsWith('.png') ||
           url.pathname.endsWith('.jpg') ||
           url.pathname.endsWith('.jpeg') ||
           url.pathname.endsWith('.svg') ||
           url.pathname.endsWith('.woff') ||
           url.pathname.endsWith('.woff2');
}

/**
 * Vérifie si la requête est une API
 */
function isAPIRequest(url) {
    return url.pathname.startsWith('/api/');
}

/**
 * Vérifie si la requête est une page dynamique
 */
function isDynamicPage(url) {
    return DYNAMIC_ROUTES.some(route => url.pathname === route);
}

/**
 * Vérifie si la requête provient d'un CDN autorisé
 */
function isCDNRequest(url) {
    return url.hostname.includes('cdn.jsdelivr.net') ||
           url.hostname.includes('cdnjs.cloudflare.com');
}

/**
 * Écoute les messages du client
 */
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.keys().then((cacheNames) => {
                return Promise.all(
                    cacheNames.map((cacheName) => caches.delete(cacheName))
                );
            }).then(() => {
                console.log('[ServiceWorker] Cache vidé');
            })
        );
    }
});

console.log('[ServiceWorker] Script chargé');
