"""
FORMULARIOS INGRESO PARTO - FICHA DE PARTO
Sistema de formularios para registro de ingreso al proceso de parto
Incluye todas las secciones: datos generales, patologías y tamizajes
"""

from django import forms
from django.core.exceptions import ValidationError
from ingresoPartoApp.models import FichaParto
from matronaApp.models import FichaObstetrica, Paciente
from gestionApp.models import Persona
from utilidad.rut_validator import normalizar_rut, RutValidator
from django.utils import timezone


# ============================================
# FORMULARIO 1: BÚSQUEDA DE PACIENTE POR RUT
# ============================================

class BuscarPacienteIngresoForm(forms.Form):
    """
    Formulario para buscar un paciente por RUT antes de crear la ficha de parto.
    Útil para vincular la ficha de ingreso con la ficha obstétrica existente.
    """
    
    rut_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT del Paciente',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
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
            'class': 'form-control',
            'placeholder': 'K',
            'maxlength': '1',
            'pattern': '[0-9Kk]',
            'style': 'text-transform: uppercase;'
        })
    )
    
    def clean(self):
        """Valida y busca el paciente con ficha obstétrica activa"""
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
                
                # Buscar ficha obstétrica activa
                fichas = FichaObstetrica.objects.filter(
                    paciente=persona.paciente,
                    activa=True
                )
                
                if not fichas.exists():
                    raise ValidationError(
                        'Esta paciente no tiene una ficha obstétrica activa. '
                        'Debe crear primero una ficha obstétrica.'
                    )
                
                # Guardar datos para uso posterior
                cleaned_data['paciente'] = persona.paciente
                cleaned_data['ficha_obstetrica'] = fichas.first()
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No se encontró ninguna persona con este RUT.'
                )
        
        return cleaned_data


# ============================================
# FORMULARIO 2: DATOS GENERALES DEL INGRESO
# ============================================

class DatosGeneralesIngresoForm(forms.ModelForm):
    """
    Formulario para la sección de datos generales del ingreso.
    Primera parte del registro de ingreso al parto.
    """
    
    class Meta:
        model = FichaParto
        fields = [
            'ficha_obstetrica',
            'tipo_paciente',
            'origen_ingreso',
            'fecha_ingreso',
            'hora_ingreso',
            'plan_de_parto',
            'visita_guiada',
            'control_prenatal',
            'consultorio_origen'
        ]
        
        widgets = {
            'ficha_obstetrica': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'tipo_paciente': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'origen_ingreso': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
                'value': timezone.now().strftime('%Y-%m-%d')
            }),
            'hora_ingreso': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'required': True,
                'value': timezone.now().strftime('%H:%M')
            }),
            'plan_de_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_plan_parto'
            }),
            'visita_guiada': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_visita_guiada'
            }),
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_control_prenatal'
            }),
            'consultorio_origen': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: CESFAM Los Volcanes'
            })
        }
        
        labels = {
            'ficha_obstetrica': 'Ficha Obstétrica',
            'tipo_paciente': 'Tipo de Paciente',
            'origen_ingreso': 'Origen del Ingreso',
            'fecha_ingreso': 'Fecha de Ingreso',
            'hora_ingreso': 'Hora de Ingreso',
            'plan_de_parto': '¿Tiene Plan de Parto?',
            'visita_guiada': '¿Realizó Visita Guiada?',
            'control_prenatal': '¿Tuvo Control Prenatal?',
            'consultorio_origen': 'Consultorio de Origen'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo fichas obstétricas activas
        self.fields['ficha_obstetrica'].queryset = FichaObstetrica.objects.filter(
            activa=True
        ).select_related('paciente__persona')


# ============================================
# FORMULARIO 3: PATOLOGÍAS AL INGRESO
# ============================================

class PatologiasIngresoForm(forms.ModelForm):
    """
    Formulario para registrar patologías presentes al momento del ingreso.
    Segunda parte del registro de ingreso.
    """
    
    class Meta:
        model = FichaParto
        fields = [
            'preeclampsia_severa',
            'eclampsia',
            'sepsis_infeccion_grave',
            'infeccion_ovular',
            'otra_patologia'
        ]
        
        widgets = {
            'preeclampsia_severa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'eclampsia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sepsis_infeccion_grave': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'infeccion_ovular': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'otra_patologia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especifique otra patología si aplica'
            })
        }
        
        labels = {
            'preeclampsia_severa': 'Preeclampsia Severa',
            'eclampsia': 'Eclampsia',
            'sepsis_infeccion_grave': 'Sepsis o Infección Sistémica Grave',
            'infeccion_ovular': 'Infección Ovular o Corioamnionitis',
            'otra_patologia': 'Otra Patología'
        }


# ============================================
# FORMULARIO 4: TAMIZAJE VIH
# ============================================

class TamizajeVIHForm(forms.ModelForm):
    """
    Formulario para registrar tamizaje de VIH al ingreso.
    """
    
    class Meta:
        model = FichaParto
        fields = [
            'numero_aro',
            'vih_tomado_prepartos',
            'vih_tomado_sala',
            'vih_orden_toma'
        ]
        
        widgets = {
            'numero_aro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: ARO-2024-001'
            }),
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_vih_prepartos'
            }),
            'vih_tomado_sala': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_vih_sala'
            }),
            'vih_orden_toma': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        
        labels = {
            'numero_aro': 'Número ARO',
            'vih_tomado_prepartos': '¿Se tomó VIH en Prepartos?',
            'vih_tomado_sala': '¿Se tomó VIH en Sala?',
            'vih_orden_toma': 'Orden de Toma (1°, 2°, 3°)'
        }
    
    def clean(self):
        """Validar que si se marca toma de VIH, se especifique el orden"""
        cleaned_data = super().clean()
        
        vih_prepartos = cleaned_data.get('vih_tomado_prepartos')
        vih_sala = cleaned_data.get('vih_tomado_sala')
        orden_toma = cleaned_data.get('vih_orden_toma')
        
        # Si se marcó alguna toma de VIH, debe especificar el orden
        if (vih_prepartos or vih_sala) and not orden_toma:
            raise ValidationError({
                'vih_orden_toma': 'Debe especificar el orden de toma del VIH.'
            })
        
        return cleaned_data


# ============================================
# FORMULARIO 5: TAMIZAJE SGB
# ============================================

class TamizajeSGBForm(forms.ModelForm):
    """
    Formulario para registrar tamizaje de Streptococcus Grupo B.
    """
    
    class Meta:
        model = FichaParto
        fields = [
            'sgb_pesquisa',
            'sgb_resultado',
            'sgb_medicamentos'
        ]
        
        widgets = {
            'sgb_pesquisa': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_sgb_pesquisa'
            }),
            'sgb_resultado': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_sgb_resultado'
            }),
            'sgb_medicamentos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Detallar medicamentos administrados para SGB'
            })
        }
        
        labels = {
            'sgb_pesquisa': '¿Se realizó Pesquisa SGB?',
            'sgb_resultado': 'Resultado SGB',
            'sgb_medicamentos': 'Medicamentos Administrados'
        }
    
    def clean(self):
        """Validar que si se realizó pesquisa, debe tener resultado"""
        cleaned_data = super().clean()
        
        sgb_pesquisa = cleaned_data.get('sgb_pesquisa')
        sgb_resultado = cleaned_data.get('sgb_resultado')
        
        if sgb_pesquisa and not sgb_resultado:
            raise ValidationError({
                'sgb_resultado': 'Debe ingresar el resultado de la pesquisa SGB.'
            })
        
        return cleaned_data


# ============================================
# FORMULARIO 6: TAMIZAJE VDRL
# ============================================

class TamizajeVDRLForm(forms.ModelForm):
    """
    Formulario para registrar tamizaje VDRL (Sífilis).
    """
    
    class Meta:
        model = FichaParto
        fields = [
            'vdrl_resultado',
            'penicilina_1',
            'penicilina_2',
            'penicilina_3',
            'derivacion_matrona_ssr'
        ]
        
        widgets = {
            'vdrl_resultado': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_vdrl_resultado',
                'required': True
            }),
            'penicilina_1': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'penicilina_2': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'penicilina_3': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'derivacion_matrona_ssr': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'vdrl_resultado': 'Resultado VDRL',
            'penicilina_1': 'Penicilina 1° Dosis',
            'penicilina_2': 'Penicilina 2° Dosis',
            'penicilina_3': 'Penicilina 3° Dosis',
            'derivacion_matrona_ssr': 'Derivación a Matrona SSR'
        }


# ============================================
# FORMULARIO 7: TAMIZAJE HEPATITIS B
# ============================================

class TamizajeHepatitisForm(forms.ModelForm):
    """
    Formulario para registrar tamizaje de Hepatitis B.
    """
    
    class Meta:
        model = FichaParto
        fields = [
            'hepatitis_b_tomado',
            'derivacion_gastro'
        ]
        
        widgets = {
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'derivacion_gastro': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'hepatitis_b_tomado': '¿Se tomó examen de Hepatitis B?',
            'derivacion_gastro': '¿Requiere derivación a Gastro-Hepatólogo?'
        }


# ============================================
# FORMULARIO 8: FORMULARIO COMPLETO
# ============================================

class FichaPartoCompletaForm(forms.ModelForm):
    """
    Formulario completo con todos los campos de la ficha de parto.
    Útil para crear o editar una ficha completa en una sola vista.
    """
    
    class Meta:
        model = FichaParto
        fields = '__all__'
        exclude = ['numero_ficha_parto', 'fecha_creacion', 'fecha_modificacion']
        
        widgets = {
            # Datos Generales
            'ficha_obstetrica': forms.Select(attrs={'class': 'form-select'}),
            'tipo_paciente': forms.Select(attrs={'class': 'form-select'}),
            'origen_ingreso': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'hora_ingreso': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'plan_de_parto': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'visita_guiada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'control_prenatal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'consultorio_origen': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Patologías
            'preeclampsia_severa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'eclampsia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sepsis_infeccion_grave': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'infeccion_ovular': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'otra_patologia': forms.TextInput(attrs={'class': 'form-control'}),
            
            # Tamizaje VIH
            'numero_aro': forms.TextInput(attrs={'class': 'form-control'}),
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_tomado_sala': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vih_orden_toma': forms.Select(attrs={'class': 'form-select'}),
            
            # Tamizaje SGB
            'sgb_pesquisa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sgb_resultado': forms.Select(attrs={'class': 'form-select'}),
            'sgb_medicamentos': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            
            # Tamizaje VDRL
            'vdrl_resultado': forms.Select(attrs={'class': 'form-select'}),
            'penicilina_1': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'penicilina_2': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'penicilina_3': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'derivacion_matrona_ssr': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Tamizaje Hepatitis B
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'derivacion_gastro': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            
            # Estado
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar fichas activas
        self.fields['ficha_obstetrica'].queryset = FichaObstetrica.objects.filter(
            activa=True
        ).select_related('paciente__persona')


# ============================================
# FORMULARIO 9: EDICIÓN RÁPIDA
# ============================================

class FichaPartoEdicionRapidaForm(forms.ModelForm):
    """
    Formulario simplificado para edición rápida de campos comunes.
    """
    
    class Meta:
        model = FichaParto
        fields = [
            'tipo_paciente',
            'origen_ingreso',
            'control_prenatal',
            'consultorio_origen',
            'activa'
        ]
        
        widgets = {
            'tipo_paciente': forms.Select(attrs={'class': 'form-select'}),
            'origen_ingreso': forms.Select(attrs={'class': 'form-select'}),
            'control_prenatal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'consultorio_origen': forms.TextInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
