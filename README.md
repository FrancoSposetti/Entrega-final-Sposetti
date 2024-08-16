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

1. Ve a la sección de autores.
2. Podrás ver una lista de autores.
3. Usa el formulario para añadir un nuevo autor.

### Gestión de Libros

1. Ve a la sección de gestión de libros.
2. Usa el formulario para añadir un nuevo libro.

### Alquiler y Devolución de Libros

1. Ve a la sección de alquiler y devolución de libros.
2. Para alquilar un libro, utiliza el formulario de alquiler. Solo los libros disponibles aparecerán en el listado.
3. Para devolver un libro, utiliza el formulario de devolución. Solo los libros alquilados aparecerán en el listado.
4. Ademas, podras filtar los libros por "disponible" o "no disponible" y podras ver mas informacion de los mismos.

## Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas principales:

- `AppBiblioteca/`: Carpeta que maneja todo lo relacionado con la gestión de libros, autores y alquileres.
  - `models.py`: Definición de los modelos de datos (Autor, Libro, Alquiler).
  - `forms.py`: Definición de los formularios (BusquedaLibroForm, AutorForm, LibroForm, AlquilerForm, DevolucionForm).
  - `views.py`: Definición de las vistas para manejar las peticiones y renderizar las páginas.
  - `templates/AppBiblioteca/`: Plantillas HTML para las vistas de `AppBiblioteca`.
  - `urls.py`: Definición de las rutas específicas para `AppBiblioteca`.

- `users/`: Carpeta que maneja todo lo relacionado con la gestión de usuarios.
  - `models.py`: Definición del modelo de usuario personalizado.
  - `forms.py`: Definición de los formularios para la gestión de usuarios (CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm).
  - `views.py`: Definición de las vistas para el manejo de usuarios (registro, inicio de sesión, actualización de perfil, cambio de contraseña).
  - `templates/users/`: Plantillas HTML para las vistas de `users`.

- `media/`: Carpeta para almacenar archivos cargados por los usuarios, como avatares, portadas y otros documentos.

- `TercerEntrega/`: Carpeta principal del proyecto que contiene la configuración del proyecto Django.
  - `settings.py`: Configuración del proyecto Django.
  - `urls.py`: Definición de las rutas globales del proyecto.
  - `wsgi.py`: Configuración WSGI para el despliegue del proyecto.
  - `__init__.py`: Archivo de inicialización del paquete.



