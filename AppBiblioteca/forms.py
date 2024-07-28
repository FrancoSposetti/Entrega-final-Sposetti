from django import forms
from .models import Autor, Libro, Alquiler

#Formulario para la busqueda de libros en pagina de inicio
class BusquedaLibroForm(forms.Form):
    titulo = forms.CharField(max_length=100, required=False, label="Buscar libro")

#formulario para agregar autores, con 4 campos por completar en la pagina autores
class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'nacionalidad']
#formulario para agregar libros, con 5 campos para completar en la pagina inicio
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['titulo', 'autor', 'fecha_publicacion', 'isbn', 'disponible']
#formulario para seleccionar un libro y alquilarlo.
class AlquilerForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['libro', 'fecha_alquiler']
    def __init__(self, *args, **kwargs):
        #Llamo al inicializador de la clase base
        super().__init__(*args, **kwargs)
        #Filtro los libros que están disponibles (libros no alquilados)
        libros_disponibles = Libro.objects.filter(disponible=True)
        self.fields['libro'].queryset = libros_disponibles

#formulario para seleccionar un libro ya alquilado y devolverlo.
class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['libro']
#defino un metado inicializar para el formulario
    def __init__(self, *args, **kwargs):
        #llamo al inicilizador de la clase base
        super().__init__(*args, **kwargs)
        # busco los ID de los libros ya alquilados
        libros_alquilados = Alquiler.objects.filter(libro__disponible=False).values_list('libro_id', flat=True)
        # filtro los libros cuyo ID se encuentre en libros_alquilados
        self.fields['libro'].queryset = Libro.objects.filter(id__in=libros_alquilados)