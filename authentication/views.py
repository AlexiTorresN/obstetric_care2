from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout as auth_logout
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
    Vista personalizada de login con detección de rol y redirección inteligente
    """
    template_name = 'authentication/login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """
        Redirigir según el rol del usuario
        """
        user = self.request.user
        
        # Superusuario → Django Admin
        if user.is_superuser:
            logger.info(f'Superusuario {user.username} redirigido a admin')
            return reverse_lazy('admin:index')
        
        # Verificar grupo y redirigir apropiadamente
        if user.groups.filter(name='Administrador').exists():
            return reverse_lazy('authentication:dashboard_admin')
        
        if user.groups.filter(name='Médico').exists():
            return reverse_lazy('authentication:dashboard_medico')
        
        if user.groups.filter(name='Matrona').exists():
            return reverse_lazy('authentication:dashboard_matrona')
        
        if user.groups.filter(name='TENS').exists():
            return reverse_lazy('authentication:dashboard_tens')
        
        # Si no tiene rol definido, enviar a página de inicio
        logger.warning(f'Usuario {user.username} sin rol definido')
        messages.warning(
            self.request, 
            'No tienes un rol asignado. Contacta al administrador.'
        )
        return reverse_lazy('home')
    
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
        username = form.cleaned_data.get('username', 'desconocido')
        logger.warning(f'Login fallido - Usuario: {username} - IP: {self.get_client_ip()}')
        messages.error(self.request, 'Error al iniciar sesión. Verifique sus credenciales.')
        return super().form_invalid(form)
    
    def get_client_ip(self):
        """Obtener IP del cliente"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip
    
    def get_user_role_display(self, user):
        """Obtener nombre del rol para mostrar"""
        if user.is_superuser:
            return "Super Administrador"
        elif user.groups.filter(name='Administrador').exists():
            return "Administrador"
        elif user.groups.filter(name='Médico').exists():
            return "Médico"
        elif user.groups.filter(name='Matrona').exists():
            return "Matrona"
        elif user.groups.filter(name='TENS').exists():
            return "TENS"
        else:
            return "Usuario"


# ============================================
# LOGOUT - Vista que redirige al splash screen
# ============================================
def custom_logout_view(request):
    """
    Vista de logout que cierra sesión y redirige directamente al splash screen
    Sin mostrar página intermedia de Django
    """
    if request.user.is_authenticated:
        username = request.user.username
        logger.info(f'Logout - Usuario: {username}')
        
        # Cerrar sesión
        # auth_logout(request)
        logout(request)
        
        # Mensaje de éxito
        messages.success(request, 'Sesión cerrada correctamente. ¡Hasta pronto!')
    
    # Redirigir directamente al splash screen
    return redirect('home')


# ============================================
# DASHBOARDS POR ROL
# ============================================

@method_decorator(login_required, name='dispatch')
class DashboardAdminView(TemplateView):
    """Dashboard para Administradores"""
    template_name = 'authentication/dashboards/dashboard_admin.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_superuser or 
                request.user.groups.filter(name='Administrador').exists()):
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from gestionApp.models import Persona
        from matronaApp.models import Paciente
        from django.contrib.auth.models import User
        
        context.update({
            'total_usuarios': User.objects.filter(is_active=True).count(),
            'total_personas': Persona.objects.filter(Activo=True).count(),
            'total_pacientes': Paciente.objects.filter(activo=True).count(),
        })
        return context


@method_decorator(login_required, name='dispatch')
class DashboardMedicoView(TemplateView):
    """Dashboard para Médicos"""
    template_name = 'authentication/dashboards/dashboard_medico.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Médico').exists():
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from medicoApp.models import Patologias
        
        context.update({
            'total_patologias': Patologias.objects.filter(estado=True).count(),
            'patologias_alto_riesgo': Patologias.objects.filter(
                nivel_de_riesgo__in=['Alto', 'Critico'],
                estado=True
            ).count(),
        })
        return context


@method_decorator(login_required, name='dispatch')
class DashboardMatronaView(TemplateView):
    """Dashboard para Matronas"""
    template_name = 'authentication/dashboards/dashboard_matrona.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='Matrona').exists():
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from matronaApp.models import FichaObstetrica, IngresoPaciente
        from django.utils import timezone
        
        hoy = timezone.now().date()
        
        context.update({
            'fichas_activas': FichaObstetrica.objects.filter(activa=True).count(),
            'ingresos_hoy': IngresoPaciente.objects.filter(
                fecha_ingreso=hoy
            ).count(),
        })
        return context


@method_decorator(login_required, name='dispatch')
class DashboardTensView(TemplateView):
    """Dashboard para TENS"""
    template_name = 'authentication/dashboards/dashboard_tens.html'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='TENS').exists():
            messages.error(request, 'No tienes permisos para acceder a esta sección.')
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from matronaApp.models import AdministracionMedicamento
        from django.utils import timezone
        
        hoy = timezone.now().date()
        
        context.update({
            'administraciones_hoy': AdministracionMedicamento.objects.filter(
                fecha_hora_administracion__date=hoy
            ).count(),
        })
        return context