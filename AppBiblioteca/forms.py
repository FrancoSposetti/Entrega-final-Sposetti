from django import forms
from .models import Autor, Libro, Alquiler
from datetime import date 

# Definicion del Formulario para la busqueda de libros 
class BusquedaLibroForm(forms.Form):
    titulo = forms.CharField(max_length=100,  required=False, label="Buscar libro")
# Definición del formulario para el modelo Autor
class AutorForm(forms.ModelForm):
    class Meta:
        # Especifica el modelo con el que el formulario está vinculado (Autor)
        model = Autor 
        # Define qué campos del modelo Autor estarán disponibles en el formulario
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'nacionalidad']  
    # Validación del campo 'fecha_nacimiento'
    def clean_fecha_nacimiento(self):
        # Obtiene el valor del campo 'fecha_nacimiento' del formulario validados
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')  
        # Compara la fecha de nacimiento ingresada con la fecha actual
        if fecha_nacimiento > date.today():
            # Si la fecha de nacimiento es mayor que la fecha actual (es decir, en el futuro), se genera un error
            raise forms.ValidationError("La fecha de nacimiento no puede ser en el futuro.")
        # Si la fecha es válida (no está en el futuro), se devuelve la fecha tal como se ingresó
        return fecha_nacimiento  
# Definición del formulario para el modelo Libro
class LibroForm(forms.ModelForm):
    class Meta:
        # Especifica el modelo con el que el formulario está vinculado (Libro)
        model = Libro
        # Define qué campos del modelo Libro estarán disponibles en el formulario
        fields = ['titulo', 'autor', 'fecha_publicacion', 'isbn', 'disponible', 'portada']
    # Validación del campo 'fecha_publicacion'
    def clean_fecha_publicacion(self):
        # Obtiene el valor del campo 'fecha_publicacion' del formulario validados
        fecha_publicacion = self.cleaned_data.get('fecha_publicacion')
        # Compara la fecha de publicación ingresada con la fecha actual
        if fecha_publicacion > date.today():
            # Si la fecha de publicación es mayor que la fecha actual (es decir, en el futuro), se genera un error
            raise forms.ValidationError("La fecha de publicación no puede ser en el futuro.")
        # Si la fecha es válida (no está en el futuro), se devuelve la fecha tal como se ingresó
        return fecha_publicacion
# Formulario para seleccionar un libro y alquilarlo
class AlquilerForm(forms.ModelForm):
    class Meta:
        # Especifica el modelo con el que el formulario está vinculado (Alquiler)
        model = Alquiler
        # Define qué campos del modelo Alquiler estarán disponibles en el formulario
        fields = ['libro']
    # Método constructor del formulario, permite personalizar el formulario en su creación
    def __init__(self, *args, **kwargs):
        # Extrae el usuario actual de los argumentos pasados al formulario. Esto se hace para poder asociar el alquiler al usuario que está alquilando el libro.
        self.current_user = kwargs.pop('current_user', None)
        # Llama al constructor de la clase padre para inicializar el formulario
        super().__init__(*args, **kwargs)
        # Filtra los libros para que solo se muestren aquellos que están disponibles
        self.fields['libro'].queryset = Libro.objects.filter(disponible=True)
    # Método para guardar el formulario y realizar acciones adicionales antes del guardado
    def save(self, commit=True):
        # Llama al método save de la clase padre, pero no guarda en la base de datos todavía (commit=False)
        alquiler = super().save(commit=False)
        # Asigna el usuario actual al alquiler antes de guardarlo
        alquiler.usuario = self.current_user
        # Si commit es True, guarda el objeto Alquiler en la base de datos
        if commit:
            alquiler.save()
        # Devuelve el objeto Alquiler
        return alquiler
# Formulario para seleccionar un libro ya alquilado y devolverlo
class DevolucionForm(forms.ModelForm):
    class Meta:
        # Especifica el modelo con el que el formulario está vinculado (Alquiler)
        model = Alquiler
        # Define qué campos del modelo Alquiler estarán disponibles en el formulario
        fields = ['libro']
    # Método constructor del formulario, permite personalizar el formulario en su creación
    def __init__(self, *args, **kwargs):
        # Extrae el usuario actual de los argumentos pasados al formulario
        self.current_user = kwargs.pop('current_user', None)
        # Llama al constructor de la clase padre para inicializar el formulario
        super().__init__(*args, **kwargs)
        # Verifica si se ha proporcionado un usuario actual. Si es así, procede a filtrar los libros.
        if self.current_user:
            # Filtra el campo libro para que solo se muestren los libros que han sido alquilados por el usuario actual y que aún no han sido devueltos (disponible=False).
            self.fields['libro'].queryset = Libro.objects.filter(
                alquiler__usuario=self.current_user,  
                alquiler__libro__disponible=False  
            ).distinct()
    # Validación del campo 'libro'
    def clean_libro(self):
        # Obtiene el valor del campo 'libro' del formulario validados
        libro = self.cleaned_data['libro']
        # Verifica si el usuario actual tiene un alquiler activo para el libro seleccionado
        if not Alquiler.objects.filter(libro=libro, usuario=self.current_user).exists():
            # Si no se encuentra un alquiler activo para ese libro, se lanza una excepción ValidationError
            raise forms.ValidationError("No tienes un alquiler activo para este libro.")
        # Si la validación es correcta, se devuelve el libro tal como se ingresó
        return libro
# Definición del formulario para filtrar libros según su disponibilidad.
class LibroFilterForm(forms.Form):
    # Constantes para los estados de disponibilidad.
    DISPONIBLE = 'disponible'  
    NO_DISPONIBLE = 'no_disponible'  
    # Lista de opciones para el campo de disponibilidad.
    DISPONIBILIDAD_CHOICES = [
        (DISPONIBLE, 'Disponibles'),  
        (NO_DISPONIBLE, 'No Disponibles'),  
        ('', 'Todos')  
    ]
    # Campo de formulario para seleccionar el filtro de disponibilidad.
    disponibilidad = forms.ChoiceField(
        # Se asignan las opciones definidas anteriormente.
        choices=DISPONIBILIDAD_CHOICES,
        # El campo no es obligatorio, permitiendo que se muestren todos los libros si no se selecciona ninguna opción.
        required=False,
        # Etiqueta que se mostrará junto al campo en el formulario.
        label='Filtrar por Disponibilidad'
    )

