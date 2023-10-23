from django import forms
from models import Patient

class PatientForm(forms.ModelForm):
    full_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Completo'}))
    identification = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Identificacion'}))
    birthday = forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','placeholder':'Nacimiento','format': 'yyyy/mm/dd'}))
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Edad'}))

    class Meta:
        model = Patient
        fields = ('full_name','identification','birthday','age')
