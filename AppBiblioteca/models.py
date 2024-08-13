from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings 

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    disponible = models.BooleanField(default=True)
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)  # Nuevo campo para la portada

    def __str__(self):
        return self.titulo

class Alquiler(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    fecha_alquiler = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Alquiler de {self.libro.titulo}"

    def save(self, *args, **kwargs):
        is_new_instance = self.pk is None
        super().save(*args, **kwargs)
        if is_new_instance:
            self.libro.disponible = False
            self.libro.save()
        else:
            if self.libro.disponible:
                self.libro.disponible = True
                self.libro.save()
