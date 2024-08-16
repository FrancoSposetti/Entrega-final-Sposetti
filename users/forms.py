
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUser

# Definición de un formulario personalizado para la creación de usuarios.
class CustomUserCreationForm(UserCreationForm):
    # Se añade un campo opcional para que los usuarios suban un avatar.
    avatar = forms.ImageField(required=False)
    # Clase interna Meta para especificar el modelo y los campos del formulario.
    class Meta(UserCreationForm.Meta):
        model = CustomUser  # Especifica que el modelo a utilizar es CustomUser.
        fields = ('username', 'email', 'avatar')  # Campos que se incluirán en el formulario.
        # Además de los campos 'username' y 'email', se incluye 'avatar'.
# Definición de un formulario personalizado para la actualización de la información del usuario.
class CustomUserChangeForm(UserChangeForm):
    # Se añade un campo opcional para cambiar el avatar.
    avatar = forms.ImageField(required=False)
    # Clase interna Meta para especificar el modelo y los campos del formulario.
    class Meta:
        model = CustomUser  # Especifica que el modelo a utilizar es CustomUser.
        fields = ('username', 'email', 'avatar')  # Campos que se pueden actualizar en el formulario.
        # Incluye el campo 'avatar' junto con 'username' y 'email'.
# Definición de un formulario personalizado para el cambio de contraseña.
class CustomPasswordChangeForm(PasswordChangeForm):
    # Campo para la contraseña actual, obligatorio, con un widget para ocultar la entrada.
    old_password = forms.CharField(widget=forms.PasswordInput, required=True)
    # Campo para la nueva contraseña, obligatorio, con un widget para ocultar la entrada.
    new_password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    # Campo para la confirmación de la nueva contraseña, obligatorio, con un widget para ocultar la entrada.
    new_password2 = forms.CharField(widget=forms.PasswordInput, required=True)
