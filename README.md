# Bidhaa Management System

A complete, production-ready Point of Sale (POS), inventory management, and sales tracking system with offline support and automatic cloud synchronization.

## Features

### Core Features
- **Point of Sale (POS)** - Modern, intuitive POS interface
- **Inventory Management** - Track products, stock levels, and alerts
- **Sales Management** - Complete sales history and tracking
- **Customer Management** - Maintain customer database and purchase history
- **Returns & Refunds** - Process returns with automatic stock restoration
- **Sales Reports** - Detailed analytics and reporting
- **Invoice Generation** - Professional, printable invoices

### Offline Support
- **Work Offline** - Full functionality without internet connection
- **Automatic Sync** - Seamless data synchronization when online
- **Local Storage** - IndexedDB for secure local data storage
- **Background Sync** - Automatic sync in the background
- **Conflict Resolution** - Intelligent handling of data conflicts

### Additional Features
- **Multi-user Support** - Role-based access control
- **Real-time Dashboards** - Sales statistics and KPIs
- **Mobile Responsive** - Works on desktop, tablet, and mobile
- **PWA Support** - Install as a native app
- **REST API** - Complete API for integration

## Technology Stack

- **Backend**: Django 4.0.6
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **API**: Django REST Framework
- **Offline**: Service Workers, IndexedDB, Progressive Web App
- **UI Framework**: Bootstrap 4, AdminLTE

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- pip (Python package manager)

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/salva669/shopping.git
cd bidhaa-management-system
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
```bash
# Copy the example env file
cp .env.example .env

# Generate a secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Update .env with the generated key
```

5. **Initialize Database**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

6. **Collect Static Files**
```bash
python manage.py collectstatic --noinput
```

7. **Run Development Server**
```bash
python manage.py runserver
```

8. **Access the Application**
- Main Application: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- Offline POS: http://localhost:8000/offline-pos/

## Detailed Setup Instructions

For complete setup instructions, see [SETUP.md](./SETUP.md)

## Usage Guide

### For End Users
See [USER_GUIDE.md](./docs/USER_GUIDE.md)

### For Developers
See [DEVELOPER_GUIDE.md](./docs/DEVELOPER_GUIDE.md)

### API Documentation
See [API.md](./docs/API.md)

## File Structure

```
bidhaa-management-system/
├── README.md
├── SETUP.md
├── requirements.txt
├── .env.example
├── .gitignore
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── your_app_name/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── api_views.py
│   ├── api_urls.py
│   ├── api_serializers.py
│   ├── admin.py
│   └── apps.py
├── templates/
│   └── hod_template/
│       ├── base_template.html
│       ├── manage_bidhaa_template.html
│       ├── add_bidhaa_template.html
│       ├── edit_bidhaa_template.html
│       ├── view_bidhaa_template.html
│       ├── make_sale_template.html
│       ├── sales_dashboard_template.html
│       ├── offline_pos_template.html
│       └── (more templates)
├── static/
│   ├── js/
│   │   ├── db-manager.js
│   │   ├── sync-manager.js
│   │   ├── offline-pos.js
│   │   └── service-worker.js
│   ├── css/
│   ├── images/
│   └── manifest.json
├── media/
│   └── (user uploaded files)
└── docs/
    ├── SETUP.md
    ├── USER_GUIDE.md
    ├── DEVELOPER_GUIDE.md
    └── API.md
```

## Key Features Explained

### Offline-First Architecture
The system uses a Service Worker and IndexedDB to enable offline functionality:
- All data syncs to local storage on login
- Users can work without internet connection
- Changes are queued locally
- Automatic sync occurs when connection is restored
- Works like Google Drive

### Sales Management
- Create sales with multiple items
- Apply discounts and taxes
- Multiple payment methods (Cash, M-Pesa, Bank, Credit)
- Print professional invoices
- Track sales history

### Inventory Control
- Real-time stock tracking
- Low stock alerts
- Product categorization
- Stock history
- Automatic stock deduction on sale

### Customer Management
- Maintain customer database
- Track purchase history
- Calculate customer lifetime value
- Quick customer lookup

### Returns & Refunds
- Process partial or full returns
- Automatic stock restoration
- Refund calculation
- Return tracking
- Multiple return reasons

### Reports & Analytics
- Daily/weekly/monthly reports
- Top selling products
- Payment method breakdown
- Revenue trends
- Staff performance

## Configuration

### Environment Variables (.env)

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:8000
```

### Django Settings
Key configurations in `settings.py`:
- Database backend (SQLite/PostgreSQL)
- Static file serving
- Media file handling
- CORS headers
- REST framework settings

## Deployment

### Production Checklist
- [ ] Set DEBUG = False
- [ ] Update SECRET_KEY
- [ ] Configure ALLOWED_HOSTS
- [ ] Use PostgreSQL database
- [ ] Set up HTTPS
- [ ] Configure static file serving
- [ ] Set up email backend
- [ ] Enable CORS for production domain
- [ ] Configure backups
- [ ] Set up monitoring

### Deployment Platforms
- Heroku
- AWS
- DigitalOcean
- PythonAnywhere
- Render

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed instructions.

## Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError: No module named 'django'**
- Solution: Activate virtual environment and install requirements
```bash
pip install -r requirements.txt
```

**Issue: "No such table" error**
- Solution: Run migrations
```bash
python manage.py migrate
```

**Issue: Static files not loading**
- Solution: Collect static files
```bash
python manage.py collectstatic --noinput
```

**Issue: Service Worker not registering**
- Solution: Check browser console, verify file paths, use HTTPS in production

For more troubleshooting, see [SETUP.md](./SETUP.md#troubleshooting)

## API Endpoints

### Bidhaa (Products)
- `GET /api/bidhaas/` - List all products
- `POST /api/bidhaas/` - Create product
- `GET /api/bidhaas/{id}/` - Get product details
- `PUT /api/bidhaas/{id}/` - Update product
- `DELETE /api/bidhaas/{id}/` - Delete product
- `GET /api/bidhaas/sync/` - Sync products

### Sales
- `GET /api/sales/` - List all sales
- `POST /api/sales/` - Create sale
- `GET /api/sales/{id}/` - Get sale details
- `POST /api/sales/bulk_create/` - Bulk create sales

### Customers
- `GET /api/customers/` - List customers
- `POST /api/customers/` - Create customer
- `GET /api/customers/{id}/` - Get customer details

For complete API documentation, see [API.md](./docs/API.md)

## Database Models

- **Bidhaas** - Product/inventory items
- **Sale** - Sales transactions
- **SaleItem** - Individual items in a sale
- **Customer** - Customer information
- **SaleReturn** - Product returns
- **ReturnItem** - Items being returned

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support:
1. Check the [troubleshooting section](./SETUP.md#troubleshooting)
2. Read the [user guide](./docs/USER_GUIDE.md)
3. Check [FAQ](./docs/FAQ.md)
4. Open an issue on GitHub

## Roadmap

- [ ] Multi-language support
- [ ] Barcode scanning
- [ ] Supplier management
- [ ] Advanced reporting
- [ ] Mobile app
- [ ] Payment gateway integration
- [ ] Automated backups
- [ ] Multi-branch support

## Security

- All data is validated server-side
- CSRF protection enabled
- SQL injection prevention
- XSS protection
- Secure password hashing
- Session management
- Authentication required for all views

## Performance

- IndexedDB caching for offline support
- Service Worker for static assets
- Database indexing
- Query optimization
- Responsive design
- Mobile-optimized UI

## Credits

Developed for small to medium businesses in Tanzania (TZ).

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for version history and updates.

## Contact

- Email: henrymkama@gmail.com
- GitHub: [@salva669](https://github.com/salva669)


---

Made with by [ChiboTech]
