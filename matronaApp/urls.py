# matronaApp/urls.py
"""
URLs para la gestión de pacientes, ingresos y fichas obstétricas
Módulo de Matrona
"""
from django.urls import path
from . import views

app_name = 'matrona'

urlpatterns = [
    # ============================================
    # RUTA PRINCIPAL
    # ============================================
    path('', views.menu_matrona, name='menu_matrona'),  # ✅ CORREGIDO: era menu_medico
    
    # ============================================
    # RUTAS DE PACIENTE
    # ============================================
    path('pacientes/', views.PacienteListView.as_view(), name='lista_pacientes'),
    path('paciente/<int:pk>/', views.PacienteDetailView.as_view(), name='detalle_paciente'),
    path('paciente/registrar/', views.registrar_paciente, name='registrar_paciente'),
    path('paciente/buscar/', views.buscar_paciente, name='buscar_paciente'),

    # ============================================
    # RUTAS DE INGRESO HOSPITALARIO
    # ============================================
    path('ingreso/registrar/', views.registrar_ingreso, name='registrar_ingreso'),
    path('ingreso/<int:pk>/', views.detalle_ingreso, name='detalle_ingreso'),

    # ============================================
    # RUTAS DE FICHA OBSTÉTRICA
    # ============================================
    
    # Seleccionar paciente para crear ficha
    path('ficha/seleccionar-paciente/', 
        views.seleccionar_paciente_ficha, 
        name='seleccionar_paciente_ficha'),
    
    # Gestión de fichas de un paciente específico
    path('paciente/<int:paciente_pk>/ficha/crear/', 
        views.crear_ficha_obstetrica, 
        name='crear_ficha'),
    
    path('paciente/<int:paciente_pk>/fichas/', 
        views.lista_fichas_paciente, 
        name='lista_fichas_paciente'),
    
    # Gestión de fichas individuales
    path('ficha/<int:pk>/', 
        views.detalle_ficha, 
        name='detalle_ficha'),
    
    path('ficha/<int:pk>/editar/', 
        views.editar_ficha, 
        name='editar_ficha'),
    
    path('ficha/<int:pk>/toggle/', 
        views.desactivar_ficha, 
        name='toggle_ficha'),
    
    # Listado general de todas las fichas
    path('fichas/', 
        views.lista_todas_fichas, 
        name='todas_fichas'),

    # ============================================
    # RUTAS DE PATOLOGÍAS (Placeholder - Futuro)
    # ============================================
    path('paciente/<int:paciente_pk>/patologia/asignar/', 
        views.asignar_patologia, 
        name='asignar_patologia'),
    
    path('paciente/<int:paciente_pk>/patologia/<int:patologia_pk>/eliminar/', 
        views.eliminar_patologia, 
        name='eliminar_patologia'),

    # ============================================
    # API REST (para búsquedas AJAX)
    # ============================================
    path('api/paciente/buscar/', 
        views.buscar_paciente_api, 
        name='api_buscar_paciente'),
    
    path('api/persona/buscar/', 
        views.buscar_persona_api, 
        name='api_buscar_persona'),

    # ============================================
    # GESTIÓN DE MEDICAMENTOS EN FICHAS
    # ============================================
    path('ficha/<int:ficha_pk>/medicamento/agregar/', 
        views.agregar_medicamento_ficha, 
        name='agregar_medicamento'),
    
    path('medicamento/<int:medicamento_pk>/editar/', 
        views.editar_medicamento_ficha, 
        name='editar_medicamento'),
    
    path('medicamento/<int:medicamento_pk>/desactivar/', 
        views.desactivar_medicamento_ficha, 
        name='desactivar_medicamento'),
]