# authentication/middleware/role_gatekeeper.py
"""
Middleware para control de acceso basado en roles
Restringe el acceso a apps según el grupo del usuario
"""
from django.core.exceptions import PermissionDenied
from django.urls import resolve
from django.shortcuts import redirect
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

# Mapeo de app_name -> Grupo requerido
RUTA_ROLES = {
    "gestion": "Administrador",
    "medico": "Médico",
    "matrona": "Matrona",
    "tens": "TENS",
}

# URLs que no requieren autenticación
EXEMPT_URL_NAMES = {
    "login",
    "logout",
    "password_reset",
    "password_reset_done",
    "password_reset_confirm",
    "password_reset_complete",
    "home",
}


class RoleGatekeeperMiddleware:
    """
    Middleware profesional:
    - Restringe el acceso por app según grupo del usuario
    - Permite rutas públicas
    - Redirige a login si no está autenticado
    - Admin y superuser acceden a todo
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            match = resolve(request.path_info)
        except Exception:
            return self.get_response(request)

        # URLs públicas
        if match.url_name in EXEMPT_URL_NAMES:
            return self.get_response(request)

        app_name = match.app_name

        # Sin app_name → no se restringe
        if not app_name:
            return self.get_response(request)

        # Si la app no tiene regla → acceso libre
        required_role = RUTA_ROLES.get(app_name)
        if not required_role:
            return self.get_response(request)

        # Validación de login
        if not request.user.is_authenticated:
            return redirect(f"{reverse('authentication:login')}?next={request.path}")

        # Súper usuario o Administrador → acceso total
        if request.user.is_superuser or \
           request.user.groups.filter(name="Administrador").exists():
            return self.get_response(request)

        # Verificar rol requerido
        if not request.user.groups.filter(name=required_role).exists():
            logger.warning(
                f"Acceso denegado: user={request.user.username}, "
                f"app={app_name}, required_role={required_role}"
            )
            raise PermissionDenied("No tienes permisos para acceder a esta sección.")

        return self.get_response(request)