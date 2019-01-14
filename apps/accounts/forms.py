from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Authenticator

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

#For changing things like username, password reset.
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class AuthenticatorCreationForm(forms.ModelForm):
    class Meta:
        model = Authenticator
        fields = ('name',)

class AuthenticatorChangeForm(forms.ModelForm):
    class Meta:
        model = Authenticator
        fields = ('name',)