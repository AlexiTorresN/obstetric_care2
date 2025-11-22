"""
Vistas de la aplicación de inicio
"""
from django.shortcuts import render, redirect


def home(request):
    """
    Splash screen / Landing page pública
    Si el usuario ya está autenticado, redirigir a su dashboard correspondiente
    """
    if request.user.is_authenticated:
        # Redirigir según el rol
        if request.user.is_superuser:
            return redirect('admin:index')
        elif request.user.groups.filter(name='Administrador').exists():
            return redirect('authentication:dashboard_admin')
        elif request.user.groups.filter(name='Médico').exists():
            return redirect('authentication:dashboard_medico')
        elif request.user.groups.filter(name='Matrona').exists():
            return redirect('authentication:dashboard_matrona')
        elif request.user.groups.filter(name='TENS').exists():
            return redirect('authentication:dashboard_tens')
    
    # Si no está autenticado, mostrar splash screen
    return render(request, 'inicio/home.html')