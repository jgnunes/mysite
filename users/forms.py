from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models
from django.core import validators
from django.contrib.auth.models import User

class LogoutForm(forms.Form):
    pass

class LoginForm(forms.Form):
    pass

class RegisterForm(UserCreationForm):
    error_messages = {
        'Erro': (u"As duas senhas digitadas são diferentes"),
    }

    password1 = forms.CharField(label=("Senha"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Confirmar senha"),
                                widget=forms.PasswordInput,
                                help_text=(u"Digite a mesma senha de cima, para verificação"))
    class Meta:
        model = User
        fields = ("username",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['Erro'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user