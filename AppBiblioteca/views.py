from django.shortcuts import render, redirect 
from .models import Autor, Libro, Alquiler
from .forms import AutorForm, LibroForm, AlquilerForm, DevolucionForm, BusquedaLibroForm
from django.contrib import messages

#defino la view de la pagina de inicio
def pagina_inicio(request):
    #variable libro vacia almacenar la busqueda del form
    libros = None
    #creo una instacia del forms 
    form = BusquedaLibroForm()
#compruebo que el metodo sea POST
    if request.method == 'POST':
        #creo una instacia inicindola con los datos enviados por el metodo POST
        form = BusquedaLibroForm(request.POST)
        #compruebo la validez de los datos
        if form.is_valid():
            titulo = form.cleaned_data.get('titulo')
            #compruebo que el titulo no sea una cadena vacia
            if titulo:
                #consulta en la base de datos 
                libros = Libro.objects.filter(titulo__icontains=titulo)
    #renderizo la plantilla html
    return render(request, 'AppBiblioteca/inicio.html', {
        'form': form,
        'libros': libros,
    })
#defino la view de la pagina libros
def listar_libros(request):
    #almaceno en la variable los conjuntos obtenidos en la base de datos
    libros = Libro.objects.all()
    #compruebo que el metodo sea POST
    if request.method == 'POST':
        form = LibroForm(request.POST)
        #compruebo si los datos del form son validos 
        if form.is_valid():
            #guardo los datos 
            form.save()
            #redirecciono al usuario a la pagina de nuevo
            return redirect('listar_libros')
    else:
        form = LibroForm()
        #renderizo en formulario
    return render(request, 'AppBiblioteca/listar_libros.html', {'libros': libros, 'form': form})

def listar_autores(request):
    #almaceno en la variable los conjuntos obtenidos en la base de datos
    autores = Autor.objects.all()
    #compruebo si los datos del form son validos
    if request.method == 'POST':
        form = AutorForm(request.POST)
        #Comprueba si los datos del formulario son válidos
        if form.is_valid():
            # Guardo los datos
            form.save()
            #redirecciono al usuario a la pagina de nuevo
            return redirect('listar_autores')
    else:
        #Si la solicitud no es 'POST', crea un formulario vacío
        form = AutorForm()
    
    #renderizo la plantilla html
    return render(request, 'AppBiblioteca/listar_autores.html', {'autores': autores, 'form': form})

def disponibilidad_y_alquiler(request):
    #Compruebo si el método de la solicitud es 'POST'
    if request.method == 'POST':
        #Compruebo si el formulario enviado es el de alquiler
        if 'alquiler_form' in request.POST:
            #Creo una instancia del formulario AlquilerForm con los datos enviados en la solicitud POST
            alquiler_form = AlquilerForm(request.POST)
            #Compruebo si los datos del formulario son válidos
            if alquiler_form.is_valid():
                #Guardo el nuevo objeto Alquiler sin guardarlo todavía en la base de datos
                alquiler = alquiler_form.save(commit=False)
                #Marco el libro como no disponible
                alquiler.libro.disponible = False
                alquiler.libro.save()  #Guardo los cambios en el libro
                alquiler.save()  #Guardo el alquiler en la base de datos
                #Muestro un mensaje de éxito al usuario
                messages.success(request, f"Libro '{alquiler.libro}' alquilado exitosamente.")
                #Redirecciono al usuario a la pagina de nuevo
                return redirect('disponibilidad_y_alquiler')
            else:
                #Muestro un mensaje de error si el formulario no es válido
                messages.error(request, "Error al alquilar el libro.")
        #Compruebo si el formulario enviado es el de devolución
        elif 'devolucion_form' in request.POST:
            #Creo una instancia del formulario DevolucionForm con los datos enviados en la solicitud POST
            devolucion_form = DevolucionForm(request.POST)
            #Compruebo si los datos del formulario son válidos
            if devolucion_form.is_valid():
                #Obtieno el libro del formulario validado
                libro = devolucion_form.cleaned_data['libro']
                try:
                    #Busco el alquiler activo para el libro seleccionado
                    alquiler = Alquiler.objects.get(libro=libro)
                    #Marco el libro como disponible
                    libro.disponible = True
                    libro.save()  #Guardo los cambios en el libro
                    #Elimino el alquiler registrado
                    alquiler.delete()
                    #Muestro un mensaje de éxito al usuario
                    messages.success(request, "Libro devuelto exitosamente.")
                except Alquiler.DoesNotExist:
                    #Muestro un mensaje de error si no se encuentra un alquiler para el libro seleccionado
                    messages.error(request, "No se encontró un alquiler para el libro seleccionado.")
                #Redirecciono al usuario a la vista 'disponibilidad_y_alquiler'
                return redirect('disponibilidad_y_alquiler')
            else:
                #Muestro un mensaje de error si el formulario no es válido
                messages.error(request, "Error al devolver el libro.")
    else:
        #Si la solicitud no es 'POST', crea formularios vacíos
        alquiler_form = AlquilerForm()
        devolucion_form = DevolucionForm()

    #Obtiene todos los libros de la base de datos
    libros = Libro.objects.all()
    
    #Renderizo la plantilla HTML
    return render(request, 'AppBiblioteca/disponibilidad_y_alquiler.html', {
        'libros': libros,
        'alquiler_form': alquiler_form,
        'devolucion_form': devolucion_form,
    })
