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
    price=forms.DecimalField(label="Price",max_digits=10,decimal_places=2,widget=forms.NumberInput(attrs={"class":"form-control", "step": "0.01"}))
    profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

class EditBidhaaForm(forms.ModelForm):
    #jina=forms.CharField(label="Jina la Bidhaa",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    #category=forms.CharField(label="Category",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    #quantity=forms.IntegerField(label="Quantity",widget=forms.NumberInput(attrs={"class":"form-control"}))
    #alert_quantity=forms.IntegerField(label="Alert Quantity",widget=forms.NumberInput(attrs={"class":"form-control"}))
    #code=forms.CharField(label="Code",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    #brand=forms.CharField(label="Brand",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    #price=forms.DecimalField(label="Price",max_digits=10,decimal_places=2,widget=forms.NumberInput(attrs={"class":"form-control", "step": "0.01"}))
    #profile_pic=forms.FileField(label="Profile Pic",max_length=50,widget=forms.FileInput(attrs={"class":"form-control"}))

    class Meta:
        model = Bidhaas
        fields = ['jina','category','quantity','alert_quantity','code','brand','price','profile_pic']