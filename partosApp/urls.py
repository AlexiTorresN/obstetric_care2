from django.urls import path
from . import views

app_name = 'partos'  # Namespace importante

urlpatterns = [
    # ============================================
    # MENÚ PRINCIPAL
    # ============================================
    path('', views.menu_partos, name='menu_partos'),
    
    # ============================================
    # BÚSQUEDA Y SELECCIÓN
    # ============================================
    path('seleccionar-ficha/', 
        views.seleccionar_ficha_parto, 
        name='seleccionar_ficha'),
    
    # ============================================
    # REGISTRO DE PARTO - OPCIÓN 1: POR PASOS
    # ============================================
    path('ficha/<int:ficha_pk>/parto/paso1/', 
        views.registrar_parto_paso1, 
        name='registrar_parto_paso1'),
    
    path('parto/paso2/', 
        views.registrar_parto_paso2, 
        name='registrar_parto_paso2'),
    
    path('parto/paso3/', 
        views.registrar_parto_paso3, 
        name='registrar_parto_paso3'),
    
    path('parto/paso4/', 
        views.registrar_parto_paso4, 
        name='registrar_parto_paso4'),
    
    path('parto/paso5/', 
        views.registrar_parto_paso5, 
        name='registrar_parto_paso5'),
    
    path('parto/paso6/', 
        views.registrar_parto_paso6, 
        name='registrar_parto_paso6'),
    
    # ============================================
    # REGISTRO DE PARTO - OPCIÓN 2: COMPLETO
    # ============================================
    path('ficha/<int:ficha_pk>/parto/completo/', 
        views.registrar_parto_completo, 
        name='registrar_parto_completo'),
    
    # ============================================
    # LISTADO Y DETALLE DE PARTOS
    # ============================================
    path('partos/', 
        views.listar_partos, 
        name='listar_partos'),
    
    path('parto/<int:pk>/', 
        views.detalle_parto, 
        name='detalle_parto'),
    
    path('parto/<int:pk>/editar/', 
        views.editar_parto, 
        name='editar_parto'),
    
    # ============================================
    # REGISTRO DE RECIÉN NACIDO
    # ============================================
    path('parto/<int:parto_pk>/rn/registrar/', 
        views.registrar_recien_nacido, 
        name='registrar_rn'),
    
    path('parto/<int:parto_pk>/gemelos/registrar/', 
        views.registrar_gemelos, 
        name='registrar_gemelos'),
    
    path('rn/<int:pk>/', 
        views.detalle_recien_nacido, 
        name='detalle_rn'),
    
    path('rn/<int:pk>/editar/', 
        views.editar_recien_nacido, 
        name='editar_rn'),
    
    # ============================================
    # GESTIÓN DE DOCUMENTOS
    # ============================================
    path('parto/<int:parto_pk>/documentos/', 
        views.gestionar_documentos, 
        name='gestionar_documentos'),
    
    # ============================================
    # REPORTES Y ESTADÍSTICAS
    # ============================================
    path('estadisticas/', 
        views.estadisticas_partos, 
        name='estadisticas'),
    
    # ============================================
    # API Y BÚSQUEDAS AJAX
    # ============================================
    path('api/buscar-ficha/', 
        views.api_buscar_ficha, 
        name='api_buscar_ficha'),
]