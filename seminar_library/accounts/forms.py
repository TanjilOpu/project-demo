from django import forms
from django.conf import settings
from .models import User


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email', '').lower()
        domain = email.split('@')[-1]
        allowed = getattr(settings, 'ALLOWED_EMAIL_DOMAIN', 'mbstu.ac.bd')
        if domain != allowed:
            raise forms.ValidationError(
                f'Only @{allowed} email addresses are allowed to register.'
            )
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
