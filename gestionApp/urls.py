# gestionApp/urls.py
from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # ============================================
    # DASHBOARD ADMINISTRATIVO
    # ============================================
    path('dashboard/', views.dashboard_admin, name='dashboard_admin'),
    
    # ============================================
    # PERSONAS
    # ============================================
    path('personas/', views.PersonaListView.as_view(), name='lista_personas'),
    path('persona/<int:pk>/', views.PersonaDetailView.as_view(), name='detalle_persona'),
    path('persona/registrar/', views.agregar_persona, name='registrar_persona'),
    
    # ============================================
    # GESTIÓN DE ROLES
    # ============================================
    path('persona/<int:pk>/roles/', views.gestionar_roles_persona, name='gestionar_roles'),
    path('persona/<int:pk>/rol/paciente/', views.asignar_rol_paciente, name='asignar_rol_paciente'),
    path('persona/<int:pk>/rol/medico/', views.asignar_rol_medico, name='asignar_rol_medico'),
    path('persona/<int:pk>/rol/matrona/', views.asignar_rol_matrona, name='asignar_rol_matrona'),
    path('persona/<int:pk>/rol/tens/', views.asignar_rol_tens, name='asignar_rol_tens'),
    
    # ============================================
    # REGISTRO DIRECTO DE ROLES (Mantener por compatibilidad)
    # ============================================
    path('paciente/registrar/', views.agregar_paciente, name='registrar_paciente'),
    path('medico/registrar/', views.agregar_medico, name='registrar_medico'),
    path('matrona/registrar/', views.agregar_matrona, name='registrar_matrona'),
    path('tens/registrar/', views.agregar_tens, name='registrar_tens'),
    
    # ============================================
    # API REST (AJAX)
    # ============================================
    path('api/persona/buscar/', views.buscar_persona_api, name='buscar_persona_api'),
]