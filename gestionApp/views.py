# gestionApp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .forms.Gestion_form import PersonaForm, PacienteForm, MedicoForm, MatronaForm, TensForm
from .models import Persona, Medico, Matrona, Tens
from matronaApp.models import Paciente
from datetime import datetime


# ============================================
# VISTAS DE LISTA Y DETALLE
# ============================================

class PersonaListView(ListView):
    """Lista de todas las personas registradas"""
    model = Persona
    template_name = 'Gestion/Data/persona_list.html'
    context_object_name = 'personas'
    
    def get_queryset(self):
        return Persona.objects.filter(Activo=True).order_by('-id')


class PersonaDetailView(DetailView):
    """Detalle de una persona específica"""
    model = Persona
    template_name = 'Gestion/Data/persona_detail.html'
    context_object_name = 'persona'


# ============================================
# FORMULARIOS DE REGISTRO
# ============================================

def agregar_persona(request):
    """Registrar una nueva persona (datos básicos)"""
    if request.method == 'POST':
        form = PersonaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Persona registrada correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PersonaForm()
    
    return render(request, 'Gestion/Formularios/registrar_persona.html', {'form': form})


def agregar_paciente(request):
    """Registrar un paciente (vinculado a una persona existente)"""
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente registrado correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = PacienteForm()
    
    return render(request, 'Gestion/Formularios/paciente_form.html', {'form': form})


def agregar_medico(request):
    """Registrar un médico (vinculado a una persona existente)"""
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Médico registrado correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = MedicoForm()
    
    return render(request, 'Gestion/Formularios/registrar_medico.html', {'form': form})


def agregar_matrona(request):
    """Registrar una matrona (vinculada a una persona existente)"""
    if request.method == 'POST':
        form = MatronaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Matrona registrada correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = MatronaForm()
    
    return render(request, 'Gestion/Formularios/registrar_matrona.html', {'form': form})


def agregar_tens(request):
    """Registrar un TENS (vinculado a una persona existente)"""
    if request.method == 'POST':
        form = TensForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "TENS registrado correctamente.")
            return redirect('home')
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = TensForm()
    
    return render(request, 'Gestion/Formularios/registrar_tens.html', {'form': form})


# ============================================
# API REST (AJAX)
# ============================================

def buscar_persona_api(request):
    """Buscar persona por RUT vía AJAX (retorna JSON)"""
    rut = request.GET.get('rut', '').strip()
    
    if not rut:
        return JsonResponse({'encontrado': False, 'mensaje': 'RUT no proporcionado'})
    
    try:
        from utilidad.rut_validator import normalizar_rut
        rut_normalizado = normalizar_rut(rut)
        
        persona = Persona.objects.filter(Rut=rut_normalizado, Activo=True).first()
        
        if persona:
            return JsonResponse({
                'encontrado': True,
                'persona': {
                    'id': persona.id,
                    'rut': persona.Rut,
                    'nombre': persona.Nombre,
                    'apellido': persona.Apellido,
                    'nombre_completo': f"{persona.Nombre} {persona.Apellido}",
                    'sexo': persona.Sexo,
                    'fecha_nacimiento': persona.Fecha_nacimiento.strftime('%d/%m/%Y'),
                    'telefono': persona.Telefono or 'No registrado',
                    'email': persona.Email or 'No registrado',
                    'direccion': persona.Direccion or 'No registrada',
                }
            })
        else:
            return JsonResponse({
                'encontrado': False,
                'mensaje': 'No se encontró una persona con ese RUT'
            })
    
    except Exception as e:
        return JsonResponse({
            'encontrado': False,
            'mensaje': f'Error al buscar: {str(e)}'
        }, status=400)


# ============================================
# GESTIÓN DE ROLES
# ============================================

def gestionar_roles_persona(request, pk):
    """Vista para gestionar los roles de una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    # Verificar roles actuales
    roles_actuales = {
        'es_paciente': hasattr(persona, 'paciente'),
        'es_medico': hasattr(persona, 'medico'),
        'es_matrona': hasattr(persona, 'matrona'),
        'es_tens': hasattr(persona, 'tens'),
    }
    
    context = {
        'persona': persona,
        'roles': roles_actuales,
    }
    
    return render(request, 'Gestion/Formularios/gestionar_roles.html', context)


def asignar_rol_paciente(request, pk):
    """Asignar rol de Paciente a una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    # Verificar si ya es paciente
    if hasattr(persona, 'paciente'):
        messages.warning(request, "⚠️ Esta persona ya tiene el rol de Paciente.")
        return redirect('gestion:gestionar_roles', pk=pk)
    
    # Crear rol de paciente
    try:
        Paciente.objects.create(
            persona=persona,
            activo=True
        )
        messages.success(request, "✅ Rol de Paciente asignado correctamente.")
    except Exception as e:
        messages.error(request, f"❌ Error al asignar rol: {str(e)}")
    
    return redirect('gestion:gestionar_roles', pk=pk)


def asignar_rol_medico(request, pk):
    """Asignar rol de Médico a una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if hasattr(persona, 'medico'):
        messages.warning(request, "⚠️ Esta persona ya tiene el rol de Médico.")
        return redirect('gestion:gestionar_roles', pk=pk)
    
    # Formulario para datos del médico
    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            medico = form.save(commit=False)
            medico.persona = persona
            medico.save()
            messages.success(request, "✅ Rol de Médico asignado correctamente.")
            return redirect('gestion:gestionar_roles', pk=pk)
    else:
        form = MedicoForm(initial={'persona': persona})
    
    return render(request, 'Gestion/Formularios/asignar_rol_medico.html', {
        'form': form,
        'persona': persona
    })


def asignar_rol_matrona(request, pk):
    """Asignar rol de Matrona a una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if hasattr(persona, 'matrona'):
        messages.warning(request, "⚠️ Esta persona ya tiene el rol de Matrona.")
        return redirect('gestion:gestionar_roles', pk=pk)
    
    if request.method == 'POST':
        form = MatronaForm(request.POST)
        if form.is_valid():
            matrona = form.save(commit=False)
            matrona.persona = persona
            matrona.save()
            messages.success(request, "✅ Rol de Matrona asignado correctamente.")
            return redirect('gestion:gestionar_roles', pk=pk)
    else:
        form = MatronaForm(initial={'persona': persona})
    
    return render(request, 'Gestion/Formularios/asignar_rol_matrona.html', {
        'form': form,
        'persona': persona
    })


def asignar_rol_tens(request, pk):
    """Asignar rol de TENS a una persona"""
    persona = get_object_or_404(Persona, pk=pk, Activo=True)
    
    if hasattr(persona, 'tens'):
        messages.warning(request, "⚠️ Esta persona ya tiene el rol de TENS.")
        return redirect('gestion:gestionar_roles', pk=pk)
    
    if request.method == 'POST':
        form = TensForm(request.POST)
        if form.is_valid():
            tens = form.save(commit=False)
            tens.persona = persona
            tens.save()
            messages.success(request, "✅ Rol de TENS asignado correctamente.")
            return redirect('gestion:gestionar_roles', pk=pk)
    else:
        form = TensForm(initial={'persona': persona})
    
    return render(request, 'Gestion/Formularios/asignar_rol_tens.html', {
        'form': form,
        'persona': persona
    })


# ============================================
# DASHBOARD ADMINISTRATIVO
# ============================================

def dashboard_admin(request):
    """
    Vista principal del dashboard administrativo.
    Muestra estadísticas generales y accesos rápidos.
    """
    
    # Contar todos los roles activos
    total_medicos = Medico.objects.filter(Activo=True).count()
    total_matronas = Matrona.objects.filter(Activo=True).count()
    total_tens = Tens.objects.filter(Activo=True).count()
    total_pacientes = Paciente.objects.filter(activo=True).count()
    
    # Total de usuarios en el sistema
    total_usuarios = total_medicos + total_matronas + total_tens + total_pacientes
    
    # Total de personas registradas
    total_personas = Persona.objects.filter(Activo=True).count()
    
    # Contexto para el template
    context = {
        'total_medicos': total_medicos,
        'total_matronas': total_matronas,
        'total_tens': total_tens,
        'total_pacientes': total_pacientes,
        'total_usuarios': total_usuarios,
        'total_personas': total_personas,
        'fecha_actual': datetime.now().strftime('%d/%m/%Y'),
    }
    
    return render(request, 'Gestion/dashboard_admin.html', context)