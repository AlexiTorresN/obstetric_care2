from django import forms
from django.core.exceptions import ValidationError
from medicoApp.models import Patologias
from gestionApp.models import Persona, Paciente
from utilidad.rut_validator import normalizar_rut, RutValidator


# ============================================
# FORMULARIO 1: ACTIVAR/DESACTIVAR PATOLOGÍA
# ============================================

class TogglePatologiaForm(forms.ModelForm):
    """
    Formulario para activar o desactivar una patología del catálogo.
    Las patologías vienen predefinidas, el médico solo las activa/desactiva.
    """
    
    class Meta:
        model = Patologias
        fields = ['estado']
        
        widgets = {
            'estado': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        
        labels = {
            'estado': 'Estado de la Patología'
        }


# ============================================
# FORMULARIO 2: BUSCAR PATOLOGÍAS
# ============================================

class BuscarPatologiaForm(forms.Form):
    """
    Formulario para buscar patologías en el catálogo por nombre o código CIE-10.
    """
    
    busqueda = forms.CharField(
        max_length=200,
        required=False,
        label='Buscar Patología',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre o código CIE-10...',
            'id': 'buscar_patologia'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[
            ('', 'Todos'),
            ('Activo', 'Activas'),
            ('Inactivo', 'Inactivas')
        ],
        required=False,
        label='Estado',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    nivel_riesgo = forms.ChoiceField(
        choices=[
            ('', 'Todos los niveles'),
            ('Bajo', 'Bajo'),
            ('Medio', 'Medio'),
            ('Alto', 'Alto'),
            ('Crítico', 'Crítico')
        ],
        required=False,
        label='Nivel de Riesgo',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


# ============================================
# FORMULARIO 3: FILTRO AVANZADO PATOLOGÍAS
# ============================================

class FiltroPatologiasForm(forms.Form):
    """
    Formulario con filtros avanzados para buscar patologías.
    """
    
    ORDEN_CHOICES = [
        ('nombre', 'Nombre (A-Z)'),
        ('-nombre', 'Nombre (Z-A)'),
        ('nivel_de_riesgo', 'Riesgo (Bajo a Crítico)'),
        ('-nivel_de_riesgo', 'Riesgo (Crítico a Bajo)'),
        ('codigo_cie_10', 'Código CIE-10'),
        ('-fecha_creacion', 'Más recientes')
    ]
    
    busqueda = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre o código...'
        })
    )
    
    estado = forms.ChoiceField(
        choices=[('', 'Todos')] + Patologias.ESTADO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    nivel_riesgo = forms.ChoiceField(
        choices=[('', 'Todos')] + Patologias.NIVEL_RIESGO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    codigo_cie = forms.ChoiceField(
        choices=[('', 'Todos')] + Patologias.CIE_10_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    ordenar_por = forms.ChoiceField(
        choices=ORDEN_CHOICES,
        required=False,
        initial='nombre',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


# ============================================
# FORMULARIO 4: BUSCAR PACIENTE POR RUT
# ============================================

class BuscarPacienteRUTForm(forms.Form):
    """
    Formulario para buscar un paciente por RUT para ver su historial clínico.
    """
    
    rut_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT del Paciente',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': '12345678',
            'autofocus': True,
            'pattern': '[0-9]{7,8}'
        }),
        help_text='Ingrese RUT sin puntos ni guión'
    )
    
    rut_dv = forms.CharField(
        max_length=1,
        required=True,
        label='DV',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'K',
            'maxlength': '1',
            'pattern': '[0-9Kk]',
            'style': 'text-transform: uppercase;'
        })
    )
    
    def clean(self):
        """Valida y busca el paciente"""
        cleaned_data = super().clean()
        
        rut_cuerpo = cleaned_data.get('rut_cuerpo')
        rut_dv = cleaned_data.get('rut_dv')
        
        if rut_cuerpo and rut_dv:
            rut_completo = f"{rut_cuerpo}-{rut_dv}"
            rut_normalizado = normalizar_rut(rut_completo)
            
            try:
                # Buscar persona
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                # Verificar que sea paciente
                if not hasattr(persona, 'paciente'):
                    raise ValidationError(
                        'Esta persona no está registrada como paciente.'
                    )
                
                # Guardar el paciente encontrado
                cleaned_data['paciente'] = persona.paciente
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No se encontró ninguna persona con este RUT.'
                )
        
        return cleaned_data


# ============================================
# FORMULARIO 5: BUSCAR PACIENTE POR NOMBRE
# ============================================

class BuscarPacienteNombreForm(forms.Form):
    """
    Formulario para buscar pacientes por nombre o apellido.
    """
    
    busqueda = forms.CharField(
        max_length=200,
        required=True,
        label='Buscar Paciente',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Nombre, apellido o RUT...',
            'autofocus': True
        }),
        help_text='Puede buscar por nombre, apellido o RUT'
    )


# ============================================
# FORMULARIO 6: FILTRO HISTORIAL CLÍNICO
# ============================================

class FiltroHistorialClinicoForm(forms.Form):
    """
    Formulario para filtrar el historial clínico de un paciente.
    """
    
    fecha_desde = forms.DateField(
        required=False,
        label='Desde',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    fecha_hasta = forms.DateField(
        required=False,
        label='Hasta',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    
    solo_activas = forms.BooleanField(
        required=False,
        initial=True,
        label='Solo fichas activas',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    con_patologias = forms.BooleanField(
        required=False,
        label='Solo con patologías',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


# ============================================
# FORMULARIO 7: NOTAS DEL MÉDICO (OPCIONAL)
# ============================================

class NotaMedicaForm(forms.Form):
    """
    Formulario simple para que el médico agregue notas al historial.
    Este es opcional, solo si quieres implementar esta funcionalidad.
    """
    
    ficha_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    nota = forms.CharField(
        label='Nota Médica',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Observaciones del médico...',
            'required': True
        })
    )
    
    tipo_nota = forms.ChoiceField(
        choices=[
            ('observacion', 'Observación General'),
            ('indicacion', 'Indicación Médica'),
            ('seguimiento', 'Seguimiento'),
            ('derivacion', 'Derivación')
        ],
        label='Tipo de Nota',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )


# ============================================
# FORMULARIO 8: EXPORTAR HISTORIAL
# ============================================

class ExportarHistorialForm(forms.Form):
    """
    Formulario para configurar la exportación del historial clínico.
    """
    
    paciente_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    formato = forms.ChoiceField(
        choices=[
            ('pdf', 'PDF'),
            ('excel', 'Excel'),
            ('csv', 'CSV')
        ],
        initial='pdf',
        label='Formato de Exportación',
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input'
        })
    )
    
    incluir_medicamentos = forms.BooleanField(
        required=False,
        initial=True,
        label='Incluir medicamentos',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    incluir_patologias = forms.BooleanField(
        required=False,
        initial=True,
        label='Incluir patologías',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    
    incluir_examenes = forms.BooleanField(
        required=False,
        initial=True,
        label='Incluir exámenes',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )


# ============================================
# FORMULARIO 9: PATOLOGÍA INFORMACIÓN RÁPIDA
# ============================================

class PatologiaInfoForm(forms.Form):
    """
    Formulario solo para mostrar información de una patología.
    No guarda nada, solo es para consulta rápida.
    """
    
    patologia_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        patologia = kwargs.pop('patologia', None)
        super().__init__(*args, **kwargs)
        
        if patologia:
            self.patologia = patologia
            self.fields['patologia_id'].initial = patologia.pk
