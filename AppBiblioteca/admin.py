from django.contrib import admin
from .models import Libro, Autor, Alquiler
# registre mis models en la parte de admin
admin.site.register(Libro)
admin.site.register(Autor)
admin.site.register(Alquiler)