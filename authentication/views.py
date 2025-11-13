from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomLoginForm
import logging

logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    """
    Vista personalizada de login con detección de rol
    """
    template_name = 'authentication/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """
        Redirigir según el rol del usuario
        """
        user = self.request.user
        
        # Verificar rol y redirigir apropiadamente
        if user.is_superuser:
            return reverse_lazy('admin:index')
        
        # Verificar si tiene perfil médico
        if hasattr(user, 'medico'):
            return reverse_lazy('medico:dashboard')
        
        # Verificar si tiene perfil matrona
        if hasattr(user, 'matrona'):
            return reverse_lazy('matrona:dashboard')
        
        # Verificar si tiene perfil TENS
        if hasattr(user, 'tens'):
            return reverse_lazy('tens:dashboard')
        
        # Por defecto, ir al dashboard general
        return reverse_lazy('inicio:dashboard')
    
    def form_valid(self, form):
        """
        Cuando el login es exitoso
        """
        remember_me = form.cleaned_data.get('remember_me')
        
        if not remember_me:
            # Sesión expira al cerrar el navegador
            self.request.session.set_expiry(0)
        else:
            # Sesión dura 30 días
            self.request.session.set_expiry(2592000)
        
        user = form.get_user()
        login(self.request, user)
        
        # Log de auditoría
        logger.info(f'Login exitoso - Usuario: {user.username} - IP: {self.get_client_ip()}')
        
        # Mensaje de bienvenida con rol
        rol = self.get_user_role_display(user)
        messages.success(
            self.request, 
            f'¡Bienvenido {user.get_full_name() or user.username}! ({rol})'
        )
        
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """
        Cuando el login falla
        """
        # Log de auditoría
        username = form.cleaned_data.get('username', 'desconocido')
        logger.warning(f'Login fallido - Usuario: {username} - IP: {self.get_client_ip()}')
        
        messages.error(self.request, 'Error al iniciar sesión. Verifique sus credenciales.')
        return super().form_invalid(form)
    
    def get_client_ip(self):
        """
        Obtener IP del cliente
        """
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    def get_user_role_display(self, user):
        """
        Obtener nombre del rol para mostrar
        """
        if user.is_superuser:
            return "Administrador"
        elif hasattr(user, 'medico'):
            return "Médico"
        elif hasattr(user, 'matrona'):
            return "Matrona"
        elif hasattr(user, 'tens'):
            return "TENS"
        else:
            return "Usuario"

class CustomLogoutView(LogoutView):
    """
    Vista personalizada de logout
    """
    next_page = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logger.info(f'Logout - Usuario: {request.user.username}')
            messages.info(request, 'Ha cerrado sesión exitosamente.')
        return super().dispatch(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """
    Dashboard principal después del login
    """
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Determinar rol y permisos
        context['user_role'] = self.get_user_role(user)
        context['user_permissions'] = self.get_user_permissions(user)
        
        return context
    
    def get_user_role(self, user):
        if user.is_superuser:
            return 'admin'
        elif hasattr(user, 'medico'):
            return 'medico'
        elif hasattr(user, 'matrona'):
            return 'matrona'
        elif hasattr(user, 'tens'):
            return 'tens'
        return 'usuario'
    
    def get_user_permissions(self, user):
        # Retornar permisos según el rol
        permissions = {
            'admin': ['all'],
            'medico': ['view_all', 'edit_medical', 'prescribe'],
            'matrona': ['view_patients', 'register_birth', 'prescribe_basic'],
            'tens': ['view_assigned', 'administer_meds', 'vital_signs']
        }
        role = self.get_user_role(user)
        return permissions.get(role, [])