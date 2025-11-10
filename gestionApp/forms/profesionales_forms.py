"""
FORMULARIOS DE PROFESIONALES - VERSIÓN ACTUALIZADA
Formularios para Médico, Matrona y TENS
Incluyen validación de RUT con campos separados
"""

from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Medico, Matrona, Tens
from utilidad.rut_validator import normalizar_rut, RutValidator


# ============================================
# FORMULARIO DE MÉDICO
# ============================================

class MedicoForm(forms.ModelForm):
    """
    Formulario para vincular rol de Médico a una Persona existente.
    """
    
    # Campos para buscar la persona por RUT
    rut_persona_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT de la Persona',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'pattern': '[0-9]{7,8}'
        }),
        help_text='Ingrese el RUT de la persona a vincular como médico'
    )
    
    rut_persona_dv = forms.CharField(
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
    
    class Meta:
        model = Medico
        fields = [
            'Especialidad',
            'Registro_medico',
            'Años_experiencia',
            'Turno',
            'Activo'
        ]
        
        widgets = {
            'Especialidad': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Registro_medico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: RM-12345',
                'required': True
            }),
            'Años_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '60',
                'required': True
            }),
            'Turno': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'Especialidad': 'Especialidad Médica',
            'Registro_medico': 'Registro Médico',
            'Años_experiencia': 'Años de Experiencia',
            'Turno': 'Turno de Trabajo',
            'Activo': '¿Médico Activo?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si estamos editando
        if self.instance and self.instance.pk and hasattr(self.instance, 'persona'):
            datos_rut = RutValidator.separar(self.instance.persona.Rut)
            self.fields['rut_persona_cuerpo'].initial = datos_rut['cuerpo']
            self.fields['rut_persona_dv'].initial = datos_rut['dv']
            self.fields['rut_persona_cuerpo'].disabled = True
            self.fields['rut_persona_dv'].disabled = True
            self.fields['rut_persona_cuerpo'].widget.attrs['class'] += ' bg-light'
            self.fields['rut_persona_dv'].widget.attrs['class'] += ' bg-light'
    
    def clean_Registro_medico(self):
        """Validar que el registro médico sea único"""
        registro = self.cleaned_data.get('Registro_medico')
        
        # Si estamos editando, excluir el registro actual
        if self.instance and self.instance.pk:
            if Medico.objects.filter(Registro_medico=registro).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Este número de registro médico ya existe.')
        else:
            if Medico.objects.filter(Registro_medico=registro).exists():
                raise ValidationError('Este número de registro médico ya existe.')
        
        return registro
    
    def clean(self):
        cleaned_data = super().clean()
        
        # No validar RUT si estamos editando
        if self.instance and self.instance.pk:
            return cleaned_data
        
        rut_cuerpo = cleaned_data.get('rut_persona_cuerpo')
        rut_dv = cleaned_data.get('rut_persona_dv')
        
        if rut_cuerpo and rut_dv:
            rut_completo = f"{rut_cuerpo}-{rut_dv}"
            rut_normalizado = normalizar_rut(rut_completo)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                if hasattr(persona, 'medico'):
                    raise ValidationError({
                        'rut_persona_cuerpo': 'Esta persona ya está registrada como médico.'
                    })
                
                self._persona_obj = persona
                
            except Persona.DoesNotExist:
                raise ValidationError({
                    'rut_persona_cuerpo': (
                        'No existe una persona registrada con este RUT. '
                        'Registre primero los datos básicos de la persona.'
                    )
                })
        
        return cleaned_data
    
    def save(self, commit=True):
        medico = super().save(commit=False)
        
        if not self.instance.pk:
            persona = getattr(self, '_persona_obj', None)
            if persona:
                medico.persona = persona
        
        if commit:
            medico.save()
        
        return medico


# ============================================
# FORMULARIO DE MATRONA
# ============================================

class MatronaForm(forms.ModelForm):
    """
    Formulario para vincular rol de Matrona a una Persona existente.
    """
    
    rut_persona_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT de la Persona',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'pattern': '[0-9]{7,8}'
        }),
        help_text='Ingrese el RUT de la persona a vincular como matrona'
    )
    
    rut_persona_dv = forms.CharField(
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
    
    class Meta:
        model = Matrona
        fields = [
            'Especialidad',
            'Registro_medico',
            'Años_experiencia',
            'Turno',
            'Activo'
        ]
        
        widgets = {
            'Especialidad': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Registro_medico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: MAT-12345',
                'required': True
            }),
            'Años_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '60',
                'required': True
            }),
            'Turno': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'Especialidad': 'Especialidad',
            'Registro_medico': 'Registro Profesional',
            'Años_experiencia': 'Años de Experiencia',
            'Turno': 'Turno de Trabajo',
            'Activo': '¿Matrona Activa?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk and hasattr(self.instance, 'persona'):
            datos_rut = RutValidator.separar(self.instance.persona.Rut)
            self.fields['rut_persona_cuerpo'].initial = datos_rut['cuerpo']
            self.fields['rut_persona_dv'].initial = datos_rut['dv']
            self.fields['rut_persona_cuerpo'].disabled = True
            self.fields['rut_persona_dv'].disabled = True
            self.fields['rut_persona_cuerpo'].widget.attrs['class'] += ' bg-light'
            self.fields['rut_persona_dv'].widget.attrs['class'] += ' bg-light'
    
    def clean_Registro_medico(self):
        registro = self.cleaned_data.get('Registro_medico')
        
        if self.instance and self.instance.pk:
            if Matrona.objects.filter(Registro_medico=registro).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Este número de registro ya existe.')
        else:
            if Matrona.objects.filter(Registro_medico=registro).exists():
                raise ValidationError('Este número de registro ya existe.')
        
        return registro
    
    def clean(self):
        cleaned_data = super().clean()
        
        if self.instance and self.instance.pk:
            return cleaned_data
        
        rut_cuerpo = cleaned_data.get('rut_persona_cuerpo')
        rut_dv = cleaned_data.get('rut_persona_dv')
        
        if rut_cuerpo and rut_dv:
            rut_completo = f"{rut_cuerpo}-{rut_dv}"
            rut_normalizado = normalizar_rut(rut_completo)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                if hasattr(persona, 'matrona'):
                    raise ValidationError({
                        'rut_persona_cuerpo': 'Esta persona ya está registrada como matrona.'
                    })
                
                self._persona_obj = persona
                
            except Persona.DoesNotExist:
                raise ValidationError({
                    'rut_persona_cuerpo': (
                        'No existe una persona registrada con este RUT. '
                        'Registre primero los datos básicos de la persona.'
                    )
                })
        
        return cleaned_data
    
    def save(self, commit=True):
        matrona = super().save(commit=False)
        
        if not self.instance.pk:
            persona = getattr(self, '_persona_obj', None)
            if persona:
                matrona.persona = persona
        
        if commit:
            matrona.save()
        
        return matrona


# ============================================
# FORMULARIO DE TENS
# ============================================

class TensForm(forms.ModelForm):
    """
    Formulario para vincular rol de TENS a una Persona existente.
    """
    
    rut_persona_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT de la Persona',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'pattern': '[0-9]{7,8}'
        }),
        help_text='Ingrese el RUT de la persona a vincular como TENS'
    )
    
    rut_persona_dv = forms.CharField(
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
    
    class Meta:
        model = Tens
        fields = [
            'Nivel',
            'Años_experiencia',
            'Turno',
            'Certificaciones',
            'Activo'
        ]
        
        widgets = {
            'Nivel': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Años_experiencia': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '60',
                'required': True
            }),
            'Turno': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Certificaciones': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'Nivel': 'Nivel TENS',
            'Años_experiencia': 'Años de Experiencia',
            'Turno': 'Turno de Trabajo',
            'Certificaciones': 'Certificaciones',
            'Activo': '¿TENS Activo?'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance and self.instance.pk and hasattr(self.instance, 'persona'):
            datos_rut = RutValidator.separar(self.instance.persona.Rut)
            self.fields['rut_persona_cuerpo'].initial = datos_rut['cuerpo']
            self.fields['rut_persona_dv'].initial = datos_rut['dv']
            self.fields['rut_persona_cuerpo'].disabled = True
            self.fields['rut_persona_dv'].disabled = True
            self.fields['rut_persona_cuerpo'].widget.attrs['class'] += ' bg-light'
            self.fields['rut_persona_dv'].widget.attrs['class'] += ' bg-light'
    
    def clean(self):
        cleaned_data = super().clean()
        
        if self.instance and self.instance.pk:
            return cleaned_data
        
        rut_cuerpo = cleaned_data.get('rut_persona_cuerpo')
        rut_dv = cleaned_data.get('rut_persona_dv')
        
        if rut_cuerpo and rut_dv:
            rut_completo = f"{rut_cuerpo}-{rut_dv}"
            rut_normalizado = normalizar_rut(rut_completo)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                if hasattr(persona, 'tens'):
                    raise ValidationError({
                        'rut_persona_cuerpo': 'Esta persona ya está registrada como TENS.'
                    })
                
                self._persona_obj = persona
                
            except Persona.DoesNotExist:
                raise ValidationError({
                    'rut_persona_cuerpo': (
                        'No existe una persona registrada con este RUT. '
                        'Registre primero los datos básicos de la persona.'
                    )
                })
        
        return cleaned_data
    
    def save(self, commit=True):
        tens = super().save(commit=False)
        
        if not self.instance.pk:
            persona = getattr(self, '_persona_obj', None)
            if persona:
                tens.persona = persona
        
        if commit:
            tens.save()
        
        return tens
