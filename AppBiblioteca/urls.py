from django.urls import path
from .views import pagina_inicio, listar_libros, listar_autores, disponibilidad_y_alquiler
#Creo las urls necesarias para poder navegar en las paginas.
urlpatterns = [
    path('', pagina_inicio, name='pagina_inicio'),  
    path('libros/', listar_libros, name='listar_libros'),
    path('autores/', listar_autores, name='listar_autores'),
    path('disponibilidad_y_alquiler/', disponibilidad_y_alquiler, name='disponibilidad_y_alquiler'),
]
