from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from inicioApp import views as inicio_views
from core.views import custom_403

# Handler de error
handler403 = 'core.views.custom_403'

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página principal
    path('', inicio_views.home, name='home'),

    # Apps del sistema
    path('gestion/', include('gestionApp.urls')),
    path('matrona/', include('matronaApp.urls')),
    path('medico/', include('medicoApp.urls')),
    path('tens/', include('tensApp.urls')),
    path('partos/', include('partosApp.urls')),

    # Core (en una ruta distinta para evitar colisión con la raíz)
    path('core/', include('core.urls')),

    # Autenticación 2FA
    path('2fa/', include('two_factor.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]