
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    # Sobrescribimos el campo 'username' para hacerlo único y no opcional.
    username = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.email  # Puedes cambiar esto si prefieres mostrar el username u otro campo
