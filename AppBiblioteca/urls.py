from django.urls import path
from .views import PaginaInicioView, ListarLibrosView, ListarAutoresView, DisponibilidadYAlquilerView, AboutView
#Creo las urls necesarias para poder navegar en las paginas.
urlpatterns = [
    path('', PaginaInicioView.as_view(), name='pagina_inicio'),  
    path('libros/', ListarLibrosView.as_view(), name='listar_libros'),
    path('autores/', ListarAutoresView.as_view(), name='listar_autores'),
    path('disponibilidad_y_alquiler/', DisponibilidadYAlquilerView.as_view(), name='disponibilidad_y_alquiler'),
    path('about/', AboutView.as_view(), name='about'),
]
