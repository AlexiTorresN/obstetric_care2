# tensApp/urls.py
from django.urls import path
from . import views

app_name = 'tens'

urlpatterns = [
    # ============================================
    # MENÚ PRINCIPAL
    # ============================================
    path('', views.menu_tens, name='menu_tens'),
    
    # ============================================
    # GESTIÓN DE PACIENTES Y FICHAS
    # ============================================
    path('buscar-paciente/', views.buscar_paciente_tens, name='buscar_paciente'),
    path('paciente/<int:paciente_pk>/fichas/', views.ver_fichas_paciente, name='ver_fichas_paciente'),
    path('ficha/<int:ficha_pk>/', views.detalle_ficha_tens, name='detalle_ficha'),
    
    # ============================================
    # ADMINISTRACIÓN DE MEDICAMENTOS
    # ============================================
    #path('medicamento/<int:medicamento_pk>/administrar/', 
     #   views.registrar_administracion, 
      #  name='registrar_administracion'),
    
    #path('ficha/<int:ficha_pk>/historial/', 
     #   views.historial_administraciones, 
      #  name='historial_administraciones'),
    
    # ============================================
    # API - Búsqueda rápida
    # ============================================
    path('api/buscar-paciente/', 
        views.api_buscar_paciente, 
        name='api_buscar_paciente'),
    # ============================================
    # Formulario Datos Basicos
    # ============================================
    path('parametros/', views.registrar_tens, name='parametros_tens'),
    path('registrar/', views.registrar_tens, name='registrar_tens'),

    

    # ============================================
    # TRATAMIENTOS VINCULADOS A FICHA (NUEVAS RUTAS)
    # ============================================
    # Registrar tratamiento desde una ficha específica
    path(
        'ficha/<int:ficha_pk>/tratamiento/registrar/',
        views.registrar_tratamiento,
        name='registrar_tratamiento_ficha'
    ),
    
    # Listar tratamientos de una ficha específica
    path(
        'ficha/<int:ficha_pk>/tratamientos/',
        views.listar_tratamientos_ficha,
        name='listar_tratamientos_ficha'
    ),
    
    # Editar tratamiento específico
    path(
        'tratamiento/<int:tratamiento_pk>/editar/',
        views.editar_tratamiento,
        name='editar_tratamiento'
    ),
    
    # Eliminar tratamiento (soft delete)
    path(
        'tratamiento/<int:tratamiento_pk>/eliminar/',
        views.eliminar_tratamiento,
        name='eliminar_tratamiento'
    ),
    
    # Restaurar tratamiento
    path(
        'tratamiento/<int:tratamiento_pk>/restaurar/',
        views.restaurar_tratamiento,
        name='restaurar_tratamiento'
    ),
    
    # ============================================
    # GESTIÓN GENERAL DE TRATAMIENTOS (Vistas globales - OPCIONAL)
    # ============================================
    # Listar todos los tratamientos del sistema
    path('tratamientos/', views.listar_todos_tratamientos, name='listar_tratamientos'),
    
    # Solo tratamientos activos
    path('tratamientos/activos/', views.listar_tratamientos_activos, name='listar_tratamientos_activos'),
    
    # Solo tratamientos inactivos
    path('tratamientos/inactivos/', views.listar_tratamientos_inactivos, name='listar_tratamientos_inactivos'),

    # ============================================
    # API - Búsqueda rápida
    # ============================================
    path('api/buscar-paciente/', views.api_buscar_paciente, name='api_buscar_paciente'),

]