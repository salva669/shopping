# Bidhaa Management System - User Guide

Complete guide for using the Bidhaa Management System for point of sale, inventory management, and sales tracking.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Dashboard](#dashboard)
3. [Product Management](#product-management)
4. [Point of Sale (POS)](#point-of-sale-pos)
5. [Offline Mode](#offline-mode)
6. [Customer Management](#customer-management)
7. [Sales Management](#sales-management)
8. [Returns & Refunds](#returns--refunds)
9. [Reports](#reports)
10. [Tips & Tricks](#tips--tricks)

---

## Getting Started

### Login
1. Open the application: `http://localhost:8000/`
2. Enter your username and password
3. Click "Login"

### Dashboard
After login, you'll see the main dashboard with:
- Quick statistics (today's sales, this week's sales, etc.)
- Top selling products
- Recent sales
- Quick action buttons

### Navigation Menu
The sidebar menu contains:
- **Dashboard** - Main overview
- **Products** - Manage inventory
- **Sales** - Create and track sales
- **Reports** - View analytics
- **Customers** - Manage customer database
- **Settings** - System configuration

---

## Dashboard

### What You See
- **Today's Sales** - Total revenue for today
- **This Week** - Weekly revenue total
- **This Month** - Monthly revenue total
- **Quick Actions** - Shortcuts to common tasks

### Using the Dashboard
1. Check daily/weekly/monthly sales at a glance
2. See best-selling products
3. Monitor recent transactions
4. Access key features quickly

### Interpreting Cards
- **Blue Card** - General information
- **Green Card** - Positive metrics (good sales)
- **Yellow Card** - Warnings (low stock)
- **Red Card** - Critical alerts

---

## Product Management

### Managing Products

#### Add New Product
1. Click **Products** > **Add New Bidhaa**
2. Fill in the form:
   - **Product Name** - Name of the product
   - **Category** - Product category (e.g., "Electronics")
   - **Brand** - Brand name
   - **Code** - Unique product code/SKU
   - **Quantity** - Current stock level
   - **Alert Quantity** - Minimum stock level for alerts
   - **Price** - Selling price in TZS
   - **Image** - Product photo (optional)
3. Click "Add Bidhaa"

#### Edit Product
1. Click **Products** > **Manage Bidhaa**
2. Find the product and click the **Edit** button (pencil icon)
3. Update the information
4. Click "Update Bidhaa"

#### View Product Details
1. Click **Products** > **Manage Bidhaa**
2. Click the **View** button (eye icon)
3. See all product information including:
   - Stock status
   - Total value in inventory
   - Purchase history
   - Low stock warnings

#### Delete Product
1. Click **Products** > **Manage Bidhaa**
2. Click the **Delete** button (trash icon)
3. Confirm deletion

### Low Stock Alerts
- Products below alert quantity show in yellow
- Click **Products** > **Low Stock Alert**
- System automatically alerts you when stock runs low

---

## Point of Sale (POS)

### Making a Sale

#### Standard POS
1. Click **Sales** > **Make Sale (POS)**
2. Search for products by name, code, or category
3. Click on product card to add to cart
4. Adjust quantity in cart if needed
5. Enter customer information (optional)
6. Select payment method
7. Click "Checkout"
8. Review total and click "Complete Sale"
9. Print receipt if needed

#### Offline POS
1. Click **Sales** > **Offline POS**
2. Works the same as standard POS
3. **Red indicator** = Offline mode
4. Sales are saved locally
5. Auto-syncs when connection restored
6. Click "Sync Now" to manually sync

### Payment Methods
- **Cash** - Physical payment
- **M-Pesa** - Mobile money payment (enter M-Pesa reference)
- **Bank** - Bank transfer (enter bank reference)
- **Credit** - Customer credit account

### Applying Discounts
1. In checkout, enter discount amount in **Discount** field
2. Tax is calculated automatically
3. Total adjusts accordingly

### Adding Customers
1. In checkout, enter customer details:
   - Name
   - Phone number
   - Email (optional)
2. System saves customer for future reference

---

## Offline Mode

### What is Offline Mode?
- Allows you to use the system without internet
- Works exactly like online mode
- Changes are saved locally
- Auto-syncs when online

### Working Offline
1. You can continue using all features
2. Sales are saved locally
3. You'll see "Offline" indicator in red
4. Don't close the browser tab

### When Connection Returns
1. System automatically syncs
2. Green indicator shows sync successful
3. All offline changes upload to server
4. You can see the changes reflected

### Manual Sync
1. Click "Sync Now" button
2. System syncs queued changes
3. You'll see confirmation message

### Important Notes
- Always download data first while online
- First-time users must be online to download products
- Keep browser open during offline work
- Don't force-close the application

---

## Customer Management

### Viewing Customers
1. Click **Customers** > **Manage Customers**
2. Search by name, phone, or email
3. See total purchases and money spent

### Customer Details
1. Click **View** button next to customer
2. See customer information:
   - Contact details
   - Total purchases
   - Total spent
   - Purchase history
   - Average purchase value

### Adding Customers
Customers are automatically added when:
- You make a sale and enter customer info
- You manually add a customer

### Manual Customer Addition
1. Click **Customers** > **Add New Customer**
2. Fill in information
3. Click "Add Customer"

### Editing Customer
1. Click **Customers** > **Manage Customers**
2. Find customer and click **Edit**
3. Update information
4. Click "Update"

---

## Sales Management

### Viewing Sales History
1. Click **Sales** > **Sales History**
2. See all sales with:
   - Sale number
   - Date
   - Customer
   - Amount
   - Payment method
   - Status

### Filtering Sales
1. In Sales History, use filters:
   - **Search** - By sale number or customer
   - **Date Range** - Select from and to dates
   - **Payment Method** - Filter by payment type
   - **Status** - Show completed, pending, or cancelled

### Viewing Sale Details
1. Click **View** button on sale
2. See all items purchased
3. See customer information
4. See payment details
5. Print invoice

### Printing Invoice
1. From sale details, click "Print Invoice"
2. Select printer
3. Click print
4. Invoice prints professionally formatted

---

## Returns & Refunds

### Processing a Return
1. Click **Sales** > **Sales History**
2. Find the sale to return
3. Click **View** to see details
4. Click "Process Return"
5. Select items to return:
   - Check items you're returning
   - Specify quantity for each
6. Select return reason:
   - Defective Product
   - Wrong Item
   - Changed Mind
   - Expired Product
   - Damaged
   - Other
7. Add notes if needed
8. Click "Process Return"

### Tracking Returns
1. Click **Sales** > **Returns History**
2. See all returns with:
   - Return number
   - Original sale
   - Items returned
   - Refund amount
   - Reason
   - Status

### Return Status
- **Pending** - Return awaiting processing
- **Approved** - Return accepted
- **Completed** - Refund processed
- **Rejected** - Return denied

### Stock Restoration
- When return is processed, stock is automatically restored
- Product quantity increases back to inventory

---

## Reports

### Accessing Reports
1. Click **Sales** > **Sales Reports**

### Report Types

#### Daily Report
- All transactions for today
- Total revenue
- Number of sales
- Payment breakdown

#### Weekly Report
- Sales from Monday to Sunday
- Weekly total
- Daily breakdown
- Trends

#### Monthly Report
- All sales for the month
- Monthly total
- Best-selling products
- Payment analysis

#### Custom Report
- Select date range
- See sales for specific period
- Detailed breakdown

### Report Information
- **Number of Sales** - Transaction count
- **Total Revenue** - Total money received
- **Average Sale** - Average transaction value
- **Top Products** - Best sellers
- **Payment Methods** - Cash, M-Pesa, Bank breakdown
- **Daily Breakdown** - Sales by day

### Exporting Reports
- Click "Print" to print report
- Click "Export to CSV" to save as spreadsheet
- Click "Export to Excel" for Excel format

---

## Tips & Tricks

### Productivity Tips

#### Keyboard Shortcuts
- **Ctrl + F** - Search products quickly
- **Enter** - Submit forms
- **Esc** - Close modals/dialogs

#### Working Faster
1. Add frequently used products to favorites
2. Use customer quick-lookup
3. Enable notifications for low stock
4. Sync regularly to keep data current

### Inventory Best Practices
1. Set realistic alert quantities
2. Review low stock daily
3. Reorder before stockouts
4. Keep product information updated
5. Regular inventory counts

### Sales Best Practices
1. Always get customer information for tracking
2. Keep receipts for reference
3. Process returns promptly
4. Review daily reports
5. Monitor payment methods

### Data Management
1. Back up regularly
2. Keep system updated
3. Archive old sales data
4. Clean up test products
5. Review customer list monthly

### Troubleshooting

#### Product Not Appearing in POS
- Check if quantity is 0 (can't sell 0 stock)
- Search by product code
- Refresh page

#### Sale Won't Complete
- Check internet connection
- Verify customer information is complete
- Check payment method selected
- Try again

#### Offline Not Working
- Verify Service Worker is registered (DevTools > Application)
- Check IndexedDB has data
- Ensure previous login was successful
- Clear browser cache and reload

#### Missing Data
- Click "Sync Now" to sync manually
- Wait for automatic sync (5 minute interval)
- Check connection status

### Getting Help
1. Check this guide
2. Review system tutorials
3. Contact administrator
4. Check FAQ section

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl + K | Open command palette |
| Ctrl + F | Search |
| Ctrl + P | Print |
| Esc | Close modal |
| Tab | Navigate fields |
| Enter | Submit form |

---

## Common Tasks

### Daily Tasks
1. [ ] Check dashboard
2. [ ] Review low stock items
3. [ ] Check sales from previous day
4. [ ] Verify cash drawer

### Weekly Tasks
1. [ ] Review weekly report
2. [ ] Check top-selling products
3. [ ] Verify inventory counts
4. [ ] Review customer purchases

### Monthly Tasks
1. [ ] Generate monthly report
2. [ ] Review payment methods
3. [ ] Analyze sales trends
4. [ ] Archive old data
5. [ ] Review returns

---

## FAQs

### Q: Can I use the system offline?
**A:** Yes! Go to Offline POS. Sales sync automatically when online.

### Q: How do I add a customer?
**A:** Either add manually in Customers section, or enter info during checkout.

### Q: Can I edit a completed sale?
**A:** No, but you can process a return to adjust inventory.

### Q: How do I export data?
**A:** Go to Reports and click Export options.

### Q: What happens if internet disconnects during a sale?
**A:** Sale is saved locally and will sync when online.

### Q: How often does data sync?
**A:** Automatically every 5 minutes when online, or manually with "Sync Now".

### Q: Can multiple users use the system?
**A:** Yes, each user has their own login and track record.

### Q: How do I backup my data?
**A:** Use admin panel to export or set up automatic backups.

---

## Support & Feedback

For issues or feedback:
- Contact system administrator
- Check documentation
- File bug reports on GitHub
- Email support team

---

## Version Information

- **Version:** 1.0.0
- **Last Updated:** 2024
- **Requirements:** Internet connection for initial setup

---

Thank you for using Bidhaa Management System!
