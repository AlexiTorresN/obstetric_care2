"""
FORMULARIO DE PERSONA - VERSIÓN ACTUALIZADA
Formulario base para registrar personas en el sistema
Incluye validación de RUT con campos separados
"""

from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona
from utilidad.rut_validator import validar_rut_chileno, normalizar_rut, RutValidator
from datetime import date


class PersonaForm(forms.ModelForm):
    """
    Formulario para registro y edición de personas.
    Incluye campos separados para RUT y DV para mejor experiencia de usuario.
    """
    
    # Campos adicionales para RUT separado (no están en el modelo)
    rut_cuerpo = forms.CharField(
        max_length=8,
        required=True,
        label='RUT',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678',
            'id': 'rut_cuerpo',
            'pattern': '[0-9]{7,8}',
            'title': 'Ingrese solo números (7 u 8 dígitos)'
        }),
        help_text='Ingrese solo los números del RUT (sin puntos ni guión)'
    )
    
    rut_dv = forms.CharField(
        max_length=1,
        required=True,
        label='DV',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'K',
            'id': 'rut_dv',
            'maxlength': '1',
            'pattern': '[0-9Kk]',
            'title': 'Dígito verificador (0-9 o K)',
            'style': 'text-transform: uppercase;'
        }),
        help_text='Dígito verificador'
    )
    
    class Meta:
        model = Persona
        fields = [
            'Nombre',
            'Apellido_Paterno',
            'Apellido_Materno',
            'Fecha_nacimiento',
            'Sexo',
            'Telefono',
            'Direccion',
            'Email',
            'Inmigrante',
            'Nacionalidad',
            'Pueblos_originarios',
            'Discapacidad',
            'Tipo_de_Discapacidad',
            'Privada_de_Libertad',
            'Trans_masculino',
            'Observaciones'
        ]
        
        widgets = {
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: María José',
                'required': True
            }),
            'Apellido_Paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: González',
                'required': True
            }),
            'Apellido_Materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Pérez',
                'required': True
            }),
            'Fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
                'max': date.today().isoformat()  # No puede ser fecha futura
            }),
            'Sexo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678',
                'pattern': '\+?[0-9]{8,12}',
                'title': 'Ingrese un número de teléfono válido'
            }),
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle Ejemplo #123, Comuna'
            }),
            'Email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ejemplo@correo.com'
            }),
            'Inmigrante': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Nacionalidad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Pueblos_originarios': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Discapacidad': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_discapacidad'
            }),
            'Tipo_de_Discapacidad': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Especifique tipo de discapacidad',
                'id': 'id_tipo_discapacidad'
            }),
            'Privada_de_Libertad': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Trans_masculino': forms.Select(attrs={
                'class': 'form-select'
            }),
            'Observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Información adicional relevante...'
            })
        }
        
        labels = {
            'Nombre': 'Nombre(s)',
            'Apellido_Paterno': 'Apellido Paterno',
            'Apellido_Materno': 'Apellido Materno',
            'Fecha_nacimiento': 'Fecha de Nacimiento',
            'Sexo': 'Sexo',
            'Telefono': 'Teléfono',
            'Direccion': 'Dirección',
            'Email': 'Correo Electrónico',
            'Inmigrante': '¿Es Inmigrante?',
            'Nacionalidad': 'Nacionalidad',
            'Pueblos_originarios': 'Pueblos Originarios',
            'Discapacidad': '¿Tiene Discapacidad?',
            'Tipo_de_Discapacidad': 'Tipo de Discapacidad',
            'Privada_de_Libertad': '¿Privada de Libertad?',
            'Trans_masculino': '¿Trans Masculino?',
            'Observaciones': 'Observaciones'
        }
    
    def __init__(self, *args, **kwargs):
        """
        Inicializa el formulario.
        Si se está editando una persona existente, separa el RUT en cuerpo y DV.
        """
        super().__init__(*args, **kwargs)
        
        # Si estamos editando una persona existente
        if self.instance and self.instance.pk:
            datos_rut = RutValidator.separar(self.instance.Rut)
            self.fields['rut_cuerpo'].initial = datos_rut['cuerpo']
            self.fields['rut_dv'].initial = datos_rut['dv']
    
    def clean_rut_cuerpo(self):
        """Validar que el cuerpo del RUT solo contenga números"""
        rut_cuerpo = self.cleaned_data.get('rut_cuerpo', '').strip()
        
        if not rut_cuerpo:
            raise ValidationError('El RUT es obligatorio.')
        
        # Validar que solo sean números
        if not rut_cuerpo.isdigit():
            raise ValidationError('El RUT debe contener solo números.')
        
        # Validar longitud
        if len(rut_cuerpo) < 7 or len(rut_cuerpo) > 8:
            raise ValidationError('El RUT debe tener 7 u 8 dígitos.')
        
        return rut_cuerpo
    
    def clean_rut_dv(self):
        """Validar el dígito verificador"""
        rut_dv = self.cleaned_data.get('rut_dv', '').strip().upper()
        
        if not rut_dv:
            raise ValidationError('El dígito verificador es obligatorio.')
        
        # Validar que sea un solo carácter
        if len(rut_dv) != 1:
            raise ValidationError('El dígito verificador debe ser un solo carácter.')
        
        # Validar que sea número o K
        if not (rut_dv.isdigit() or rut_dv == 'K'):
            raise ValidationError('El dígito verificador debe ser un número (0-9) o K.')
        
        return rut_dv
    
    def clean(self):
        """
        Validación adicional del formulario.
        Combina RUT y DV, valida el RUT completo.
        """
        cleaned_data = super().clean()
        
        rut_cuerpo = cleaned_data.get('rut_cuerpo')
        rut_dv = cleaned_data.get('rut_dv')
        
        # Si tenemos ambos campos, validar el RUT completo
        if rut_cuerpo and rut_dv:
            rut_completo = f"{rut_cuerpo}-{rut_dv}"
            
            # Validar RUT completo
            try:
                validar_rut_chileno(rut_completo)
            except ValidationError as e:
                raise ValidationError({
                    'rut_dv': 'El dígito verificador no es correcto para este RUT.'
                })
            
            # Normalizar y guardar en el campo Rut del modelo
            cleaned_data['Rut'] = normalizar_rut(rut_completo)
            
            # Verificar si el RUT ya existe (solo si es nuevo o si cambió)
            if not self.instance.pk or self.instance.Rut != cleaned_data['Rut']:
                if Persona.objects.filter(Rut=cleaned_data['Rut']).exists():
                    raise ValidationError({
                        'rut_cuerpo': 'Ya existe una persona registrada con este RUT.'
                    })
        
        # Validar edad
        fecha_nacimiento = cleaned_data.get('Fecha_nacimiento')
        if fecha_nacimiento:
            hoy = date.today()
            edad = hoy.year - fecha_nacimiento.year - (
                (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day)
            )
            
            if edad < 0:
                raise ValidationError({
                    'Fecha_nacimiento': 'La fecha de nacimiento no puede ser futura.'
                })
            
            if edad > 120:
                raise ValidationError({
                    'Fecha_nacimiento': 'La fecha de nacimiento no parece válida.'
                })
        
        # Validar que si tiene discapacidad, especifique el tipo
        if cleaned_data.get('Discapacidad') == 'Si':
            if not cleaned_data.get('Tipo_de_Discapacidad'):
                raise ValidationError({
                    'Tipo_de_Discapacidad': 'Debe especificar el tipo de discapacidad.'
                })
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Guarda la persona en la base de datos.
        El RUT ya está normalizado en el método clean().
        """
        persona = super().save(commit=False)
        
        # El RUT ya fue normalizado en clean()
        # No necesitamos hacer nada adicional aquí
        
        if commit:
            persona.save()
        
        return persona


class PersonaUpdateForm(PersonaForm):
    """
    Formulario para actualizar una persona existente.
    Hereda de PersonaForm pero no permite cambiar el RUT.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Deshabilitar campos de RUT para edición
        self.fields['rut_cuerpo'].disabled = True
        self.fields['rut_dv'].disabled = True
        self.fields['rut_cuerpo'].help_text = 'El RUT no se puede modificar'
        self.fields['rut_dv'].help_text = ''
        
        # Agregar clases para indicar que están deshabilitados
        self.fields['rut_cuerpo'].widget.attrs['class'] += ' bg-light'
        self.fields['rut_dv'].widget.attrs['class'] += ' bg-light'