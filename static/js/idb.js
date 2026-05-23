// IndexedDB Helper for Offline Data Storage
const DB_NAME = 'KrishiMitraDB';
const DB_VERSION = 1;
const STORES = {
    CROPS: 'crops',
    TASKS: 'tasks',
    EXPENSES: 'expenses',
    LISTINGS: 'listings',
    PENDING_SYNC: 'pending_sync'
};

let db = null;

// Open database
function openDB() {
    return new Promise((resolve, reject) => {
        if (db) {
            resolve(db);
            return;
        }
        
        const request = indexedDB.open(DB_NAME, DB_VERSION);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => {
            db = request.result;
            resolve(db);
        };
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            
            // Create stores
            if (!db.objectStoreNames.contains(STORES.CROPS)) {
                db.createObjectStore(STORES.CROPS, { keyPath: 'id', autoIncrement: true });
            }
            if (!db.objectStoreNames.contains(STORES.TASKS)) {
                db.createObjectStore(STORES.TASKS, { keyPath: 'id', autoIncrement: true });
            }
            if (!db.objectStoreNames.contains(STORES.EXPENSES)) {
                db.createObjectStore(STORES.EXPENSES, { keyPath: 'id', autoIncrement: true });
            }
            if (!db.objectStoreNames.contains(STORES.LISTINGS)) {
                db.createObjectStore(STORES.LISTINGS, { keyPath: 'id', autoIncrement: true });
            }
            if (!db.objectStoreNames.contains(STORES.PENDING_SYNC)) {
                db.createObjectStore(STORES.PENDING_SYNC, { keyPath: 'id', autoIncrement: true });
            }
        };
    });
}

// Save data offline
async function saveOffline(storeName, data) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const transaction = db.transaction([storeName], 'readwrite');
        const store = transaction.objectStore(storeName);
        const request = store.add(data);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// Get all offline data
async function getOfflineData(storeName) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const transaction = db.transaction([storeName], 'readonly');
        const store = transaction.objectStore(storeName);
        const request = store.getAll();
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// Delete offline data
async function deleteOfflineData(storeName, id) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const transaction = db.transaction([storeName], 'readwrite');
        const store = transaction.objectStore(storeName);
        const request = store.delete(id);
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
    });
}

// Queue data for sync when online
async function queueForSync(url, payload) {
    const db = await openDB();
    return new Promise((resolve, reject) => {
        const transaction = db.transaction([STORES.PENDING_SYNC], 'readwrite');
        const store = transaction.objectStore(STORES.PENDING_SYNC);
        const request = store.add({
            url: url,
            payload: payload,
            timestamp: new Date().toISOString()
        });
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// Sync pending data
async function syncPendingData() {
    const pending = await getOfflineData(STORES.PENDING_SYNC);
    
    for (const item of pending) {
        try {
            const response = await fetch(item.url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(item.payload)
            });
            
            if (response.ok) {
                await deleteOfflineData(STORES.PENDING_SYNC, item.id);
                console.log('Synced:', item.url);
            }
        } catch (error) {
            console.log('Sync failed for:', item.url);
        }
    }
}

// Check online status
window.addEventListener('online', () => {
    console.log('Online - Syncing data...');
    syncPendingData();
    
    // Show notification
    const notification = document.createElement('div');
    notification.className = 'alert alert-success alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-2';
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        <i class="fas fa-wifi"></i> You are back online! Syncing your data...
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.prepend(notification);
    setTimeout(() => notification.remove(), 3000);
});

window.addEventListener('offline', () => {
    const notification = document.createElement('div');
    notification.className = 'alert alert-warning alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-2';
    notification.style.zIndex = '9999';
    notification.innerHTML = `
        <i class="fas fa-wifi"></i> You are offline. Data will be saved locally and sync when online.
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.prepend(notification);
    setTimeout(() => notification.remove(), 4000);
});

// Export functions
window.KrishiDB = {
    saveOffline,
    getOfflineData,
    deleteOfflineData,
    queueForSync,
    syncPendingData,
    STORES
};