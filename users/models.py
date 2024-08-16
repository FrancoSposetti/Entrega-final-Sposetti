
from django.contrib.auth.models import AbstractUser
from django.db import models

# Define un modelo de usuario 
class CustomUser(AbstractUser):
    # Campo de email único.
    email = models.EmailField(unique=True)
    # Campo de nombre de usuario único, con máximo 150 caracteres.
    username = models.CharField(max_length=150, unique=True)
    # Campo opcional de imagen de avatar.
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    # Devuelve el email como representación en cadena.
    def __str__(self):
        return self.email
