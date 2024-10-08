# users/urls.py
from django.urls import path
from .views import SignUpView, CustomLoginView, CustomLogoutView, ProfileUpdateView, CustomPasswordChangeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]
