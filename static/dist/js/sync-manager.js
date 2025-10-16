class SyncManager {
    constructor(dbManager) {
      this.db = dbManager;
      this.apiBase = '/api';
      this.lastSync = localStorage.getItem('lastSync') || null;
      this.syncInProgress = false;
    }
  
    // Check if online
    isOnline() {
      return navigator.onLine;
    }
  
    // Download data from server
    async downloadData() {
      if (!this.isOnline()) {
        console.log('Offline: Cannot download data');
        return;
      }
  
      try {
        // Download bidhaas
        const response = await fetch(`${this.apiBase}/bidhaas/sync/?last_sync=${this.lastSync || ''}`);
        const data = await response.json();
        
        for (const bidhaa of data.data) {
          await this.db.save('bidhaas', bidhaa);
        }
  
        this.lastSync = data.timestamp;
        localStorage.setItem('lastSync', this.lastSync);
        
        this.showNotification('Data synced successfully', 'success');
      } catch (error) {
        console.error('Download failed:', error);
        this.showNotification('Sync failed', 'error');
      }
    }
  
    // Upload queued data to server
    async uploadData() {
      if (!this.isOnline() || this.syncInProgress) {
        return;
      }
  
      this.syncInProgress = true;
      this.updateSyncStatus('Syncing...');
  
      try {
        const queuedItems = await this.db.getUnsyncedItems();
        
        for (const item of queuedItems) {
          await this.syncItem(item);
        }
  
        this.showNotification(`${queuedItems.length} items synced`, 'success');
      } catch (error) {
        console.error('Upload failed:', error);
        this.showNotification('Sync failed', 'error');
      } finally {
        this.syncInProgress = false;
        this.updateSyncStatus('');
      }
    }
  
    async syncItem(item) {
      try {
        let response;
        
        switch (item.type) {
          case 'sale':
            response = await fetch(`${this.apiBase}/sales/`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
              },
              body: JSON.stringify(item.data)
            });
            break;
          
          case 'bidhaa':
            response = await fetch(`${this.apiBase}/bidhaas/${item.data.id}/`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
              },
              body: JSON.stringify(item.data)
            });
            break;
        }
  
        if (response.ok) {
          // Mark as synced and delete from queue
          await this.db.delete('sync_queue', item.id);
        }
      } catch (error) {
        console.error(`Failed to sync ${item.type}:`, error);
        throw error;
      }
    }
  
    // Full sync (download + upload)
    async fullSync() {
      await this.downloadData();
      await this.uploadData();
    }
  
    // Register sync event listeners
    registerSyncListeners() {
      // Listen for online/offline events
      window.addEventListener('online', () => {
        console.log('Back online!');
        this.showNotification('Connection restored', 'success');
        this.fullSync();
      });
  
      window.addEventListener('offline', () => {
        console.log('Gone offline');
        this.showNotification('Working offline', 'warning');
      });
  
      // Periodic sync (every 5 minutes when online)
      setInterval(() => {
        if (this.isOnline() && !this.syncInProgress) {
          this.fullSync();
        }
      }, 5 * 60 * 1000);
    }
  
    // UI Helpers
    getCSRFToken() {
      return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
  
    updateSyncStatus(message) {
      const statusEl = document.getElementById('sync-status');
      if (statusEl) {
        statusEl.textContent = message;
      }
    }
  
    showNotification(message, type) {
      // Implement your notification system
      console.log(`[${type}] ${message}`);
    }
  }
  
  // Initialize
  const syncManager = new SyncManager(dbManager);