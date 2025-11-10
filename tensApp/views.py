from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count, Prefetch
from django.utils import timezone

from gestionApp.models import Tens, Persona, Paciente
from matronaApp.models import (
    FichaObstetrica, MedicamentoFicha, AdministracionMedicamento, IngresoPaciente )
from tensApp.forms.administracion_forms import AdministracionMedicamentoForm
# from gestionApp.forms.tens_forms import BuscarPacienteForm, RegistroTensForm  # ❌ COMENTAR ESTA LÍNEA
from tensApp.models import  RegistroTens

# de registro de tratamientos
from tensApp.models import Tratamiento_aplicado
# from gestionApp.forms.tens_forms import FormularioTratamientoAplicado  # ❌ COMENTAR ESTA LÍNEA
from tensApp.models import Tratamiento_aplicado
from gestionApp.models import Paciente
from matronaApp.models import FichaObstetrica,MedicamentoFicha, AdministracionMedicamento
# ============================================
# MENÚ PRINCIPAL TENS
# ============================================

def menu_tens(request):
    """Menú principal del módulo TENS"""
    
    # Obtener la fecha de hoy
    hoy = timezone.now().date()
    
    # Contar administraciones de hoy
    administraciones_hoy = AdministracionMedicamento.objects.filter(
        fecha_hora_administracion__date=hoy
    ).count()
    
    context = {
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'total_fichas_activas': FichaObstetrica.objects.filter(activa=True).count(),
        'administraciones_hoy': administraciones_hoy,
    }
    
    return render(request, 'Tens/Data/menu_tens.html', context)

# ============================================
# BÚSQUEDA DE PACIENTES
# ============================================

def buscar_paciente_tens(request):
    """Buscar paciente por RUT o nombre"""
    query = request.GET.get('q', '').strip()
    pacientes = []
    
    if query:
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
    
    return render(request, 'tens/data/buscar_paciente.html', {
        'pacientes': pacientes,
        'query': query
    })


def api_buscar_paciente(request):
    """API JSON para búsqueda de pacientes"""
    rut = request.GET.get('rut', '').strip()
    
    if not rut:
        return JsonResponse({'encontrado': False, 'mensaje': 'RUT no proporcionado'})
    
    try:
        from utilidad.rut_validator import normalizar_rut
        rut_normalizado = normalizar_rut(rut)
        
        paciente = Paciente.objects.select_related('persona').get(
            persona__Rut=rut_normalizado,
            activo=True
        )
        
        return JsonResponse({
            'encontrado': True,
            'paciente': {
                'id': paciente.pk,
                'rut': paciente.persona.Rut,
                'nombre_completo': f"{paciente.persona.Nombre} {paciente.persona.Apellido_Paterno} {paciente.persona.Apellido_Materno}",
                'edad': paciente.Edad,
            }
        })
    except Paciente.DoesNotExist:
        return JsonResponse({
            'encontrado': False,
            'mensaje': 'Paciente no encontrado'
        })


# ============================================
# GESTIÓN DE FICHAS
# ============================================

def ver_fichas_paciente(request, paciente_pk):
    """Ver todas las fichas obstétricas de un paciente"""
    paciente = get_object_or_404(
        Paciente.objects.select_related('persona'),
        pk=paciente_pk,
        activo=True
    )
    
    fichas = FichaObstetrica.objects.filter(
        paciente=paciente
    ).select_related(
        'matrona_responsable__persona'
    ).annotate(
        num_medicamentos=Count('medicamentos', filter=Q(medicamentos__activo=True))
    ).order_by('-fecha_creacion')
    
    return render(request, 'tens/Data/ver_fichas.html', {
        'paciente': paciente,
        'fichas': fichas
    })


def detalle_ficha_tens(request, ficha_pk):
    """Detalle de ficha obstétrica, medicamentos y tratamientos aplicados"""
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related(
            'paciente__persona',
            'matrona_responsable__persona'
        ),
        pk=ficha_pk
    )

    # Medicamentos prescritos
    medicamentos = MedicamentoFicha.objects.filter(
        ficha=ficha,
        activo=True
    ).order_by('-fecha_inicio')

    # Tratamientos aplicados por TENS
    tratamientos = Tratamiento_aplicado.objects.filter(
        ficha=ficha,
        activo=True
    ).select_related(
        'tens__persona',
        'medicamento_ficha'
    ).order_by('-fecha_aplicacion', '-hora_aplicacion')

    # Estadísticas
    total_medicamentos = medicamentos.count()
    total_tratamientos = tratamientos.count()

    return render(request, 'tens/formularios/detalle_ficha.html', {
        'ficha': ficha,
        'paciente': ficha.paciente,
        'medicamentos': medicamentos,
        'tratamientos': tratamientos,
        'total_medicamentos': total_medicamentos,
        'total_tratamientos': total_tratamientos,
    })

# ============================================
# ADMINISTRACIÓN DE MEDICAMENTOS
# ============================================

def registrar_administracion(request, medicamento_pk):
    """
    Registrar la administración de un medicamento
    El TENS registra: hora, si hizo lavado, observaciones
    """
    medicamento_ficha = get_object_or_404(
        MedicamentoFicha.objects.select_related(
            'ficha__paciente__persona'
        ),
        pk=medicamento_pk,
        activo=True
    )
    
    if request.method == 'POST':
        form = AdministracionMedicamentoForm(request.POST)
        
        if form.is_valid():
            administracion = form.save(commit=False)
            administracion.medicamento_ficha = medicamento_ficha
            
            # TODO: Obtener el TENS del usuario logueado
            # Por ahora, usamos el primer TENS disponible
            tens = Tens.objects.filter(Activo=True).first()
            if not tens:
                messages.error(request, "❌ No hay TENS registrados en el sistema.")
                return redirect('tens:detalle_ficha', ficha_pk=medicamento_ficha.ficha.pk)
            
            administracion.tens = tens
            administracion.save()
            
            messages.success(
                request,
                f"✅ Administración de {medicamento_ficha.nombre_medicamento} registrada exitosamente."
            )
            return redirect('tens:detalle_ficha', ficha_pk=medicamento_ficha.ficha.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores en el formulario.")
    else:
        # Pre-cargar fecha y hora actual
            form = AdministracionMedicamentoForm(initial={
            'fecha_hora_administracion': timezone.now()
            })
            
    return render(request, 'Tens/Formularios/registrar_administracion.html', {
        'form': form,
        'medicamento': medicamento_ficha,
        'ficha': medicamento_ficha.ficha,
        'paciente': medicamento_ficha.ficha.paciente
    })


def historial_administraciones(request, ficha_pk):
    """Ver historial completo de administraciones de una ficha"""
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related('paciente__persona'),
        pk=ficha_pk
    )
    
    administraciones = AdministracionMedicamento.objects.filter(
        medicamento_ficha__ficha=ficha
    ).select_related(
        'medicamento_ficha',
        'tens__persona'
    ).order_by('-fecha_hora_administracion')
    
    return render(request, 'tens/historial_administraciones.html', {
        'ficha': ficha,
        'paciente': ficha.paciente,
        'administraciones': administraciones
    })

def registrar_tens(request):
    """Vista para buscar paciente y registrar signos vitales"""
    
    buscar_form = BuscarPacienteForm()
    registro_form = None
    ficha = None
    
    # Si hay una ficha_id en la sesión, cargar la ficha
    ficha_id = request.session.get('ficha_id')
    if ficha_id:
        try:
            ficha = FichaObstetrica.objects.select_related('paciente', 'paciente__persona').get(id=ficha_id)
        except FichaObstetrica.DoesNotExist:
            del request.session['ficha_id']
            ficha = None
    
    # Procesar búsqueda de paciente/ficha
    if request.method == 'POST' and 'buscar_paciente' in request.POST:
        buscar_form = BuscarPacienteForm(request.POST)
        if buscar_form.is_valid():
            rut = buscar_form.cleaned_data['rut']
            try:
                # Buscar primero en el modelo Persona
                persona = Persona.objects.get(Rut=rut)
                paciente = Paciente.objects.get(persona=persona)
                # Buscar la ficha obstétrica del paciente
                ficha = FichaObstetrica.objects.filter(paciente=paciente).first()
                
                if ficha:
                    request.session['ficha_id'] = ficha.id
                    messages.success(request, f'Ficha obstétrica encontrada para: {persona.Nombre} {persona.Apellido_Paterno}')
                else:
                    messages.error(request, f'El paciente no tiene una ficha obstétrica registrada')
                    
            except Persona.DoesNotExist:
                messages.error(request, f'No se encontró ninguna persona con RUT: {rut}')
                if 'ficha_id' in request.session:
                    del request.session['ficha_id']
            except Paciente.DoesNotExist:
                messages.error(request, f'La persona con RUT {rut} no está registrada como paciente')
                if 'ficha_id' in request.session:
                    del request.session['ficha_id']
    
    # Procesar registro de signos vitales
    if request.method == 'POST' and 'guardar_registro' in request.POST:
        if ficha:
            registro_form = RegistroTensForm(request.POST)
            if registro_form.is_valid():
                registro = registro_form.save(commit=False)
                registro.ficha = ficha
                registro.save()
                messages.success(request, 'Registro guardado exitosamente')
                # Limpiar sesión después de guardar para buscar nuevo paciente
                if 'ficha_id' in request.session:
                    del request.session['ficha_id']
                return redirect('tens:parametros_tens')
        else:
            messages.error(request, 'Debe seleccionar un paciente primero')
    
    # Limpiar selección de ficha
    if request.method == 'POST' and 'limpiar' in request.POST:
        if 'ficha_id' in request.session:
            del request.session['ficha_id']
        return redirect('tens:parametros_tens')
    
    # Inicializar formulario de registro si hay ficha seleccionada
    if ficha and not registro_form:
        registro_form = RegistroTensForm(initial={'ficha': ficha})
    
    # Obtener últimos registros de la ficha
    ultimos_registros = []
    if ficha:
        ultimos_registros = RegistroTens.objects.filter(
            ficha=ficha
        ).order_by('-fecha')[:10]
    
    context = {
        'buscar_form': buscar_form,
        'registro_form': registro_form,
        'ficha': ficha,
        'ultimos_registros': ultimos_registros,
    }
    
    return render(request, 'tens/formularios/registro_tens.html', context)


# ============================================
# ADMINISTRACIÓN DE MEDICAMENTOS
# ============================================

def registrar_administracion(request, medicamento_pk):
    """Registrar administración de medicamento por TENS"""
    medicamento_ficha = get_object_or_404(
        MedicamentoFicha.objects.select_related('ficha__paciente__persona'),
        pk=medicamento_pk,
        activo=True
    )

    if request.method == 'POST':
        form = AdministracionMedicamentoForm(request.POST)
        if form.is_valid():
            administracion = form.save(commit=False)
            administracion.medicamento_ficha = medicamento_ficha

            # TODO: Obtener TENS del usuario logueado
            tens = Tens.objects.filter(Activo=True).first()
            if not tens:
                messages.error(request, "❌ No hay TENS registrados en el sistema.")
                return redirect('tens:detalle_ficha', ficha_pk=medicamento_ficha.ficha.pk)

            administracion.tens = tens
            administracion.save()
            messages.success(
                request,
                f"✅ Administración de {medicamento_ficha.nombre_medicamento} registrada exitosamente."
            )
            return redirect('tens:detalle_ficha', ficha_pk=medicamento_ficha.ficha.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores en el formulario.")
    else:
        form = AdministracionMedicamentoForm(initial={
            'fecha_hora_administracion': timezone.now()
        })

    return render(request, 'tens/formularios/registrar_administracion.html', {
        'form': form,
        'medicamento': medicamento_ficha,
        'ficha': medicamento_ficha.ficha,
        'paciente': medicamento_ficha.ficha.paciente
    })


def historial_administraciones(request, ficha_pk):
    """Historial completo de administraciones de una ficha"""
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related('paciente__persona'),
        pk=ficha_pk
    )

    administraciones = AdministracionMedicamento.objects.filter(
        medicamento_ficha__ficha=ficha
    ).select_related('medicamento_ficha', 'tens__persona').order_by('-fecha_hora_administracion')

    return render(request, 'tens/historial_administraciones.html', {
        'ficha': ficha,
        'paciente': ficha.paciente,
        'administraciones': administraciones
    })


# ============================================
# TRATAMIENTOS APLICADOS - VINCULADOS A FICHA
# ============================================

def registrar_tratamiento(request, ficha_pk):
    """
    Registrar un nuevo tratamiento aplicado vinculado a una ficha obstétrica
    
    Args:
        ficha_pk: ID de la ficha obstétrica
    """
    # Obtener la ficha con datos relacionados
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related(
            'paciente__persona',
            'matrona_responsable__persona'
        ),
        pk=ficha_pk,
        activa=True
    )
    
    if request.method == 'POST':
        form = FormularioTratamientoAplicado(request.POST, ficha=ficha)
        
        if form.is_valid():
            tratamiento = form.save(commit=False)
            
            # Asignar automáticamente la ficha y el paciente
            tratamiento.ficha = ficha
            tratamiento.paciente = ficha.paciente
            
            # TODO: Obtener TENS del usuario logueado cuando implementes autenticación
            # Por ahora toma el primer TENS activo
            tens = Tens.objects.filter(Activo=True).first()
            
            if not tens:
                messages.error(
                    request, 
                    "❌ No hay personal TENS registrado en el sistema. "
                    "Por favor contacte al administrador."
                )
                return redirect('tens:detalle_ficha', ficha_pk=ficha.pk)
            
            tratamiento.tens = tens
            tratamiento.save()
            
            messages.success(
                request,
                f"✅ Tratamiento '{tratamiento.nombre_medicamento}' registrado exitosamente "
                f"para {ficha.paciente.persona.Nombre} {ficha.paciente.persona.Apellido_Paterno}."
            )
            
            return redirect('tens:detalle_ficha', ficha_pk=ficha.pk)
        else:
            messages.error(
                request, 
                "⚠️ Por favor corrija los errores en el formulario."
            )
    else:
        # Inicializar formulario con valores por defecto
        form = FormularioTratamientoAplicado(
            ficha=ficha,
            initial={
                'fecha_aplicacion': timezone.now(),
                'hora_aplicacion': timezone.now().time()
            }
        )

    return render(request, 'tens/formularios/registrar_tratamiento.html', {
        'titulo': 'Registrar Tratamiento Aplicado',
        'form': form,
        'ficha': ficha,
        'paciente': ficha.paciente,
        'fecha_actual': timezone.now(),
    })


def listar_tratamientos_ficha(request, ficha_pk):
    """
    Listar todos los tratamientos aplicados de una ficha específica
    """
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related('paciente__persona'),
        pk=ficha_pk
    )
    
    tratamientos = Tratamiento_aplicado.objects.filter(
        ficha=ficha
    ).select_related(
        'tens__persona',
        'medicamento_ficha'
    ).order_by('-fecha_aplicacion', '-hora_aplicacion')
    
    return render(request, 'tens/formularios/listar_tratamientos_ficha.html', {
        'titulo': f'Tratamientos - Ficha {ficha.numero_ficha}',
        'ficha': ficha,
        'paciente': ficha.paciente,
        'tratamientos': tratamientos,
        'total_tratamientos': tratamientos.count(),
        'fecha_actual': timezone.now(),
    })


def editar_tratamiento(request, tratamiento_pk):
    """
    Editar un tratamiento aplicado existente
    """
    tratamiento = get_object_or_404(
        Tratamiento_aplicado.objects.select_related(
            'ficha__paciente__persona',
            'tens__persona'
        ),
        pk=tratamiento_pk
    )
    
    ficha = tratamiento.ficha

    if request.method == 'POST':
        form = FormularioTratamientoAplicado(
            request.POST, 
            instance=tratamiento,
            ficha=ficha
        )
        
        if form.is_valid():
            form.save()
            messages.success(
                request, 
                f"✅ Tratamiento actualizado correctamente."
            )
            return redirect('tens:detalle_ficha', ficha_pk=ficha.pk)
        else:
            messages.error(
                request,
                "⚠️ Por favor corrija los errores en el formulario."
            )
    else:
        form = FormularioTratamientoAplicado(
            instance=tratamiento, 
            ficha=ficha
        )

    return render(request, 'tens/formularios/registrar_tratamiento.html', {
        'form': form,
        'titulo': 'Editar Tratamiento Aplicado',
        'ficha': ficha,
        'paciente': ficha.paciente,
        'tratamiento': tratamiento,
        'fecha_actual': timezone.now(),
    })


def eliminar_tratamiento(request, tratamiento_pk):
    """
    Desactivar (soft delete) un tratamiento aplicado
    """
    tratamiento = get_object_or_404(Tratamiento_aplicado, pk=tratamiento_pk)
    ficha_pk = tratamiento.ficha.pk
    
    tratamiento.activo = False
    tratamiento.save()
    
    messages.success(
        request, 
        f"✅ Tratamiento '{tratamiento.nombre_medicamento}' ocultado correctamente."
    )
    return redirect('tens:detalle_ficha', ficha_pk=ficha_pk)


def restaurar_tratamiento(request, tratamiento_pk):
    """
    Reactivar un tratamiento aplicado
    """
    tratamiento = get_object_or_404(Tratamiento_aplicado, pk=tratamiento_pk)
    ficha_pk = tratamiento.ficha.pk
    
    tratamiento.activo = True
    tratamiento.save()
    
    messages.success(
        request, 
        f"✅ Tratamiento '{tratamiento.nombre_medicamento}' restaurado correctamente."
    )
    return redirect('tens:detalle_ficha', ficha_pk=ficha_pk)


# ============================================
# LISTADOS GENERALES DE TRATAMIENTOS (OPCIONAL)
# ============================================

def listar_todos_tratamientos(request):
    """
    Listar todos los tratamientos del sistema (para reportes)
    """
    tratamientos = Tratamiento_aplicado.objects.select_related(
        'ficha__paciente__persona',
        'tens__persona',
        'ficha'
    ).order_by('-fecha_aplicacion', '-hora_aplicacion')
    
    return render(request, 'tens/formularios/listar_tratamientos.html', {
        'titulo': 'Todos los Tratamientos Aplicados',
        'tratamientos': tratamientos,
        'total_tratamientos': tratamientos.count(),
        'fecha_actual': timezone.now(),
    })


def listar_tratamientos_activos(request):
    """Listar solo tratamientos activos"""
    tratamientos = Tratamiento_aplicado.objects.filter(
        activo=True
    ).select_related(
        'ficha__paciente__persona',
        'tens__persona',
        'ficha'
    ).order_by('-fecha_aplicacion', '-hora_aplicacion')
    
    return render(request, 'tens/formularios/listar_tratamientos.html', {
        'titulo': 'Tratamientos Activos',
        'tratamientos': tratamientos,
        'total_tratamientos': tratamientos.count(),
        'fecha_actual': timezone.now(),
    })


def listar_tratamientos_inactivos(request):
    """Listar solo tratamientos inactivos/eliminados"""
    tratamientos = Tratamiento_aplicado.objects.filter(
        activo=False
    ).select_related(
        'ficha__paciente__persona',
        'tens__persona',
        'ficha'
    ).order_by('-fecha_aplicacion', '-hora_aplicacion')
    
    return render(request, 'tens/formularios/listar_tratamientos.html', {
        'titulo': 'Tratamientos Inactivos',
        'tratamientos': tratamientos,
        'total_tratamientos': tratamientos.count(),
        'fecha_actual': timezone.now(),
    })