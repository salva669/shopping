from django import forms
from django.core.validators import MinValueValidator
from .models import Bidhaas, Sale, SaleItem, Customer

class DateInput(forms.DateInput):
    input_type = "date"

class AddBidhaaForm(forms.ModelForm):
    """Form for adding new bidhaa"""
    
    class Meta:
        model = Bidhaas
        fields = ['jina', 'category', 'quantity', 'alert_quantity', 'code', 'brand', 'price', 'profile_pic']
        widgets = {
            'jina': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0'
            }),
            'alert_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Alert when quantity reaches this level'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product code/SKU'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand name'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00'
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
        }
        labels = {
            'jina': 'Jina la Bidhaa',
            'category': 'Category',
            'quantity': 'Quantity in Stock',
            'alert_quantity': 'Alert Quantity',
            'code': 'Product Code',
            'brand': 'Brand',
            'price': 'Price (TZS)',
            'profile_pic': 'Product Image',
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            # Check if code already exists (excluding current instance if editing)
            existing = Bidhaas.objects.filter(code=code)
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError('A product with this code already exists.')
        return code

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

    def clean_alert_quantity(self):
        alert_quantity = self.cleaned_data.get('alert_quantity')
        quantity = self.cleaned_data.get('quantity')
        
        if alert_quantity and quantity and alert_quantity > quantity:
            raise forms.ValidationError('Alert quantity cannot be greater than current quantity.')
        return alert_quantity


class EditBidhaaForm(forms.ModelForm):
    """Form for editing existing bidhaa - This fixes your original issue"""
    
    class Meta:
        model = Bidhaas
        fields = ['jina', 'category', 'quantity', 'alert_quantity', 'code', 'brand', 'price', 'profile_pic']
        widgets = {
            'jina': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'alert_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product code/SKU'
            }),
            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brand name'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            }),
        }
        labels = {
            'jina': 'Jina la Bidhaa',
            'category': 'Category',
            'quantity': 'Quantity in Stock',
            'alert_quantity': 'Alert Quantity',
            'code': 'Product Code',
            'brand': 'Brand',
            'price': 'Price (TZS)',
            'profile_pic': 'Product Image',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make profile_pic optional for editing
        self.fields['profile_pic'].required = False
        self.fields['profile_pic'].help_text = 'Leave empty to keep current image'

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            # Check if code already exists (excluding current instance)
            existing = Bidhaas.objects.filter(code=code).exclude(pk=self.instance.pk)
            if existing.exists():
                raise forms.ValidationError('A product with this code already exists.')
        return code

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return price

    def clean_alert_quantity(self):
        alert_quantity = self.cleaned_data.get('alert_quantity')
        quantity = self.cleaned_data.get('quantity')
        
        if alert_quantity and quantity and alert_quantity > quantity:
            raise forms.ValidationError('Alert quantity cannot be greater than current quantity.')
        return alert_quantity


class SearchBidhaaForm(forms.Form):
    """Form for searching bidhaa"""
    
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, category, brand, or code...'
        })
    )
    
    category = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Filter by category'
        })
    )
    
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Min price'
        })
    )
    
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Max price'
        })
    )
    
    low_stock_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Show low stock items only'
    )

class SaleForm(forms.ModelForm):
    """Form for creating a new sale"""
    
    class Meta:
        model = Sale
        fields = ['customer_name', 'customer_phone', 'customer_email', 
                  'payment_method', 'payment_reference', 'discount', 'tax', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer name (optional)'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer phone (optional)'
            }),
            'customer_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Customer email (optional)'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'form-control'
            }),
            'payment_reference': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile Money code, Bank ref, etc. (optional)'
            }),
            'discount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'value': '0'
            }),
            'tax': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'value': '0'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes (optional)'
            }),
        }
        labels = {
            'customer_name': 'Customer Name',
            'customer_phone': 'Phone Number',
            'customer_email': 'Email',
            'payment_method': 'Payment Method',
            'payment_reference': 'Payment Reference',
            'discount': 'Discount (TZS)',
            'tax': 'Tax (TZS)',
            'notes': 'Notes',
        }

class BulkUpdateQuantityForm(forms.Form):
    """Form for bulk updating quantities"""
    
    def __init__(self, *args, **kwargs):
        bidhaas = kwargs.pop('bidhaas', [])
        super().__init__(*args, **kwargs)
        
        # Dynamically add quantity fields for each bidhaa
        for bidhaa in bidhaas:
            field_name = f'quantity_{bidhaa.id}'
            self.fields[field_name] = forms.IntegerField(
                label=f'{bidhaa.jina} Quantity',
                initial=bidhaa.quantity,
                min_value=0,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control',
                    'min': '0'
                })
            )


class QuickAddBidhaaForm(forms.Form):
    """Simplified form for quick adding bidhaa"""
    
    jina = forms.CharField(
        label="Product Name",
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter product name'
        })
    )
    
    category = forms.CharField(
        label="Category",
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter category'
        })
    )
    
    quantity = forms.IntegerField(
        label="Quantity",
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '0',
            'placeholder': '0'
        })
    )
    
    price = forms.DecimalField(
        label="Price (TZS)",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'min': '0.01',
            'placeholder': '0.00'
        })
    )


class ImportBidhaaForm(forms.Form):
    """Form for importing bidhaa from CSV"""
    
    csv_file = forms.FileField(
        label="CSV File",
        widget=forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': '.csv'
        }),
        help_text="Upload a CSV file with columns: jina, category, quantity, alert_quantity, code, brand, price"
    )
    
    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file:
            if not csv_file.name.endswith('.csv'):
                raise forms.ValidationError('File must be a CSV file.')
            if csv_file.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError('File size must be less than 5MB.')
        return csv_file


class StockAdjustmentForm(forms.Form):
    """Form for adjusting stock quantities with reasons"""
    
    ADJUSTMENT_TYPES = [
        ('add', 'Add Stock'),
        ('remove', 'Remove Stock'),
        ('set', 'Set Quantity'),
    ]
    
    REASON_CHOICES = [
        ('purchase', 'New Purchase'),
        ('sale', 'Sale'),
        ('damage', 'Damaged'),
        ('expired', 'Expired'),
        ('theft', 'Theft'),
        ('count', 'Stock Count Adjustment'),
        ('return', 'Customer Return'),
        ('other', 'Other'),
    ]
    
    adjustment_type = forms.ChoiceField(
        choices=ADJUSTMENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    quantity = forms.IntegerField(
        validators=[MinValueValidator(1)],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        })
    )
    
    reason = forms.ChoiceField(
        choices=REASON_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional notes about this adjustment'
        })
    )