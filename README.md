#AppBiblioteca

AppBiblioteca es una aplicación web desarrollada con Django para la gestión de una biblioteca. Permite buscar libros, gestionar autores y manejar el alquiler y la devolución de libros.

## Contenido del Proyecto

El proyecto incluye las siguientes funcionalidades:
1. Búsqueda de libros: Un formulario para buscar libros por título.
2. Gestión de autores: Listar, añadir y editar autores.
3. Gestión de libros: Listar, añadir y editar libros.
4. Alquiler y devolución de libros: Formularios para alquilar y devolver libros.

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes componentes:
- Python 
- Django 
- pip (el gestor de paquetes de Python)

## Instalación

Sigue estos pasos para instalar y configurar el proyecto en tu entorno local:

1. Realiza las migraciones de la base de datos:

    python manage.py migrate

2. Crea un superusuario para acceder al panel de administración:

    python manage.py createsuperuser

3. Inicia el servidor de desarrollo:

    python manage.py runserver

8. Accede a la aplicación en tu navegador:

    Abre [http://127.0.0.1:8000]

## Uso de la Aplicación

### Búsqueda de Libros

1. En la página de inicio, utiliza el formulario de búsqueda para buscar libros por título.
2. Introduce el título (o parte del título) en el campo de búsqueda y presiona "Buscar libro".

### Gestión de Autores

1. Ve a la sección de gestión de autores.
2. Podrás ver una lista de autores.
3. Usa el formulario para añadir un nuevo autor.

### Gestión de Libros

1. Ve a la sección de gestión de libros.
2. Usa el formulario para añadir un nuevo libro.

### Alquiler y Devolución de Libros

1. Ve a la sección de alquiler y devolución de libros.
2. Para alquilar un libro, utiliza el formulario de alquiler. Solo los libros disponibles aparecerán en el listado.
3. Para devolver un libro, utiliza el formulario de devolución. Solo los libros alquilados aparecerán en el listado.

## Estructura del Proyecto

- `AppBiblioteca/`: Carpeta principal del proyecto.
- `AppBiblioteca/models.py`: Definición de los modelos de datos (Autor, Libro, Alquiler).
- `AppBiblioteca/forms.py`: Definición de los formularios (BusquedaLibroForm, AutorForm, LibroForm, AlquilerForm, DevolucionForm).
- `AppBiblioteca/views.py`: Definición de las vistas para manejar las peticiones y renderizar las páginas.
- `AppBiblioteca/templates/AppBiblioteca/`: Plantillas HTML para las vistas.
- `AppBiblioteca/urls.py`: Definición de las rutas de la aplicación.


