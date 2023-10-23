from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50,widget=forms.TextInput(attrs={'class': 'form-control border-1 shadow-sm px-4 text-primary text-center', 'id': 'username', 'placeholder': 'USUARIO'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control border-1 shadow-sm px-4 text-primary text-center', 'id': 'password', 'placeholder': 'CONTRASEÑA'}), label_suffix='')

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(max_length="50",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.CharField(max_length="50",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'email@ejemplo.com'}))
    password1 = forms.CharField(max_length="50",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}))
    password2 = forms.CharField(max_length="50",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar Contraseña'}))
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')

class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(max_length="50",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}))
    email = forms.CharField(max_length="50",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'email@ejemplo.com'}))
    password1 = forms.CharField(max_length="50",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Contraseña'}))
    password2 = forms.CharField(max_length="50",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirmar Contraseña'}))
    
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email','password1','password2')