"""
FORMULARIO DE PACIENTE - VERSIÓN ACTUALIZADA
Formulario para vincular rol de Paciente a una Persona existente
Incluye validación de RUT y campos específicos de paciente
"""

from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona
from matronaApp.models import Paciente
from utilidad.rut_validator import normalizar_rut, RutValidator
from datetime import date


class PacienteForm(forms.ModelForm):
    """
    Formulario para registrar un paciente vinculado a una persona existente.
    El paciente debe estar previamente registrado como Persona.
    """
    
    # Campo para buscar la persona por RUT
    rut_persona_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT de la Persona',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'id': 'rut_persona_cuerpo',
            'pattern': '[0-9]{7,8}'
        }),
        help_text='Ingrese el RUT de la persona a vincular como paciente'
    )
    
    rut_persona_dv = forms.CharField(
        max_length=1,
        required=True,
        label='DV',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'K',
            'id': 'rut_persona_dv',
            'maxlength': '1',
            'pattern': '[0-9Kk]',
            'style': 'text-transform: uppercase;'
        }),
        help_text='DV'
    )
    
    class Meta:
        model = Paciente
        fields = [
            'Estado_civil',
            'Previcion',
            'paridad',
            'Ductus_Venosus',
            'control_prenatal',
            'consultorio',
            'imc',
            'alergias',
            'observaciones'
        ]
        
        widgets = {
            'Estado_civil': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Previcion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'paridad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: G3P2A0',
                'title': 'Formato: G(gestas)P(partos)A(abortos)'
            }),
            'Ductus_Venosus': forms.Select(attrs={
                'class': 'form-select'
            }),
            'control_prenatal': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_control_prenatal'
            }),
            'consultorio': forms.Select(attrs={
                'class': 'form-select'
            }),
            'imc': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 24.5',
                'step': '0.1',
                'min': '10',
                'max': '60'
            }),
            'alergias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Alergias conocidas (medicamentos, alimentos, etc.)'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Información médica adicional relevante...'
            })
        }
        
        labels = {
            'Estado_civil': 'Estado Civil',
            'Previcion': 'Previsión de Salud',
            'paridad': 'Paridad',
            'Ductus_Venosus': 'Ductus Venosus',
            'control_prenatal': '¿Tuvo Control Prenatal?',
            'consultorio': 'Consultorio de Atención',
            'imc': 'IMC (Índice de Masa Corporal)',
            'alergias': 'Alergias',
            'observaciones': 'Observaciones Médicas'
        }
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario.
        Si se está editando un paciente existente, muestra su RUT.
        """
        super().__init__(*args, **kwargs)
        
        # Si estamos editando un paciente existente
        if self.instance and self.instance.pk and hasattr(self.instance, 'persona'):
            datos_rut = RutValidator.separar(self.instance.persona.Rut)
            self.fields['rut_persona_cuerpo'].initial = datos_rut['cuerpo']
            self.fields['rut_persona_dv'].initial = datos_rut['dv']
            
            # Deshabilitar campos de RUT al editar
            self.fields['rut_persona_cuerpo'].disabled = True
            self.fields['rut_persona_dv'].disabled = True
            self.fields['rut_persona_cuerpo'].widget.attrs['class'] += ' bg-light'
            self.fields['rut_persona_dv'].widget.attrs['class'] += ' bg-light'
            self.fields['rut_persona_cuerpo'].help_text = 'El RUT no se puede modificar'
    
    def clean_rut_persona_cuerpo(self):
        """Validar el cuerpo del RUT"""
        rut_cuerpo = self.cleaned_data.get('rut_persona_cuerpo', '').strip()
        
        if not rut_cuerpo:
            raise ValidationError('El RUT de la persona es obligatorio.')
        
        if not rut_cuerpo.isdigit():
            raise ValidationError('El RUT debe contener solo números.')
        
        if len(rut_cuerpo) < 7 or len(rut_cuerpo) > 8:
            raise ValidationError('El RUT debe tener 7 u 8 dígitos.')
        
        return rut_cuerpo
    
    def clean_rut_persona_dv(self):
        """Validar el dígito verificador"""
        rut_dv = self.cleaned_data.get('rut_persona_dv', '').strip().upper()
        
        if not rut_dv:
            raise ValidationError('El dígito verificador es obligatorio.')
        
        if len(rut_dv) != 1:
            raise ValidationError('El dígito verificador debe ser un solo carácter.')
        
        if not (rut_dv.isdigit() or rut_dv == 'K'):
            raise ValidationError('El dígito verificador debe ser un número o K.')
        
        return rut_dv
    
    def clean(self):
        """
        Validación completa del formulario.
        Verifica que la persona exista y no sea ya paciente.
        """
        cleaned_data = super().clean()
        
        # No validar RUT si estamos editando
        if self.instance and self.instance.pk:
            return cleaned_data
        
        rut_cuerpo = cleaned_data.get('rut_persona_cuerpo')
        rut_dv = cleaned_data.get('rut_persona_dv')
        
        if rut_cuerpo and rut_dv:
            rut_completo = f"{rut_cuerpo}-{rut_dv}"
            rut_normalizado = normalizar_rut(rut_completo)
            
            # Validar que la persona exista
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                # Verificar que no sea ya paciente
                if hasattr(persona, 'paciente'):
                    raise ValidationError({
                        'rut_persona_cuerpo': f'Esta persona ya está registrada como paciente.'
                    })
                
                # Guardar la persona para usarla en save()
                self._persona_obj = persona
                
            except Persona.DoesNotExist:
                raise ValidationError({
                    'rut_persona_cuerpo': (
                        'No existe una persona registrada con este RUT. '
                        'Por favor, registre primero los datos básicos de la persona.'
                    )
                })
        
        # Validar IMC si se proporciona
        imc = cleaned_data.get('imc')
        if imc:
            if imc < 10 or imc > 60:
                raise ValidationError({
                    'imc': 'El IMC debe estar entre 10 y 60.'
                })
        
        # Validar formato de paridad si se proporciona
        paridad = cleaned_data.get('paridad')
        if paridad:
            import re
            # Formato válido: G#P#A# (ej: G3P2A0)
            if not re.match(r'^G\d+P\d+A\d+$', paridad.upper().replace(' ', '')):
                raise ValidationError({
                    'paridad': 'Formato inválido. Use: G(gestas)P(partos)A(abortos). Ej: G3P2A0'
                })
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Guarda el paciente vinculándolo a la persona.
        """
        paciente = super().save(commit=False)
        
        # Si es nuevo, vincular con la persona
        if not self.instance.pk:
            persona = getattr(self, '_persona_obj', None)
            if persona:
                paciente.persona = persona
        
        if commit:
            paciente.save()
        
        return paciente


class PacienteBuscarForm(forms.Form):
    """
    Formulario simple para buscar un paciente por RUT.
    Útil para búsquedas rápidas en el sistema.
    """
    
    rut_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'autofocus': True,
            'pattern': '[0-9]{7,8}'
        })
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
        """Valida y busca el paciente"""
        cleaned_data = super().clean()
        
        rut_cuerpo = cleaned_data.get('rut_cuerpo')
        rut_dv = cleaned_data.get('rut_dv')
        
        if rut_cuerpo and rut_dv:
            rut_completo = f"{rut_cuerpo}-{rut_dv}"
            rut_normalizado = normalizar_rut(rut_completo)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
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