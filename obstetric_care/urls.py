from django.contrib import admin
from django.urls import path, include
from inicioApp import views as inicio_views
from core.views import custom_403 

# Handler para rediccion a paginas con errores HTML
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

    # incluimos la nueva app core
    path("", include("core.urls")),

    # incluimos el path para 2FA
    path('', include('two_factor.urls', 'two_factor')),

]   