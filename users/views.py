from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from .models import CustomUser

# Vista para el registro de usuarios.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirige a la página de login tras el registro exitoso.
    template_name = 'users/signup.html'
    # Procesa el formulario si es válido.
    def form_valid(self, form):
        response = super().form_valid(form)
        # Guarda el avatar si el usuario sube uno durante el registro.
        if self.request.FILES.get('avatar'):
            self.object.avatar = self.request.FILES['avatar']
            self.object.save()
        return response
# Vista personalizada de inicio de sesión.
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
# Vista personalizada de cierre de sesión.
class CustomLogoutView(LogoutView):
    template_name = 'users/logged_out.html'
# Vista para actualizar el perfil del usuario, requiere que el usuario esté autenticado.
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('profile')  # Redirige al perfil tras la actualización.
    # Retorna el usuario actual para que se actualice su perfil.
    def get_object(self):
        return self.request.user
# Vista para cambiar la contraseña, requiere que el usuario esté autenticado.
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('profile')  # Redirige al perfil tras cambiar la contraseña.
