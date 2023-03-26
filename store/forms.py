from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import *

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='UserName', widget=forms.TextInput(attrs={'class': 'lf--input', 'placeholder': 'Username'}))
    fio = forms.CharField(label='FIO', widget=forms.TextInput(attrs={'class': 'lf--input', 'placeholder': 'FIO'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'lf--input', 'placeholder': 'Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'lf--input', 'placeholder': 'Password'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'lf--input', 'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ('username', 'fio', 'email', 'password1', 'password2',)


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'lf--input', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'lf--input', 'placeholder':'Password'}))
