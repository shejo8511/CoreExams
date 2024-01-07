from django import forms
from django.forms import ModelChoiceField
from .models import Company, Membership, Country, Province, City
from exam.models import TypeExam

class MembershipForm(forms.ModelForm):

    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Membresia'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Descipcion de la Membresia'}))
    cost = forms.DecimalField(max_digits=10, decimal_places=2,widget=forms.TextInput(attrs={'class':'form-control'}))
    connections = forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = Membership
        fields = ('name','description', 'cost', 'connections')

class CountryForm(forms.ModelForm):

    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Pais'}))
    
    class Meta:
        model = Country
        fields = ('name',)

class ProvinceForm(forms.ModelForm):

    country = forms.ModelChoiceField(queryset=Country.objects.filter(enabled=1),widget=forms.Select(attrs={'class':'form-control'}))
    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Provincia'}))

    class Meta:
        model = Province
        fields = ('name',)

class CityForm(forms.ModelForm):

    country = forms.ModelChoiceField(queryset=Country.objects.filter(enabled=1),widget=forms.Select(attrs={'class':'form-control'}))
    province = forms.ModelChoiceField(queryset=Province.objects.filter(enabled=1),widget=forms.Select(attrs={'class':'form-control'}))
    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Ciudad'}))

    class Meta:
        model = City
        fields = ('name',)

class CompanyForm(forms.ModelForm):
    TYPE_IDENTI = (
        ('CI','CI'),
        ('PASS','PASAPORTE'),
        ('RUC','RUC'),
    )

    company_name = forms.CharField(max_length="50",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Empresa'}))
    identification = forms.CharField(max_length="13",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'0000000000001'}))
    identification_type = forms.ChoiceField(choices=TYPE_IDENTI,widget=forms.Select(attrs={'class':'form-control'}))
    name = forms.CharField(max_length="50",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombres'}))
    last_name = forms.CharField(max_length="50",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apellidos'}))
    phone = forms.CharField(max_length="10",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'0720000000'}))
    address = forms.CharField(max_length="500",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Av. Calle. Segunda Numero:1234 Main St'}))
    logo = forms.ImageField(label='Logo Empresa')
    country = forms.ModelChoiceField(queryset=Country.objects.filter(enabled=1),widget=forms.Select(attrs={'class':'form-control'}))
    province = forms.ModelChoiceField(queryset=Province.objects.filter(enabled=1),widget=forms.Select(attrs={'class':'form-control'}))
    city = forms.ModelChoiceField(queryset=City.objects.filter(enabled=1),widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Company
        fields = ('company_name', 'name', 'last_name', 'identification','identification_type','phone','address','logo','country','province','city')
