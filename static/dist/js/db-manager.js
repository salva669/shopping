class DBManager {
    constructor() {
      this.dbName = 'BidhaaDB';
      this.version = 1;
      this.db = null;
    }
  
    async init() {
      return new Promise((resolve, reject) => {
        const request = indexedDB.open(this.dbName, this.version);
  
        request.onerror = () => reject(request.error);
        request.onsuccess = () => {
          this.db = request.result;
          resolve(this.db);
        };
  
        request.onupgradeneeded = (event) => {
          const db = event.target.result;
  
          // Create object stores
          if (!db.objectStoreNames.contains('bidhaas')) {
            const bidhaaStore = db.createObjectStore('bidhaas', { keyPath: 'id' });
            bidhaaStore.createIndex('updated_at', 'updated_at', { unique: false });
          }
  
          if (!db.objectStoreNames.contains('sales')) {
            const salesStore = db.createObjectStore('sales', { keyPath: 'id', autoIncrement: true });
            salesStore.createIndex('synced', 'synced', { unique: false });
            salesStore.createIndex('created_at', 'created_at', { unique: false });
          }
  
          if (!db.objectStoreNames.contains('customers')) {
            db.createObjectStore('customers', { keyPath: 'id' });
          }
  
          if (!db.objectStoreNames.contains('sync_queue')) {
            const syncStore = db.createObjectStore('sync_queue', { keyPath: 'id', autoIncrement: true });
            syncStore.createIndex('type', 'type', { unique: false });
          }
        };
      });
    }
  
    // Save data to IndexedDB
    async save(storeName, data) {
      const tx = this.db.transaction(storeName, 'readwrite');
      const store = tx.objectStore(storeName);
      return new Promise((resolve, reject) => {
        const request = store.put(data);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    }
  
    // Get all items from store
    async getAll(storeName) {
      const tx = this.db.transaction(storeName, 'readonly');
      const store = tx.objectStore(storeName);
      return new Promise((resolve, reject) => {
        const request = store.getAll();
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    }
  
    // Get single item
    async get(storeName, id) {
      const tx = this.db.transaction(storeName, 'readonly');
      const store = tx.objectStore(storeName);
      return new Promise((resolve, reject) => {
        const request = store.get(id);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    }
  
    // Delete item
    async delete(storeName, id) {
      const tx = this.db.transaction(storeName, 'readwrite');
      const store = tx.objectStore(storeName);
      return new Promise((resolve, reject) => {
        const request = store.delete(id);
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      });
    }
  
    // Clear all data from store
    async clear(storeName) {
      const tx = this.db.transaction(storeName, 'readwrite');
      const store = tx.objectStore(storeName);
      return new Promise((resolve, reject) => {
        const request = store.clear();
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      });
    }
  
    // Add to sync queue
    async addToSyncQueue(type, data) {
      return this.save('sync_queue', {
        type: type,  // 'sale', 'bidhaa', 'customer'
        data: data,
        timestamp: new Date().toISOString(),
        synced: false
      });
    }
  
    // Get unsynced items
    async getUnsyncedItems() {
      const tx = this.db.transaction('sync_queue', 'readonly');
      const store = tx.objectStore('sync_queue');
      const index = store.index('synced');
      return new Promise((resolve, reject) => {
        const request = index.getAll(false);
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    }
  }
  
  // Export instance
  const dbManager = new DBManager();