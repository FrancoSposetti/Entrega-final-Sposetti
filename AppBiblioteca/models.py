from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings 

# Definición del modelo Autor.
class Autor(models.Model):
    # Campo para el nombre del autor.
    nombre = models.CharField(max_length=100)
    # Campo para el apellido del autor.
    apellido = models.CharField(max_length=100)
    # Campo para la fecha de nacimiento del autor.
    fecha_nacimiento = models.DateField()
    # Campo para la nacionalidad del autor.
    nacionalidad = models.CharField(max_length=100)
    # Método para representar el autor como una cadena.
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
# Definición del modelo Libro.
class Libro(models.Model):
    # Campo para el título del libro.
    titulo = models.CharField(max_length=200)
    # Campo para la relación con el autor (clave foránea).
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE )
    # Campo para la fecha de publicación del libro.
    fecha_publicacion = models.DateField() 
    # Campo para el ISBN del libro (debe ser único).
    isbn = models.CharField(max_length=13, unique=True )
    # Campo para indicar si el libro está disponible.
    disponible = models.BooleanField(default=True) 
    # Campo para la portada del libro (opcional).
    portada = models.ImageField(upload_to='portadas/', null=True, blank=True)
    # Método para representar el libro como una cadena.
    def __str__(self):
        return self.titulo
# Definición del modelo Alquiler.
class Alquiler(models.Model):
    # Campo para la relación con el libro (clave foránea).
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    # Campo para la relación con el usuario que alquila (clave foránea).
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    # Campo para la fecha y hora del alquiler.
    fecha_alquiler = models.DateTimeField(default=timezone.now)
    # Método para representar el alquiler como una cadena.
    def __str__(self):
        return f"Alquiler de {self.libro.titulo}"
    # Método para guardar el alquiler en la base de datos.
    def save(self, *args, **kwargs):
        # Verifica si es una nueva instancia del alquiler (sin PK).
        is_new_instance = self.pk is None
        # Llama al método save de la clase base.
        super().save(*args, **kwargs)
        # Si es una nueva instancia, marca el libro como no disponible.
        if is_new_instance:
            self.libro.disponible = False
            self.libro.save()
        else:
            # Si no es una nueva instancia, marca el libro como disponible si es necesario.
            if self.libro.disponible:
                self.libro.disponible = True
                self.libro.save()
