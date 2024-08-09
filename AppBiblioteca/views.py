from django.shortcuts import render, redirect 
from .models import Autor, Libro, Alquiler
from .forms import AutorForm, LibroForm, AlquilerForm, DevolucionForm, BusquedaLibroForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class PaginaInicioView(FormView):
    template_name = 'AppBiblioteca/inicio.html'
    form_class = BusquedaLibroForm

    def form_valid(self, form):
        titulo = form.cleaned_data.get('titulo')
        libros = None
        if titulo:
            libros = Libro.objects.filter(titulo__icontains=titulo)
        return self.render_to_response(self.get_context_data(form=form, libros=libros))

class ListarLibrosView(LoginRequiredMixin,ListView, FormView):
    model = Libro
    template_name = 'AppBiblioteca/listar_libros.html'
    form_class = LibroForm
    success_url = reverse_lazy('listar_libros')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libros'] = self.get_queryset()
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

class ListarAutoresView(LoginRequiredMixin,ListView, FormView):
    model = Autor
    template_name = 'AppBiblioteca/listar_autores.html'
    form_class = AutorForm
    success_url = reverse_lazy('listar_autores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['autores'] = self.get_queryset()
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)

class DisponibilidadYAlquilerView(LoginRequiredMixin, TemplateView):
    template_name = 'AppBiblioteca/disponibilidad_y_alquiler.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['libros'] = Libro.objects.all()
        context['alquiler_form'] = AlquilerForm()
        context['devolucion_form'] = DevolucionForm(current_user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        if 'alquiler_form' in request.POST:
            alquiler_form = AlquilerForm(request.POST)
            if alquiler_form.is_valid():
                alquiler = alquiler_form.save(commit=False)
                alquiler.usuario = request.user  # Asigna el usuario actual
                alquiler.libro.disponible = False
                alquiler.libro.save()
                alquiler.save()
                messages.success(request, f"Libro '{alquiler.libro}' alquilado exitosamente.")
                return redirect('disponibilidad_y_alquiler')
            else:
                messages.error(request, "Error al alquilar el libro.")
        
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
        
        context = self.get_context_data()
        return self.render_to_response(context)