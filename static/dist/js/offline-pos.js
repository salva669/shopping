class OfflinePOS {
    constructor(dbManager, syncManager) {
      this.db = dbManager;
      this.sync = syncManager;
      this.cart = [];
    }
  
    async init() {
      await this.db.init();
      await this.loadProducts();
      this.sync.registerSyncListeners();
      
      // Try to sync on load if online
      if (this.sync.isOnline()) {
        this.sync.fullSync();
      }
    }
  
    async loadProducts() {
      const bidhaas = await this.db.getAll('bidhaas');
      this.displayProducts(bidhaas);
    }
  
    displayProducts(bidhaas) {
      const container = document.getElementById('products-container');
      if (!container) return;
  
      container.innerHTML = bidhaas.map(bidhaa => `
        <div class="product-card" onclick="offlinePOS.addToCart(${bidhaa.id})">
          <img src="${bidhaa.profile_pic || '/static/images/placeholder.png'}" />
          <h4>${bidhaa.jina}</h4>
          <p>${bidhaa.price} TZS</p>
          <small>Stock: ${bidhaa.quantity}</small>
        </div>
      `).join('');
    }
  
    async addToCart(bidhaaId) {
      const bidhaa = await this.db.get('bidhaas', bidhaaId);
      
      if (!bidhaa) {
        alert('Product not found');
        return;
      }
  
      if (bidhaa.quantity <= 0) {
        alert('Out of stock');
        return;
      }
  
      // Check if already in cart
      const existing = this.cart.find(item => item.bidhaa_id === bidhaaId);
      
      if (existing) {
        existing.quantity++;
      } else {
        this.cart.push({
          bidhaa_id: bidhaaId,
          bidhaa: bidhaa,
          quantity: 1,
          unit_price: bidhaa.price
        });
      }
  
      this.updateCartDisplay();
    }
  
    updateCartDisplay() {
      const cartEl = document.getElementById('cart-items');
      const totalEl = document.getElementById('cart-total');
      
      if (!cartEl) return;
  
      const total = this.cart.reduce((sum, item) => 
        sum + (item.quantity * item.unit_price), 0
      );
  
      cartEl.innerHTML = this.cart.map((item, index) => `
        <div class="cart-item">
          <span>${item.bidhaa.jina}</span>
          <span>${item.quantity} x ${item.unit_price}</span>
          <button onclick="offlinePOS.removeFromCart(${index})">Remove</button>
        </div>
      `).join('');
  
      totalEl.textContent = total.toFixed(2) + ' TZS';
    }
  
    removeFromCart(index) {
      this.cart.splice(index, 1);
      this.updateCartDisplay();
    }
  
    async completeSale() {
      if (this.cart.length === 0) {
        alert('Cart is empty');
        return;
      }
  
      const sale = {
        sale_number: 'OFFLINE-' + Date.now(),
        customer_name: document.getElementById('customer_name')?.value || '',
        customer_phone: document.getElementById('customer_phone')?.value || '',
        payment_method: document.getElementById('payment_method')?.value || 'cash',
        subtotal: this.cart.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0),
        total_amount: this.cart.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0),
        items: this.cart.map(item => ({
          bidhaa_id: item.bidhaa_id,
          quantity: item.quantity,
          unit_price: item.unit_price
        })),
        status: 'completed',
        sale_date: new Date().toISOString(),
        created_at: new Date().toISOString(),
        synced: false
      };
  
      try {
        // Save to local database
        await this.db.save('sales', sale);
        
        // Add to sync queue
        await this.db.addToSyncQueue('sale', sale);
        
        // Update stock locally
        for (const item of this.cart) {
          const bidhaa = await this.db.get('bidhaas', item.bidhaa_id);
          bidhaa.quantity -= item.quantity;
          await this.db.save('bidhaas', bidhaa);
          await this.db.addToSyncQueue('bidhaa', bidhaa);
        }
  
        alert('Sale completed! Will sync when online.');
        this.cart = [];
        this.updateCartDisplay();
        this.loadProducts();
  
        // Try to sync immediately if online
        if (this.sync.isOnline()) {
          this.sync.uploadData();
        }
      } catch (error) {
        console.error('Failed to save sale:', error);
        alert('Failed to complete sale');
      }
    }
  }
  
  // Initialize offline POS
  let offlinePOS;
  document.addEventListener('DOMContentLoaded', async () => {
    offlinePOS = new OfflinePOS(dbManager, syncManager);
    await offlinePOS.init();
    
    // If online and no data, download first
    const bidhaas = await dbManager.getAll('bidhaas');
    if (navigator.onLine && bidhaas.length === 0) {
      console.log('No local data found. Downloading from server...');
      await syncManager.downloadData();
    }
    
    // Load products
    await offlinePOS.loadProducts();
    
    // Update cart display
    offlinePOS.updateCartDisplay();
    
    // Enable/disable checkout button
    setInterval(() => {
      const btn = document.getElementById('checkout-btn');
      btn.disabled = offlinePOS.cart.length === 0;
      document.getElementById('cart-count').textContent = offlinePOS.cart.length + ' items';
    }, 500);
  });