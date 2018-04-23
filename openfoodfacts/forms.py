from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class QueryForm(forms.Form):
    query = forms.CharField()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text='Requis. Rentrez une adresse email valide.'
        )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class EmailChangeForm(forms.Form):
    """Form used in account template. Aim to change the e-mail of the user."""
    new_email = forms.EmailField(
        label='Nouvel e-mail',
        max_length=254,
        required=True,
        )
