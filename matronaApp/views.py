from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.db.models import Q, Count, Prefetch

from matronaApp.models import IngresoPaciente, FichaObstetrica, MedicamentoFicha
from gestionApp.models import Persona, Paciente, Matrona
from gestionApp.forms.Gestion_form import PacienteForm
from matronaApp.forms import IngresoPacienteForm, FichaObstetricaForm  # <-- ESTA LÍNEA ES LA IMPORTANTE
from legacyApp.models import ControlesPrevios



def seleccionar_paciente_ficha(request):
    return render(request, 'Matrona/Data/seleccionar_paciente_ficha.html')

# ============================================
# VISTA PRINCIPAL DEL MÓDULO MATRONA
# ============================================

def menu_matrona(request):
    """Vista principal del módulo Matrona"""
    return render(request, 'Matrona/menu_matrona.html')


# ============================================
# VISTAS DE PACIENTE
# ============================================

class PacienteListView(ListView):
    """Listado de todos los pacientes"""
    model = Paciente
    template_name = 'Matrona/Data/paciente_list.html'
    context_object_name = 'pacientes'
    
    def get_queryset(self):
        return Paciente.objects.filter(activo=True).select_related('persona')


class PacienteDetailView(DetailView):
    """Detalle de un paciente específico"""
    model = Paciente
    template_name = 'Matrona/Data/paciente_detail.html'
    context_object_name = 'paciente'

    def get_queryset(self):
        return Paciente.objects.select_related('persona')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        paciente = ctx["paciente"]
        rut = (paciente.persona.Rut or "").strip()

        try:
            # Consulta SIEMPRE contra la BD legacy
            controles = (ControlesPrevios.objects
                         .using("legacy")
                         .filter(paciente_rut__iexact=rut)
                         .order_by("-fecha_control"))

            controles = list(controles)   # materializa para el template

            # seleccionar control por ?ctrl=<id> (o el más reciente)
            sel_id = self.request.GET.get("ctrl")
            seleccionado = None
            if controles:
                if sel_id:
                    seleccionado = next((c for c in controles if str(c.id) == str(sel_id)), controles[0])
                else:
                    seleccionado = controles[0]

            ctx.update({
                "legacy_controles": controles,
                "legacy_total": len(controles),
                "legacy_selected": seleccionado,
                "legacy_selected_id": getattr(seleccionado, "id", None),
                "legacy_fuente": "Base de datos histórica (LEGACY)",
            })
        except Exception as e:
            # si algo falla, no rompas el detalle
            import logging
            logging.getLogger(__name__).exception("Fallo consultando LEGACY: %s", e)
            ctx.update({
                "legacy_controles": [],
                "legacy_total": 0,
                "legacy_selected": None,
                "legacy_selected_id": None,
                "legacy_fuente": "LEGACY (sin conexión)",
                "legacy_error": True,
            })

        return ctx


def registrar_paciente(request):
    """Registrar un nuevo paciente"""
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            paciente = form.save()
            messages.success(request, "✅ Paciente registrado correctamente.")
            return redirect('matrona:detalle_paciente', pk=paciente.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores en el formulario.")
    else:
        form = PacienteForm()
    
    return render(request, 'Matrona/Formularios/registrar_paciente.html', {'form': form})


def buscar_paciente(request):
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
        ).select_related('persona')
    
    return render(request, 'Matrona/Data/buscar_paciente.html', {
        'pacientes': pacientes,
        'query': query
    })


# ============================================
# VISTAS DE INGRESO HOSPITALARIO
# ============================================

def registrar_ingreso(request):
    """Registrar ingreso hospitalario"""
    if request.method == 'POST':
        form = IngresoPacienteForm(request.POST)
        if form.is_valid():
            ingreso = form.save()
            messages.success(request, "✅ Ingreso registrado correctamente.")
            return redirect('matrona:detalle_ingreso', pk=ingreso.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores en el formulario.")
    else:
        form = IngresoPacienteForm()
    
    return render(request, 'Matrona/Formularios/registrar_ingreso.html', {'form': form})


def detalle_ingreso(request, pk):
    """Ver detalle de un ingreso"""
    ingreso = get_object_or_404(
        IngresoPaciente.objects.select_related('paciente__persona'),
        pk=pk
    )
    return render(request, 'Matrona/Formularios/detalle_ingresos.html', {
        'ingreso': ingreso,
        'paciente': ingreso.paciente
    })


# ============================================
# VISTAS DE FICHA OBSTÉTRICA
# ============================================

def seleccionar_paciente_ficha(request):
    """
    Vista para buscar y seleccionar un paciente antes de crear su ficha
    """
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
    
    return render(request, 'Matrona/Data/seleccionar_paciente_ficha.html', {
        'pacientes': pacientes,
        'query': query
    })


def crear_ficha_obstetrica(request, paciente_pk):
    """
    Crear una nueva ficha obstétrica para un paciente
    """
    paciente = get_object_or_404(
        Paciente.objects.select_related('persona'),
        pk=paciente_pk,
        activo=True
    )
    
    if request.method == 'POST':
        form = FichaObstetricaForm(request.POST)
        
        if form.is_valid():
            ficha = form.save(commit=False)
            ficha.paciente = paciente
            ficha.save()
            form.save_m2m()  # Guardar las patologías (ManyToMany)
            
            messages.success(
                request,
                f"✅ Ficha obstétrica {ficha.numero_ficha} creada exitosamente."
            )
            return redirect('matrona:detalle_ficha', pk=ficha.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores en el formulario.")
    else:
        # Preparar datos iniciales
        initial_data = {
            'paciente_id': paciente.pk,
        }
        form = FichaObstetricaForm(initial=initial_data)
    
    context = {
        'form': form,
        'paciente': paciente,
    }
    
    return render(request, 'Matrona/Formularios/crear_ficha.html', context)


def lista_fichas_paciente(request, paciente_pk):
    """
    Ver todas las fichas obstétricas de un paciente específico
    """
    paciente = get_object_or_404(
        Paciente.objects.select_related('persona'),
        pk=paciente_pk,
        activo=True
    )
    
    fichas = FichaObstetrica.objects.filter(
        paciente=paciente
    ).select_related(
        'matrona_responsable__persona'
    ).prefetch_related(
        'patologias'
    ).order_by('-fecha_creacion')
    
    return render(request, 'Matrona/Data/lista_fichas.html', {
        'paciente': paciente,
        'fichas': fichas
    })


def detalle_ficha(request, pk):
    """
    Ver detalle completo de una ficha obstétrica
    """
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related(
            'paciente__persona',
            'matrona_responsable__persona'
        ).prefetch_related('patologias'),
        pk=pk
    )
    
    # Obtener medicamentos asociados
    medicamentos = MedicamentoFicha.objects.filter(
        ficha=ficha,
        activo=True
    ).order_by('-fecha_inicio')
    
    return render(request, 'Matrona/Data/detalle_ficha.html', {
        'ficha': ficha,
        'paciente': ficha.paciente,
        'medicamentos': medicamentos,
    })


def editar_ficha(request, pk):
    """
    Editar una ficha obstétrica existente
    Solo se pueden editar fichas activas
    """
    # Obtener la ficha con sus relaciones
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related(
            'paciente__persona',
            'matrona_responsable__persona'
        ).prefetch_related('patologias'),
        pk=pk
    )
    
    # Verificar que la ficha esté activa
    if not ficha.activa:
        messages.warning(
            request, 
            "⚠️ No se puede editar una ficha cerrada. Si necesita modificarla, contacte al administrador."
        )
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    paciente = ficha.paciente
    
    if request.method == 'POST':
        # Crear formulario con los datos POST y la instancia existente
        form = FichaObstetricaForm(request.POST, instance=ficha)
        
        if form.is_valid():
            # Guardar sin commit para asegurar el paciente
            ficha_actualizada = form.save(commit=False)
            ficha_actualizada.paciente = paciente  # Mantener el mismo paciente
            ficha_actualizada.save()
            
            # Guardar relaciones ManyToMany (patologías)
            form.save_m2m()
            
            messages.success(
                request, 
                f"✅ Ficha obstétrica {ficha.numero_ficha} actualizada exitosamente."
            )
            return redirect('matrona:detalle_ficha', pk=ficha.pk)
        else:
            messages.error(
                request, 
                "❌ Por favor corrige los errores en el formulario."
            )
    else:
        # GET: Mostrar formulario con datos actuales
        initial_data = {
            'paciente_id': paciente.pk,
        }
        
        # CRÍTICO: Pasar instance para que se llenen los campos
        form = FichaObstetricaForm(instance=ficha, initial=initial_data)
    
    context = {
        'form': form,
        'ficha': ficha,
        'paciente': paciente,
        'editando': True,
    }
    
    return render(request, 'Matrona/Formularios/editar_ficha.html', context)


def desactivar_ficha(request, pk):
    """
    Cerrar/desactivar una ficha obstétrica
    """
    ficha = get_object_or_404(FichaObstetrica, pk=pk)
    
    if request.method == 'POST':
        ficha.activa = not ficha.activa
        ficha.save()
        
        estado = "activada" if ficha.activa else "cerrada"
        messages.success(request, f"✅ Ficha {ficha.numero_ficha} {estado} exitosamente.")
        
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    return render(request, 'Matrona/Formularios/toggle_ficha.html', {
        'ficha': ficha
    })


def lista_todas_fichas(request):
    """
    Listado general de todas las fichas obstétricas del sistema
    """
    fichas = FichaObstetrica.objects.select_related(
        'paciente__persona',
        'matrona_responsable__persona'
    ).order_by('-fecha_creacion')
    
    # Filtros opcionales
    activa = request.GET.get('activa')
    if activa == '1':
        fichas = fichas.filter(activa=True)
    elif activa == '0':
        fichas = fichas.filter(activa=False)
    
    return render(request, 'Matrona/Data/todas_fichas.html', {
        'fichas': fichas
    })


# ============================================
# GESTIÓN DE PATOLOGÍAS (Placeholders)
# ============================================

def asignar_patologia(request, paciente_pk):
    """Asignar patología a un paciente (en desarrollo)"""
    messages.info(request, "ℹ️ Función en desarrollo. Use las fichas obstétricas para asignar patologías.")
    return redirect('matrona:detalle_paciente', pk=paciente_pk)


def eliminar_patologia(request, paciente_pk, patologia_pk):
    """Eliminar una patología de un paciente (en desarrollo)"""
    messages.info(request, "ℹ️ Función en desarrollo. Use las fichas obstétricas para gestionar patologías.")
    return redirect('matrona:detalle_paciente', pk=paciente_pk)


# ============================================
# API REST (AJAX) - Para búsquedas dinámicas
# ============================================

def buscar_paciente_api(request):
    """
    Buscar paciente vía AJAX (retorna JSON)
    Usado en formularios para autocompletar datos
    """
    rut = request.GET.get('rut', '').strip()
    
    if not rut:
        return JsonResponse({
            'encontrado': False,
            'mensaje': 'RUT no proporcionado'
        })
    
    try:
        paciente = Paciente.objects.select_related('persona').get(
            persona__Rut=rut,
            activo=True
        )
        
        return JsonResponse({
            'encontrado': True,
            'paciente': {
                'id': paciente.pk,
                'rut': paciente.persona.Rut,
                'nombre_completo': f'{paciente.persona.Nombre} {paciente.persona.Apellido_Paterno} {paciente.persona.Apellido_Materno}',
                'edad': paciente.Edad,
                'telefono': paciente.persona.Telefono or '',
                'estado_civil': paciente.get_Estado_civil_display(),
                'prevision': paciente.get_Previcion_display(),
                'acompanante': paciente.Acompañante or '',
                'contacto_emergencia': paciente.Contacto_emergencia or '',
            }
        })
    except Paciente.DoesNotExist:
        return JsonResponse({
            'encontrado': False,
            'mensaje': 'No se encontró un paciente activo con ese RUT'
        })


def buscar_persona_api(request):
    """
    Buscar persona vía AJAX (retorna JSON)
    Usado para verificar si una persona existe antes de crear paciente
    """
    rut = request.GET.get('rut', '').strip()
    
    if not rut:
        return JsonResponse({
            'encontrado': False,
            'mensaje': 'RUT no proporcionado'
        })
    
    try:
        persona = Persona.objects.get(Rut=rut, Activo=True)
        
        # Verificar si ya es paciente
        es_paciente = hasattr(persona, 'paciente')
        
        response_data = {
            'encontrado': True,
            'es_paciente': es_paciente,
            'persona': {
                'rut': persona.Rut,
                'nombre_completo': f'{persona.Nombre} {persona.Apellido_Paterno} {persona.Apellido_Materno}',
                'fecha_nacimiento': persona.Fecha_nacimiento.strftime('%d/%m/%Y'),
                'telefono': persona.Telefono or '',
                'direccion': persona.Direccion or '',
                'email': persona.Email or '',
                'sexo': persona.Sexo,
            }
        }
        
        # Si ya es paciente, incluir info del paciente
        if es_paciente:
            response_data['paciente_id'] = persona.paciente.pk
            response_data['mensaje'] = 'Esta persona ya está registrada como paciente'
        
        return JsonResponse(response_data)
        
    except Persona.DoesNotExist:
        return JsonResponse({
            'encontrado': False,
            'mensaje': 'No se encontró una persona con ese RUT'
        })


# ============================================
# GESTIÓN DE MEDICAMENTOS EN FICHAS
# ============================================

def agregar_medicamento_ficha(request, ficha_pk):
    """
    Vista para que la MATRONA asigne un medicamento a una ficha
    """
    from matronaApp.forms.medicamento_forms import MatronaAsignarMedicamento
    
    ficha = get_object_or_404(
        FichaObstetrica.objects.select_related('paciente__persona'),
        pk=ficha_pk
    )
    
    # Verificar que la ficha esté activa
    if not ficha.activa:
        messages.error(request, "❌ No se pueden agregar medicamentos a una ficha cerrada.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    if request.method == 'POST':
        form = MatronaAsignarMedicamento(request.POST)
        
        if form.is_valid():
            medicamento = form.save(commit=False)
            medicamento.ficha = ficha
            medicamento.save()
            
            messages.success(
                request, 
                f"✅ Medicamento {medicamento.nombre_medicamento} asignado exitosamente."
            )
            return redirect('matrona:detalle_ficha', pk=ficha.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores en el formulario.")
    else:
        form = MatronaAsignarMedicamento()
    
    return render(request, 'Matrona/Formularios/agregar_medicamento.html', {
        'form': form,
        'ficha': ficha,
        'paciente': ficha.paciente
    })


def editar_medicamento_ficha(request, medicamento_pk):
    """
    Vista para que la MATRONA edite un medicamento asignado
    """
    from matronaApp.forms.medicamento_forms import MatronaAsignarMedicamento
    
    medicamento = get_object_or_404(
        MedicamentoFicha.objects.select_related('ficha__paciente__persona'),
        pk=medicamento_pk
    )
    
    ficha = medicamento.ficha
    
    # Verificar que la ficha esté activa
    if not ficha.activa:
        messages.error(request, "❌ No se pueden editar medicamentos de una ficha cerrada.")
        return redirect('matrona:detalle_ficha', pk=ficha.pk)
    
    if request.method == 'POST':
        form = MatronaAsignarMedicamento(request.POST, instance=medicamento)
        
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Medicamento actualizado exitosamente.")
            return redirect('matrona:detalle_ficha', pk=ficha.pk)
        else:
            messages.error(request, "❌ Por favor corrige los errores en el formulario.")
    else:
        form = MatronaAsignarMedicamento(instance=medicamento)
    
    return render(request, 'Matrona/Formularios/editar_medicamento.html', {
        'form': form,
        'medicamento': medicamento,
        'ficha': ficha,
        'paciente': ficha.paciente
    })


def desactivar_medicamento_ficha(request, medicamento_pk):
    """
    Desactivar un medicamento (no se elimina, solo se marca como inactivo)
    """
    medicamento = get_object_or_404(MedicamentoFicha, pk=medicamento_pk)
    
    if request.method == 'POST':
        medicamento.activo = False
        medicamento.save()
        
        messages.success(
            request,
            f"✅ Medicamento {medicamento.nombre_medicamento} desactivado."
        )
        return redirect('matrona:detalle_ficha', pk=medicamento.ficha.pk)
    
    return render(request, 'Matrona/Formularios/desactivar_medicamento.html', {
        'medicamento': medicamento
    })