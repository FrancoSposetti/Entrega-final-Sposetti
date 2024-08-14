# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField(required=False)  # Agregar el campo para el avatar

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'avatar') 
        # Incluye el campo 'avatar'
class CustomUserChangeForm(UserChangeForm):
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avatar')

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=True)