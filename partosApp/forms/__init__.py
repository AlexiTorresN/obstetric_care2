# partosApp/forms/__init__.py
"""
Inicialización de formularios de partosApp
"""

from .registro_parto_forms import (
    RegistroPartoBaseForm,
    TrabajoDePartoForm,
    InformacionPartoForm,
    PuerperioForm,
    AnestesiaAnalgesiaForm,
    ProfesionalesForm,
    RegistroPartoCompletoForm,
)

from .recien_nacido_forms import (
    RegistroRecienNacidoForm,
    DatosRecienNacidoForm,
    ApegoAcompanamientoForm,
)

from .documentos_forms import (
    DocumentosPartoForm,
)

__all__ = [
    # Formularios de Parto
    'RegistroPartoBaseForm',
    'TrabajoDePartoForm',
    'InformacionPartoForm',
    'PuerperioForm',
    'AnestesiaAnalgesiaForm',
    'ProfesionalesForm',
    'RegistroPartoCompletoForm',
    # Formularios de RN
    'RegistroRecienNacidoForm',
    'DatosRecienNacidoForm',
    'ApegoAcompanamientoForm',
    # Formularios de Documentos
    'DocumentosPartoForm',
]