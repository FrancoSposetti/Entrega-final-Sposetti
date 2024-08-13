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
        fields = ['titulo', 'autor', 'fecha_publicacion', 'isbn', 'disponible', 'portada']  # Agregar 'portada' a los campos
#formulario para seleccionar un libro y alquilarlo.
class AlquilerForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['libro']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        # Filtrar libros disponibles
        self.fields['libro'].queryset = Libro.objects.filter(disponible=True)

    def save(self, commit=True):
        alquiler = super().save(commit=False)
        alquiler.usuario = self.current_user
        if commit:
            alquiler.save()
        return alquiler

#formulario para seleccionar un libro ya alquilado y devolverlo.
class DevolucionForm(forms.ModelForm):
    class Meta:
        model = Alquiler
        fields = ['libro']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if self.current_user:
            # Filtra los libros alquilados por el usuario actual
            self.fields['libro'].queryset = Libro.objects.filter(
                alquiler__usuario=self.current_user,
                alquiler__libro__disponible=False
            ).distinct()

    def clean_libro(self):
        libro = self.cleaned_data['libro']
        if not Alquiler.objects.filter(libro=libro, usuario=self.current_user).exists():
            raise forms.ValidationError("No tienes un alquiler activo para este libro.")
        return libro
    
class LibroFilterForm(forms.Form):
    DISPONIBLE = 'disponible'
    NO_DISPONIBLE = 'no_disponible'
    
    DISPONIBILIDAD_CHOICES = [
        (DISPONIBLE, 'Disponibles'),
        (NO_DISPONIBLE, 'No Disponibles'),
        ('', 'Todos')  # Para mostrar todos los libros si no se selecciona ningún filtro
    ]
    
    disponibilidad = forms.ChoiceField(
        choices=DISPONIBILIDAD_CHOICES,
        required=False,
        label='Filtrar por Disponibilidad'
    )
