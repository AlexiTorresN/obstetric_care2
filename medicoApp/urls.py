"""
URLs para la gestión del catálogo de patologías
"""
from django.urls import path
from . import views

app_name = 'medico'  # ✅ ESTO ES CRÍTICO

urlpatterns = [
    # ============================================
    # MENÚ PRINCIPAL
    # ============================================
    path('', views.menu_medico, name='menu_medico'),
    
    # ============================================
    # GESTIÓN DE PATOLOGÍAS
    # ============================================
    path('patologias/', views.listar_patologias, name='listar_patologias'),
    path('patologia/registrar/', views.registrar_patologia, name='registrar_patologia'),
    path('patologia/<int:pk>/', views.detalle_patologia, name='detalle_patologia'),
    path('patologia/<int:pk>/editar/', views.editar_patologia, name='editar_patologia'),
    path('patologia/<int:pk>/toggle/', views.toggle_patologia, name='toggle_patologia'),
    
    # ============================================
    # CONSULTA DE HISTORIAL CLÍNICO (NUEVO)
    # ============================================
    path('paciente/buscar/', views.buscar_paciente_medico, name='buscar_paciente'),
    path('paciente/<int:paciente_pk>/historial/', views.ver_historial_clinico, name='historial_clinico'),
]