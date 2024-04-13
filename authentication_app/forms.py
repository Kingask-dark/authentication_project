# form.py
import re
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser
from django.core.validators import EmailValidator

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'Email'
        }
        validators = {
            'email': EmailValidator(message="Provide valid email")
        }

    def clean_password1(self):
        password = self.cleaned_data.get("password1")
        if not re.match(r'^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+=\-{}[\]:;"\'|,.<>?`~]).{8,}$', password):
            raise forms.ValidationError(
                "Password must contain at least one uppercase letter, one number, and one special character."
            )
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'] = forms.EmailField(label="Email", validators=[EmailValidator(message="Provide valid email")])
        self.fields['password'] = forms.CharField(label="Password", widget=forms.PasswordInput)
