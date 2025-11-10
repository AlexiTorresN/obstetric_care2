"""
Importaciones centralizadas de formularios de gestionApp
"""
from .Gestion_form import Persona, MedicoForm, MatronaForm, TensForm, PersonaForm, PacienteForm
from .medico_forms import MedicoForm
from .matrona_forms import MatronaForm




__all__ = [
    'gestionApp.forms.Gestion_form',
    'gestionApp.forms.persona_forms',
    'gestionApp.forms.medico_forms',
    'gestionApp.forms.matrona_forms',
    'gestionApp.forms.tens_forms',
]


