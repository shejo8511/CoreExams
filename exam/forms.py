from django import forms
from .models import TypeExam

class TypeExamForm(forms.ModelForm):

    name = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre Tipo Examen'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Descipcion de la Examen'}))
    
    class Meta:
        model = TypeExam
        fields = ('id','name','description',)