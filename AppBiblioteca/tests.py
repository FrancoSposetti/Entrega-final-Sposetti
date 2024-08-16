from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Autor, Libro, Alquiler
from django.urls import reverse
class TestLibraryViews(TestCase):
    def setUp(self):
        # Obtén el modelo de usuario personalizado
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

        # Crea un autor
        self.autor = Autor.objects.create(
            nombre='Gabriel',
            apellido='Garcia Marquez',
            fecha_nacimiento='1927-03-06',
            nacionalidad='Colombiana'
        )

        # Crea un libro
        self.libro = Libro.objects.create(
            titulo='El general en su laberinto',
            autor=self.autor,
            fecha_publicacion='1989-01-01',
            isbn='9780060883287',
            disponible=True
        )

    def test_alquiler_libro(self):
        # Alquilar el libro
        Alquiler.objects.create(libro=self.libro, usuario=self.user)

        # Recarga el libro de la base de datos para verificar su estado
        self.libro.refresh_from_db()

        # Verifica que el libro no está disponible
        self.assertFalse(self.libro.disponible, "El libro debería estar marcado como no disponible después del alquiler.")
    
    def test_devolucion_libro(self):
        # Alquilar el libro primero
        Alquiler.objects.create(libro=self.libro, usuario=self.user)
        # Devolver el libro
        alquiler = Alquiler.objects.get(libro=self.libro, usuario=self.user)
        alquiler.libro.disponible = True
        alquiler.libro.save()

        # Recarga el libro de la base de datos para verificar su estado
        self.libro.refresh_from_db()

        # Verifica que el libro está disponible
        self.assertTrue(self.libro.disponible, "El libro debería estar disponible después de la devolución.")
    def test_busqueda_libro(self):
        # Simula una búsqueda de libro por título
        response = self.client.get(reverse('pagina_inicio'), {'titulo': 'El general en su laberinto'})
        