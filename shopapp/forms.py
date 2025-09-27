from django import forms

from shopapp.models import Courses, Bidhaas

class DateInput(forms.DateInput):
    input_type = "date"

class AddBidhaaForm(forms.Form):
    jina=forms.CharField(label="Jina la Bidhaa",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    category=forms.CharField(label="Category",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    quantity=forms.IntegerField(label="Quantity",widget=forms.NumberInput(attrs={"class":"form-control"}))
    alert_quantity=forms.IntegerField(label="Alert Quantity",widget=forms.NumberInput(attrs={"class":"form-control"}))
    code=forms.CharField(label="Code",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    brand=forms.CharField(label="Brand",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    price=forms.DecimalField(label="Price (TZs)",max_digits=10,decimal_places=2,widget=forms.NumberInput(attrs={"class":"form-control", "step": "0.01"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

class EditBidhaaForm(forms.ModelForm):
    jina=forms.CharField(label="Jina la Bidhaa",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    category=forms.CharField(label="Category",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    quantity=forms.IntegerField(label="Quantity",widget=forms.NumberInput(attrs={"class":"form-control"}))
    alert_quantity=forms.IntegerField(label="Alert Quantity",widget=forms.NumberInput(attrs={"class":"form-control"}))
    code=forms.CharField(label="Code",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    brand=forms.CharField(label="Brand",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    price=forms.DecimalField(label="Price",max_digits=10,decimal_places=2,widget=forms.NumberInput(attrs={"class":"form-control", "step": "0.01"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta:
        model = Bidhaas
        fields = ['jina','category','quantity','alert_quantity','code','brand','price','profile_pic']

class SearchBidhaaForm(forms.Form):
    #form for searching bidhaa
    search = forms.CharField(
        max_length = 100,
        required = False,
        widget = forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Search by name, category, brand, or code ...'
        })
    )

    category = forms.CharField(
        max_length = 100,
        required = False,
        widget = forms.TextInput(attrs = {
            'class': 'form-control',
            'placeholder': 'Filter by category'
        })
    )

    min_price =forms.DecimalField(
        max_digits = 10,
        decimal_places = 2, 
        required = False,
        widget = forms.NumberInput(attrs = {
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Min price'
        })
    )

    max_price =forms.DecimalField(
        max_digits = 10,
        decimal_places = 2, 
        required = False,
        widget = forms.NumberInput(attrs = {
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Max price'
        })
    )

    low_stock_only = forms.BooleanField(
        required = False,
        widget = forms.CheckboxInput(attrs = {
            'class': 'form-check-input'
        }),
        label = 'Show low stock items only'
    )

class BulkUpdateQuantityForm(forms.Form):
    #form for bulk updating quantities
    def __init__(self, *args, **kwargs):
        bidhaas = kwargs.pop('bidhaas', [])
        super() .__init__(*args, **kwargs)

        #dynamically add quantity fields for each bidha
        for bidhaa in bidhaas:
            field_name = f'quantity_{bidhaa.id}'
            self.fields[field_name] = forms.IntegerField(
                label = f'{bidhaa.jina} Quantity',
                initial = bidhaa.quantity,
                min_value = 0,
                widget = forms.NumberInput(attrs={
                    'class': 'form-control',
                    'min': '0'
                })
            ) 

class ImportBidhaaForm(forms.Form):
    #form for importing data from CSV
    csv_file = forms.FileField(
        label = "CSV File",
        widget = forms.FileInput(attrs={
            'class': 'form-control-file',
            'accept': '.csv'
        }),
        help_text="Upload a CSV file with columns: jina, category, quantity, alert_quantity, code, brand, price"
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data.get('csv_file')
        if csv_file:
            if not csv_file.name.endswith('.csv'):
                raise forms.ValidationError('Files must be a CSV file.')
            
            if csv_file.size > 5 * 1024 * 1024: #5MB Limit
                raise forms.ValidationError('File size must be less than 5MB.')

        return csv_file
        