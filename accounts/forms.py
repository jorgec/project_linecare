from django import forms
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import Account


class LoginForm(AuthenticationForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = (
            'email', 'password'
        )


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = (
            'email',
            'password',
        )

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )