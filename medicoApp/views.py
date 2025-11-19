# medicoApp/views.py
"""
Vistas para el módulo de Médico
Gestión del catálogo de patologías obstétricas
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from medicoApp.models import Patologias
# cargamos los decoradores para validar los accesos
from core.decorators import role_required


# ============================================
# VISTA PRINCIPAL DEL MÓDULO MÉDICO
# ============================================
@role_required("Médico") # Llamada al decorador para validar el acceso va de la mani con app_name
def menu_medico(request):
    """Vista principal del módulo Médico"""
    context = {
        'total_patologias': Patologias.objects.count(),
        'patologias_activas': Patologias.objects.filter(estado='Activo').count(),
        'patologias_inactivas': Patologias.objects.filter(estado='Inactivo').count(),
        'patologias_alto_riesgo': Patologias.objects.filter(
            nivel_de_riesgo__in=['Alto', 'Crítico'],
            estado='Activo'
        ).count(),
    }
    return render(request, 'Medico/menu_medico.html', context)


# ============================================
# GESTIÓN DE PATOLOGÍAS (SIMPLIFICADA)
# ============================================

def listar_patologias(request):
    """
    Listar todas las patologías con filtros
    El médico solo activa/desactiva las que usará el hospital
    """
    patologias = Patologias.objects.all().order_by('nivel_de_riesgo', 'nombre')
    
    # Filtros
    busqueda = request.GET.get('busqueda', '').strip()
    estado = request.GET.get('estado', '')
    nivel_riesgo = request.GET.get('nivel_riesgo', '')
    
    if busqueda:
        patologias = patologias.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo_cie_10__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )
    
    if estado:
        patologias = patologias.filter(estado=estado)
    
    if nivel_riesgo:
        patologias = patologias.filter(nivel_de_riesgo=nivel_riesgo)
    
    # Contar cuántas fichas usan cada patología
    patologias = patologias.annotate(
        num_fichas=Count('fichas_con_patologia')
    )
    
    context = {
        'patologias': patologias,
        'busqueda': busqueda,
        'estado': estado,
        'nivel_riesgo': nivel_riesgo,
    }
    
    return render(request, 'Medico/Data/Patologia_listar.html', context)


def detalle_patologia(request, pk):
    """Ver el detalle completo de una patología"""
    patologia = get_object_or_404(Patologias, pk=pk)
    
    # Contar en cuántas fichas se usa
    fichas_usando = patologia.fichas_con_patologia.filter(activa=True).count()
    
    context = {
        'patologia': patologia,
        'fichas_usando': fichas_usando,
    }
    
    return render(request, 'Medico/Data/Patologia_detalle.html', context)


def toggle_patologia(request, pk):
    """
    Activar/Desactivar una patología
    """
    patologia = get_object_or_404(Patologias, pk=pk)
    
    if request.method == 'POST':
        if patologia.estado == 'Activo':
            patologia.estado = 'Inactivo'
            mensaje = f"❌ Patología '{patologia.nombre}' desactivada. Ya no estará disponible para nuevas fichas."
        else:
            patologia.estado = 'Activo'
            mensaje = f"✅ Patología '{patologia.nombre}' activada. Ahora está disponible para asignar a pacientes."
        
        patologia.save()
        messages.success(request, mensaje)
        return redirect('medico:listar_patologias')
    
    return render(request, 'Medico/Formularios/Patologias_toggle.html', {
        'patologia': patologia
    })


# ============================================
# FUNCIONES DEPRECADAS (Ya no se usan)
# ============================================

def registrar_patologia(request):
    """
    DEPRECADA: Ahora las patologías vienen predefinidas
    Redirigir al listado
    """
    messages.info(
        request,
        "ℹ️ Las patologías vienen predefinidas en el sistema. "
        "Solo debe activar las que usará el hospital."
    )
    return redirect('medico:listar_patologias')


def editar_patologia(request, pk):
    """
    DEPRECADA: Ya no se editan patologías, solo se activan/desactivan
    """
    messages.info(
        request,
        "ℹ️ Las patologías tienen información predefinida y no se pueden editar. "
        "Solo puede activarlas o desactivarlas."
    )
    return redirect('medico:detalle_patologia', pk=pk)

# medicoApp/views.py

# ... (código existente de patologías)

# ============================================
# CONSULTA DE HISTORIAL CLÍNICO
# ============================================

def buscar_paciente_medico(request):
    """
    Buscar paciente por RUT o nombre para consultar historial clínico
    Reutiliza la misma lógica de búsqueda de otros módulos
    """
    query = request.GET.get('q', '').strip()
    pacientes = []
    
    if query:
        from gestionApp.models import Paciente
        from django.db.models import Q, Count
        
        pacientes = Paciente.objects.filter(
            Q(activo=True)
        ).filter(
            Q(persona__Rut__icontains=query) |
            Q(persona__Nombre__icontains=query) |
            Q(persona__Apellido_Paterno__icontains=query) |
            Q(persona__Apellido_Materno__icontains=query)
        ).select_related('persona').annotate(
            num_fichas=Count('fichas_obstetricas')
        )
    
    return render(request, 'Medico/Data/buscar_paciente.html', {
        'pacientes': pacientes,
        'query': query
    })


def ver_historial_clinico(request, paciente_pk):
    """
    Ver el historial clínico completo de un paciente
    Muestra todas las fichas obstétricas con sus detalles
    """
    from gestionApp.models import Paciente
    from matronaApp.models import FichaObstetrica
    from django.db.models import Prefetch, Count
    
    paciente = get_object_or_404(
        Paciente.objects.select_related('persona'),
        pk=paciente_pk,
        activo=True
    )
    
    # Obtener todas las fichas con información relacionada
    fichas = FichaObstetrica.objects.filter(
        paciente=paciente
    ).select_related(
        'matrona_responsable__persona'
    ).prefetch_related(
        'patologias',
        'medicamentos'
    ).annotate(
        num_medicamentos=Count('medicamentos', filter=Q(medicamentos__activo=True)),
        num_patologias=Count('patologias')
    ).order_by('-fecha_creacion')
    
    return render(request, 'Medico/Data/historial_clinico.html', {
        'paciente': paciente,
        'fichas': fichas,
        'total_fichas': fichas.count()
    })