// KrishiMitra Service Worker - Complete Offline Support
const CACHE_NAME = 'krishimitra-v3';
const OFFLINE_URL = '/offline/';

// Files to cache for offline use
const STATIC_CACHE_URLS = [
    '/',
    '/offline/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/js/idb.js',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap'
];

// Install event - cache static assets
self.addEventListener('install', event => {
    console.log('[SW] Installing...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[SW] Caching static assets');
                return cache.addAll(STATIC_CACHE_URLS);
            })
            .then(() => self.skipWaiting())
    );
});

// Activate event - clean old caches
self.addEventListener('activate', event => {
    console.log('[SW] Activating...');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('[SW] Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch event - intelligent caching strategy
self.addEventListener('fetch', event => {
    const url = new URL(event.request.url);
    
    // API requests - Network First, Cache Fallback
    if (url.pathname.includes('/api/') || 
        url.pathname.includes('/get-weather-api/') ||
        url.pathname.includes('/market/api/') ||
        url.pathname.includes('/ai-chat/')) {
        
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    // Cache fresh response
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then(cache => {
                        cache.put(event.request, responseClone);
                    });
                    return response;
                })
                .catch(() => {
                    // Offline - return cached response
                    return caches.match(event.request);
                })
        );
    }
    
    // HTML pages - Network First, Fallback to Offline Page
    else if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .catch(() => {
                    return caches.match(OFFLINE_URL);
                })
        );
    }
    
    // Static assets - Cache First, Network Fallback
    else {
        event.respondWith(
            caches.match(event.request)
                .then(response => {
                    return response || fetch(event.request);
                })
        );
    }
});

// Background sync for offline data
self.addEventListener('sync', event => {
    if (event.tag === 'sync-farmer-data') {
        console.log('[SW] Background sync triggered');
        event.waitUntil(syncFarmerData());
    }
});

async function syncFarmerData() {
    console.log('[SW] Syncing farmer data...');
    // Open IndexedDB
    const db = await openDB();
    const pendingData = await getPendingData(db);
    
    for (const data of pendingData) {
        try {
            const response = await fetch(data.url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data.payload)
            });
            
            if (response.ok) {
                await deletePendingData(db, data.id);
                console.log('[SW] Synced:', data.url);
            }
        } catch (error) {
            console.log('[SW] Sync failed:', data.url);
        }
    }
}

// IndexedDB helper functions for service worker
function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('KrishiMitraDB', 1);
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('pending_sync')) {
                db.createObjectStore('pending_sync', { keyPath: 'id', autoIncrement: true });
            }
        };
    });
}

function getPendingData(db) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['pending_sync'], 'readonly');
        const store = transaction.objectStore('pending_sync');
        const request = store.getAll();
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

function deletePendingData(db, id) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['pending_sync'], 'readwrite');
        const store = transaction.objectStore('pending_sync');
        const request = store.delete(id);
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
    });
}