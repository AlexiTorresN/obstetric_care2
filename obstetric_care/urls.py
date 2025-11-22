from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from inicioApp import views as inicio_views
from core.views import custom_403

# Handler de error
handler403 = 'core.views.custom_403'

urlpatterns = [
    # ============================================
    # ADMIN DE DJANGO
    # ============================================
    path('admin/', admin.site.urls),

    # ============================================
    # PÁGINA PRINCIPAL
    # ============================================
    path('', inicio_views.home, name='home'),

    # ============================================
    # AUTENTICACIÓN (authentication app)
    # ============================================
    path('', include('authentication.urls')),  # login, logout

    # ============================================
    # APPS DEL SISTEMA
    # ============================================
    path('gestion/', include('gestionApp.urls')),
    path('matrona/', include('matronaApp.urls')),
    path('medico/', include('medicoApp.urls')),
    path('tens/', include('tensApp.urls')),
    path('partos/', include('partosApp.urls')),

    # ============================================
    # AUTENTICACIÓN 2FA (TEMPORALMENTE DESACTIVADO)
    # ============================================
    # path('2fa/', include('two_factor.urls')),
]

# ============================================
# DEBUG TOOLBAR (TEMPORALMENTE DESACTIVADO)
# ============================================
# if settings.DEBUG:
#     try:
#         import debug_toolbar
#         urlpatterns = [
#             path('__debug__/', include(debug_toolbar.urls)),
#         ] + urlpatterns
#     except ImportError:
#  