from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Count, Prefetch
from django.utils import timezone
from django.core.paginator import Paginator

from partosApp.models import RegistroParto
from recienNacidoApp.models import RegistroRecienNacido, DocumentosParto
from matronaApp.models import FichaObstetrica
from gestionApp.models import Paciente

from partosApp.forms import (
    # Formularios de Parto
    RegistroPartoBaseForm,
    TrabajoDePartoForm,
    InformacionPartoForm,
    PuerperioForm,
    AnestesiaAnalgesiaForm,
    ProfesionalesForm,
    RegistroPartoCompletoForm,
    # Formularios de Recién Nacido
    RegistroRecienNacidoForm,
    DatosRecienNacidoForm,
    ApegoAcompanamientoForm,
    # Formularios de Documentos
    DocumentosPartoForm,
)


# ============================================
# MENÚ PRINCIPAL
# ============================================

def menu_partos(request):
    """Vista principal del módulo de Partos"""
    
    # Estadísticas generales
    hoy = timezone.now().date()
    
    context = {
        'total_partos': RegistroParto.objects.filter(activo=True).count(),
        'partos_hoy': RegistroParto.objects.filter(
            fecha_hora_admision__date=hoy,
            activo=True
        ).count(),
        'partos_mes': RegistroParto.objects.filter(
            fecha_hora_admision__year=hoy.year,
            fecha_hora_admision__month=hoy.month,
            activo=True
        ).count(),
        'total_rn': RegistroRecienNacido.objects.count(),
        'rn_hoy': RegistroRecienNacido.objects.filter(
            fecha_nacimiento__date=hoy
        ).count(),
        # Estadísticas por tipo de parto
        'partos_eutocicos': RegistroParto.objects.filter(
            tipo_parto='EUTOCICO',
            activo=True
        ).count(),
        'cesareas': RegistroParto.objects.filter(
            tipo_parto__in=['CESAREA_URGENCIA', 'CESAREA_ELECTIVA'],
            activo=True
        ).count(),
    }
    
    return render(request, 'Partos/menu_partos.html', context)


# ============================================
# BÚSQUEDA Y SELECCIÓN DE FICHAS
# ============================================

def seleccionar_ficha_parto(request):
    """
    Buscar y seleccionar ficha obstétrica para registrar parto
    """
    query = request.GET.get('q', '').strip()
    fichas = []
    
    if query:
        fichas = FichaObstetrica.objects.filter(
            activa=True
        ).filter(
            Q(numero_ficha__icontains=query) |
            Q(paciente__persona__Rut__icontains=query) |
            Q(paciente__persona__Nombre__icontains=query) |
            Q(paciente__persona__Apellido_Paterno__icontains=query)
        ).select_related(
            'paciente__persona',
            'matrona_responsable__persona'
        ).annotate(
            num_partos=Count('registros_parto')
        )[:20]
    
    return render(request, 'Partos/seleccionar_ficha.html', {
        'fichas': fichas,
        'query': query
    })


# ============================================
# REGISTRO DE PARTO - OPCIÓN 1: POR PASOS
# ============================================

def registrar_parto_paso1(request, ficha_pk):
    """
    PASO 1: Información básica del parto
    """
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related('paciente__persona'),
        pk=ficha_pk,
        activa=True
    )
    
    if request.method == 'POST':
        form = RegistroPartoBaseForm(request.POST)
        if form.is_valid():
            parto = form.save()
            # Guardar el ID en sesión para los siguientes pasos
            request.session['parto_actual_id'] = parto.pk
            messages.success(request, f'✅ Parto {parto.numero_registro} iniciado correctamente.')
            return redirect('partos:registrar_parto_paso2')
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario.')
    else:
        # Pre-seleccionar la ficha
        form = RegistroPartoBaseForm(initial={'ficha': ficha})
    
    context = {
        'form': form,
        'ficha': ficha,
        'paciente': ficha.paciente,
        'paso': 1,
        'total_pasos': 6,
    }
    
    return render(request, 'Partos/Formularios/paso1_base.html', context)


def registrar_parto_paso2(request):
    """
    PASO 2: Trabajo de parto
    """
    parto_id = request.session.get('parto_actual_id')
    if not parto_id:
        messages.warning(request, '⚠️ Sesión expirada. Inicia nuevamente el registro.')
        return redirect('partos:seleccionar_ficha')
    
    parto = get_object_or_404(RegistroParto, pk=parto_id)
    
    if request.method == 'POST':
        form = TrabajoDePartoForm(request.POST, instance=parto)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Información de trabajo de parto guardada.')
            return redirect('partos:registrar_parto_paso3')
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = TrabajoDePartoForm(instance=parto)
    
    context = {
        'form': form,
        'parto': parto,
        'paso': 2,
        'total_pasos': 6,
    }
    
    return render(request, 'Partos/Formularios/paso2_trabajo.html', context)


def registrar_parto_paso3(request):
    """
    PASO 3: Información del parto
    """
    parto_id = request.session.get('parto_actual_id')
    if not parto_id:
        messages.warning(request, '⚠️ Sesión expirada.')
        return redirect('partos:seleccionar_ficha')
    
    parto = get_object_or_404(RegistroParto, pk=parto_id)
    
    if request.method == 'POST':
        form = InformacionPartoForm(request.POST, instance=parto)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Información del parto guardada.')
            return redirect('partos:registrar_parto_paso4')
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = InformacionPartoForm(instance=parto)
    
    context = {
        'form': form,
        'parto': parto,
        'paso': 3,
        'total_pasos': 6,
    }
    
    return render(request, 'Partos/Formularios/paso3_info.html', context)


def registrar_parto_paso4(request):
    """
    PASO 4: Puerperio
    """
    parto_id = request.session.get('parto_actual_id')
    if not parto_id:
        messages.warning(request, '⚠️ Sesión expirada.')
        return redirect('partos:seleccionar_ficha')
    
    parto = get_object_or_404(RegistroParto, pk=parto_id)
    
    if request.method == 'POST':
        form = PuerperioForm(request.POST, instance=parto)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Información de puerperio guardada.')
            return redirect('partos:registrar_parto_paso5')
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = PuerperioForm(instance=parto)
    
    context = {
        'form': form,
        'parto': parto,
        'paso': 4,
        'total_pasos': 6,
    }
    
    return render(request, 'Partos/Formularios/paso4_puerperio.html', context)


def registrar_parto_paso5(request):
    """
    PASO 5: Anestesia y Analgesia
    """
    parto_id = request.session.get('parto_actual_id')
    if not parto_id:
        messages.warning(request, '⚠️ Sesión expirada.')
        return redirect('partos:seleccionar_ficha')
    
    parto = get_object_or_404(RegistroParto, pk=parto_id)
    
    if request.method == 'POST':
        form = AnestesiaAnalgesiaForm(request.POST, instance=parto)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Información de anestesia guardada.')
            return redirect('partos:registrar_parto_paso6')
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = AnestesiaAnalgesiaForm(instance=parto)
    
    context = {
        'form': form,
        'parto': parto,
        'paso': 5,
        'total_pasos': 6,
    }
    
    return render(request, 'Partos/Formularios/paso5_anestesia.html', context)


def registrar_parto_paso6(request):
    """
    PASO 6: Profesionales y finalización
    """
    parto_id = request.session.get('parto_actual_id')
    if not parto_id:
        messages.warning(request, '⚠️ Sesión expirada.')
        return redirect('partos:seleccionar_ficha')
    
    parto = get_object_or_404(RegistroParto, pk=parto_id)
    
    if request.method == 'POST':
        form = ProfesionalesForm(request.POST, instance=parto)
        if form.is_valid():
            form.save()
            # Limpiar sesión
            if 'parto_actual_id' in request.session:
                del request.session['parto_actual_id']
            messages.success(request, f'🎉 Registro de parto {parto.numero_registro} completado exitosamente.')
            return redirect('partos:detalle_parto', pk=parto.pk)
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = ProfesionalesForm(instance=parto)
    
    context = {
        'form': form,
        'parto': parto,
        'paso': 6,
        'total_pasos': 6,
    }
    
    return render(request, 'Partos/Formularios/paso6_profesionales.html', context)


# ============================================
# REGISTRO DE PARTO - OPCIÓN 2: COMPLETO
# ============================================

def registrar_parto_completo(request, ficha_pk):
    """
    Registrar parto completo en una sola vista
    Recomendado solo para usuarios experimentados
    """
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related('paciente__persona'),
        pk=ficha_pk,
        activa=True
    )
    
    if request.method == 'POST':
        form = RegistroPartoCompletoForm(request.POST)
        if form.is_valid():
            parto = form.save()
            messages.success(request, f'🎉 Parto {parto.numero_registro} registrado exitosamente.')
            return redirect('partos:detalle_parto', pk=parto.pk)
        else:
            messages.error(request, '❌ Por favor corrige los errores en el formulario.')
    else:
        form = RegistroPartoCompletoForm(initial={'ficha': ficha})
    
    context = {
        'form': form,
        'ficha': ficha,
        'paciente': ficha.paciente,
    }
    
    return render(request, 'Partos/Formularios/registro_completo.html', context)


# ============================================
# LISTADO Y DETALLE DE PARTOS
# ============================================

def listar_partos(request):
    """
    Listar todos los partos con filtros y búsqueda
    """
    partos = RegistroParto.objects.filter(
        activo=True
    ).select_related(
        'ficha__paciente__persona'
    ).order_by('-fecha_hora_admision')
    
    # Filtros
    busqueda = request.GET.get('q', '').strip()
    tipo_parto = request.GET.get('tipo_parto', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')
    
    if busqueda:
        partos = partos.filter(
            Q(numero_registro__icontains=busqueda) |
            Q(ficha__numero_ficha__icontains=busqueda) |
            Q(ficha__paciente__persona__Rut__icontains=busqueda) |
            Q(ficha__paciente__persona__Nombre__icontains=busqueda) |
            Q(ficha__paciente__persona__Apellido_Paterno__icontains=busqueda)
        )
    
    if tipo_parto:
        partos = partos.filter(tipo_parto=tipo_parto)
    
    if fecha_inicio:
        partos = partos.filter(fecha_hora_admision__gte=fecha_inicio)
    
    if fecha_fin:
        partos = partos.filter(fecha_hora_admision__lte=fecha_fin)
    
    # Paginación
    paginator = Paginator(partos, 20)  # 20 partos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'partos': page_obj,
        'total_partos': partos.count(),
        'busqueda': busqueda,
        'tipo_parto': tipo_parto,
    }
    
    return render(request, 'Partos/Data/listar_partos.html', context)


def detalle_parto(request, pk):
    """
    Ver detalle completo de un parto
    """
    parto = get_object_or_404(
        RegistroParto.objects.select_related(
            'ficha__paciente__persona',
            'ficha__matrona_responsable__persona'
        ).prefetch_related(
            'recien_nacidos'
        ),
        pk=pk
    )
    
    # Obtener documentos asociados (si existen)
    try:
        documentos = parto.documentos
    except DocumentosParto.DoesNotExist:
        documentos = None
    
    context = {
        'parto': parto,
        'ficha': parto.ficha,
        'paciente': parto.ficha.paciente,
        'documentos': documentos,
        'recien_nacidos': parto.recien_nacidos.all(),
    }
    
    return render(request, 'Partos/Data/detalle_parto.html', context)


def editar_parto(request, pk):
    """
    Editar un registro de parto existente
    """
    parto = get_object_or_404(RegistroParto, pk=pk, activo=True)
    
    if request.method == 'POST':
        form = RegistroPartoCompletoForm(request.POST, instance=parto)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Parto {parto.numero_registro} actualizado correctamente.')
            return redirect('partos:detalle_parto', pk=parto.pk)
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = RegistroPartoCompletoForm(instance=parto)
    
    context = {
        'form': form,
        'parto': parto,
        'editando': True,
    }
    
    return render(request, 'Partos/Formularios/editar_parto.html', context)


# ============================================
# REGISTRO DE RECIÉN NACIDO
# ============================================

def registrar_recien_nacido(request, parto_pk):
    """
    Registrar recién nacido asociado a un parto
    """
    parto = get_object_or_404(
        RegistroParto.objects.select_related('ficha__paciente__persona'),
        pk=parto_pk,
        activo=True
    )
    
    if request.method == 'POST':
        form = RegistroRecienNacidoForm(request.POST, registro_parto=parto)
        if form.is_valid():
            rn = form.save()
            messages.success(request, f'✅ Recién nacido registrado exitosamente.')
            return redirect('partos:detalle_rn', pk=rn.pk)
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = RegistroRecienNacidoForm(registro_parto=parto)
    
    context = {
        'form': form,
        'parto': parto,
        'paciente': parto.ficha.paciente,
    }
    
    return render(request, 'Partos/Formularios/registrar_rn.html', context)


def registrar_gemelos(request, parto_pk):
    """
    Registrar gemelos o múltiples (2 o más RN del mismo parto)
    """
    parto = get_object_or_404(
        RegistroParto.objects.select_related('ficha__paciente__persona'),
        pk=parto_pk,
        activo=True
    )
    
    if request.method == 'POST':
        # Gemelo 1
        form1 = RegistroRecienNacidoForm(
            request.POST,
            prefix='gemelo1',
            registro_parto=parto
        )
        # Gemelo 2
        form2 = RegistroRecienNacidoForm(
            request.POST,
            prefix='gemelo2',
            registro_parto=parto
        )
        
        if form1.is_valid() and form2.is_valid():
            rn1 = form1.save()
            rn2 = form2.save()
            messages.success(request, f'✅ Gemelos registrados exitosamente.')
            return redirect('partos:detalle_parto', pk=parto.pk)
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form1 = RegistroRecienNacidoForm(prefix='gemelo1', registro_parto=parto)
        form2 = RegistroRecienNacidoForm(prefix='gemelo2', registro_parto=parto)
    
    context = {
        'form1': form1,
        'form2': form2,
        'parto': parto,
        'paciente': parto.ficha.paciente,
    }
    
    return render(request, 'Partos/Formularios/registrar_gemelos.html', context)


def detalle_recien_nacido(request, pk):
    """
    Ver detalle completo de un recién nacido
    """
    rn = get_object_or_404(
        RegistroRecienNacido.objects.select_related(
            'registro_parto__ficha__paciente__persona'
        ),
        pk=pk
    )
    
    context = {
        'rn': rn,
        'parto': rn.registro_parto,
        'paciente': rn.registro_parto.ficha.paciente,
    }
    
    return render(request, 'Partos/Data/detalle_rn.html', context)


def editar_recien_nacido(request, pk):
    """
    Editar información del recién nacido
    """
    rn = get_object_or_404(RegistroRecienNacido, pk=pk)
    
    if request.method == 'POST':
        form = RegistroRecienNacidoForm(
            request.POST,
            instance=rn,
            registro_parto=rn.registro_parto
        )
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Información del RN actualizada correctamente.')
            return redirect('partos:detalle_rn', pk=rn.pk)
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = RegistroRecienNacidoForm(
            instance=rn,
            registro_parto=rn.registro_parto
        )
    
    context = {
        'form': form,
        'rn': rn,
        'editando': True,
    }
    
    return render(request, 'Partos/Formularios/editar_rn.html', context)


# ============================================
# GESTIÓN DE DOCUMENTOS
# ============================================

def gestionar_documentos(request, parto_pk):
    """
    Gestionar documentos legales y administrativos del parto
    """
    parto = get_object_or_404(RegistroParto, pk=parto_pk, activo=True)
    
    # Obtener o crear documentos
    documentos, created = DocumentosParto.objects.get_or_create(
        registro_parto=parto
    )
    
    if request.method == 'POST':
        form = DocumentosPartoForm(
            request.POST,
            instance=documentos,
            registro_parto=parto
        )
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Documentos actualizados correctamente.')
            return redirect('partos:detalle_parto', pk=parto.pk)
        else:
            messages.error(request, '❌ Por favor corrige los errores.')
    else:
        form = DocumentosPartoForm(
            instance=documentos,
            registro_parto=parto
        )
    
    context = {
        'form': form,
        'parto': parto,
        'documentos': documentos,
        'es_nuevo': created,
    }
    
    return render(request, 'Partos/Formularios/gestionar_documentos.html', context)


# ============================================
# REPORTES Y ESTADÍSTICAS
# ============================================

def estadisticas_partos(request):
    """
    Vista con estadísticas y gráficos de partos
    """
    # Obtener rango de fechas
    hoy = timezone.now().date()
    mes_actual = hoy.replace(day=1)
    
    # Estadísticas del mes
    partos_mes = RegistroParto.objects.filter(
        fecha_hora_admision__gte=mes_actual,
        activo=True
    )
    
    # Por tipo de parto
    stats_tipo = {
        'eutocico': partos_mes.filter(tipo_parto='EUTOCICO').count(),
        'distocico': partos_mes.filter(tipo_parto='DISTOCICO').count(),
        'cesarea_urgencia': partos_mes.filter(tipo_parto='CESAREA_URGENCIA').count(),
        'cesarea_electiva': partos_mes.filter(tipo_parto='CESAREA_ELECTIVA').count(),
    }
    
    # Por clasificación de Robson
    stats_robson = {}
    for grupo in RegistroParto.objects.filter(
        fecha_hora_admision__gte=mes_actual
    ).values('clasificacion_robson').annotate(total=Count('id')):
        stats_robson[grupo['clasificacion_robson']] = grupo['total']
    
    context = {
        'partos_mes': partos_mes.count(),
        'stats_tipo': stats_tipo,
        'stats_robson': stats_robson,
        'mes_nombre': mes_actual.strftime('%B %Y'),
    }
    
    return render(request, 'Partos/Data/estadisticas.html', context)


# ============================================
# API Y BÚSQUEDAS AJAX
# ============================================

def api_buscar_ficha(request):
    """
    API para búsqueda de fichas (para autocomplete)
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 3:
        return JsonResponse({'fichas': []})
    
    fichas = FichaObstetrica.objects.filter(
        activa=True
    ).filter(
        Q(numero_ficha__icontains=query) |
        Q(paciente__persona__Rut__icontains=query) |
        Q(paciente__persona__Nombre__icontains=query)
    ).select_related(
        'paciente__persona'
    )[:10]
    
    resultados = [{
        'id': f.pk,
        'numero_ficha': f.numero_ficha,
        'paciente_nombre': f"{f.paciente.persona.Nombre} {f.paciente.persona.Apellido_Paterno}",
        'paciente_rut': f.paciente.persona.Rut,
    } for f in fichas]
    
    return JsonResponse({'fichas': resultados})