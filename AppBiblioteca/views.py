from django.shortcuts import render, redirect, get_object_or_404
from .models import Autor, Libro, Alquiler
from .forms import AutorForm, LibroForm, AlquilerForm, DevolucionForm, BusquedaLibroForm, LibroFilterForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Vista para la página de inicio con un formulario de búsqueda de libros.
class PaginaInicioView(FormView):
    # Plantilla a usar para esta vista.
    template_name = 'AppBiblioteca/inicio.html'
    # Formulario usado en esta vista.
    form_class = BusquedaLibroForm
    # Método llamado cuando el formulario es válido.
    def form_valid(self, form):
        # Obtiene el título del libro del formulario.
        titulo = form.cleaned_data.get('titulo')
        libros = None
        # Si hay un título, busca libros que contengan ese título.
        if titulo:
            libros = Libro.objects.filter(titulo__icontains=titulo)
        # Renderiza la respuesta con el contexto adecuado.
        return self.render_to_response(self.get_context_data(form=form, libros=libros))
# Vista para listar libros y agregar un nuevo libro.
class ListarLibrosView(LoginRequiredMixin, ListView, FormView):
    # Modelo asociado con esta vista.
    model = Libro
    # Plantilla a usar para esta vista.
    template_name = 'AppBiblioteca/listar_libros.html'
    # Formulario usado en esta vista.
    form_class = LibroForm
    # URL de éxito para redireccionar después de una acción exitosa.
    success_url = reverse_lazy('listar_libros')
    # Método para obtener el contexto de la vista.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Incluye la lista de libros en el contexto.
        context['libros'] = self.get_queryset()
        # Incluye el formulario en el contexto.
        context['form'] = self.get_form()
        return context
    # Método para manejar las solicitudes POST.
    def post(self, request, *args, **kwargs):
        # Obtiene el formulario con los datos del POST.
        form = self.get_form()
        # Verifica si el formulario es válido.
        if form.is_valid():
            return self.form_valid(form)
        else:
            # Redirige con un mensaje de error si el formulario no es válido.
            messages.error(self.request, "Los datos ingresados son incorrectos. Por favor, corríjalos e intente nuevamente.")
            return redirect(self.success_url)
    # Método llamado cuando el formulario es válido.
    def form_valid(self, form):
        # Guarda el formulario y redirige a la URL de éxito.
        form.save()
        messages.success(self.request, "Libro guardado exitosamente.")
        return redirect(self.success_url)
# Vista para listar autores y agregar un nuevo autor.
class ListarAutoresView(LoginRequiredMixin, ListView, FormMixin):
    # Modelo asociado con esta vista.
    model = Autor
    # Plantilla a usar para esta vista.
    template_name = 'AppBiblioteca/listar_autores.html'
    # Nombre del contexto para los autores.
    context_object_name = 'autores'
    # Formulario usado en esta vista.
    form_class = AutorForm
    # URL de éxito para redireccionar después de una acción exitosa.
    success_url = reverse_lazy('listar_autores')
    # Método para obtener el contexto de la vista.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Incluye el formulario en el contexto.
        context['form'] = self.get_form()
        return context
    # Método para manejar las solicitudes POST.
    def post(self, request, *args, **kwargs):
        # Obtiene el formulario con los datos del POST.
        form = self.get_form()
        # Verifica si el formulario es válido.
        if form.is_valid():
            return self.form_valid(form)
        else:
            # Redirige con un mensaje de error si el formulario no es válido.
            messages.error(self.request, "Los datos ingresados son incorrectos. Por favor, corríjalos e intente nuevamente.")
            return redirect(self.success_url)
    # Método llamado cuando el formulario es válido.
    def form_valid(self, form):
        # Guarda el formulario y redirige a la URL de éxito.
        form.save()
        messages.success(self.request, "Autor guardado exitosamente.")
        return redirect(self.success_url)
# Vista para gestionar la disponibilidad y alquiler de libros.
class DisponibilidadYAlquilerView(LoginRequiredMixin, TemplateView):
    # Plantilla a usar para esta vista.
    template_name = 'AppBiblioteca/disponibilidad_y_alquiler.html'
    # Método para obtener el contexto de la vista.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene el filtro de disponibilidad del GET request.
        disponibilidad = self.request.GET.get('disponibilidad', '')
        # Filtra los libros según la disponibilidad.
        if disponibilidad == 'disponible':
            context['libros'] = Libro.objects.filter(disponible=True)
        elif disponibilidad == 'no_disponible':
            context['libros'] = Libro.objects.filter(disponible=False)
        else:
            context['libros'] = Libro.objects.all()
        # Obtiene el libro seleccionado si se ha hecho clic en "Ver más".
        libro_id = self.request.GET.get('libro_id')
        if libro_id:
            context['libro_seleccionado'] = get_object_or_404(Libro, id=libro_id)
        # Incluye los formularios de alquiler y devolución en el contexto.
        context['alquiler_form'] = AlquilerForm()
        context['devolucion_form'] = DevolucionForm(current_user=self.request.user)
        context['filter_form'] = LibroFilterForm(initial={'disponibilidad': disponibilidad})
        return context
    # Método para manejar las solicitudes POST.
    def post(self, request, *args, **kwargs):
        # Manejo del formulario de alquiler.
        if 'alquiler_form' in request.POST:
            alquiler_form = AlquilerForm(request.POST)
            if alquiler_form.is_valid():
                alquiler = alquiler_form.save(commit=False)
                alquiler.usuario = request.user
                alquiler.libro.disponible = False
                alquiler.libro.save()
                alquiler.save()
                messages.success(request, f"Libro '{alquiler.libro}' alquilado exitosamente.")
                return redirect('disponibilidad_y_alquiler')
            else:
                messages.error(request, "Error al alquilar el libro.")
        # Manejo del formulario de devolución.
        elif 'devolucion_form' in request.POST:
            devolucion_form = DevolucionForm(request.POST, current_user=request.user)
            if devolucion_form.is_valid():
                libro = devolucion_form.cleaned_data['libro']
                try:
                    alquiler = Alquiler.objects.get(libro=libro, usuario=request.user)
                    libro.disponible = True
                    libro.save()
                    alquiler.delete()
                    messages.success(request, "Libro devuelto exitosamente.")
                except Alquiler.DoesNotExist:
                    messages.error(request, "No se encontró un alquiler para el libro seleccionado o no es el libro alquilado por usted.")
                return redirect('disponibilidad_y_alquiler')
            else:
                messages.error(request, "Error al devolver el libro.")
        # Redibuja la vista con el contexto actual.
        context = self.get_context_data()
        return self.render_to_response(context)
# Vista para la página "Sobre nosotros".
class AboutView(TemplateView):
    # Plantilla a usar para esta vista.
    template_name = 'AppBiblioteca/about.html'
