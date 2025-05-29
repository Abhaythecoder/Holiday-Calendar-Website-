from django.contrib.auth.models import User
from django import forms
from .models import Login
from django.contrib.auth import authenticate


class Loginform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


def clean(self):
    cleaned_data = super().clean()
    username = cleaned_data.get('username')
    password = cleaned_data.get('password')

    # Authenticate user
    user = authenticate(username=username, password=password)
    if not user:
        raise forms.ValidationError("Invalid username or password")
    return cleaned_data
