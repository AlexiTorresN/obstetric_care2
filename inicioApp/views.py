# inicioApp/views.py
from django.shortcuts import render
from gestionApp.models import Persona, Medico, Matrona, Tens, Paciente


def home(request):
    """Vista principal del sistema"""
    
    # Estadísticas básicas
    context = {
        'total_personas': Persona.objects.filter(Activo=True).count(),
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'total_medicos': Medico.objects.filter(Activo=True).count(),
        'total_matronas': Matrona.objects.filter(Activo=True).count(),
        'total_tens': Tens.objects.filter(Activo=True).count(),
    }
    
    return render(request, 'inicio/home.html', context)