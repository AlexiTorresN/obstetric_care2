# gestionApp/forms/Gestion_form.py
from django import forms
from django.core.exceptions import ValidationError
from gestionApp.models import Persona, Medico, Matrona, Tens, Paciente
from utilidad.rut_validator import validar_rut_chileno, normalizar_rut
from datetime import date


# ============================================
# FORMULARIO DE PERSONA
# ============================================

class PersonaForm(forms.ModelForm):
    """Formulario para registro de personas (datos básicos)"""
    
    class Meta:
        model = Persona
        fields = [
            'Rut', 'Nombre', 'Apellido_Paterno', 'Apellido_Materno', 
            'Sexo', 'Fecha_nacimiento', 'Telefono', 'Direccion', 'Email'
        ]
        widgets = {
            'Rut': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '12345678-9',
                'maxlength': '12',
                'id': 'rut_input',
                'required': True
            }),
            'Nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre',
                'required': True
            }),
            'Apellido_Paterno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido paterno',
                'required': True
            }),
            'Apellido_Materno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese apellido materno',
                'required': True
            }),
            'Sexo': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'Telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            }),
            'Direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle, número, comuna'
            }),
            'Email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            })
        }
        labels = {
            'Rut': 'RUT',
            'Nombre': 'Nombre',
            'Apellido_Paterno': 'Apellido Paterno',
            'Apellido_Materno': 'Apellido Materno',
            'Sexo': 'Sexo',
            'Fecha_nacimiento': 'Fecha de Nacimiento',
            'Telefono': 'Teléfono',
            'Direccion': 'Dirección',
            'Email': 'Correo Electrónico'
        }
    
    def clean_Rut(self):
        """Validación y normalización del RUT"""
        rut = self.cleaned_data.get('Rut')
        if not rut:
            raise ValidationError('El RUT es obligatorio.')
        
        try:
            # Normalizar primero
            rut_normalizado = normalizar_rut(rut)
            
            # Validar formato y dígito verificador
            validar_rut_chileno(rut_normalizado)
            
            # Verificar duplicados solo al crear (no al editar)
            if not self.instance.pk:
                if Persona.objects.filter(Rut=rut_normalizado).exists():
                    raise ValidationError('Este RUT ya está registrado.')
            
            return rut_normalizado
            
        except ValidationError as e:
            raise e
        except Exception as e:
            raise ValidationError(f'Error al validar RUT: {str(e)}')
    
    def clean_Fecha_nacimiento(self):
        """Validar que la fecha de nacimiento sea coherente"""
        fecha = self.cleaned_data.get('Fecha_nacimiento')
        if not fecha:
            raise ValidationError('La fecha de nacimiento es obligatoria.')
        
        hoy = date.today()
        edad = hoy.year - fecha.year - ((hoy.month, hoy.day) < (fecha.month, fecha.day))
        
        if edad < 0:
            raise ValidationError('La fecha de nacimiento no puede ser futura.')
        if edad > 120:
            raise ValidationError('La fecha de nacimiento no es válida.')
        
        return fecha
    
    def clean_Nombre(self):
        """Validar que el nombre no esté vacío"""
        nombre = self.cleaned_data.get('Nombre', '').strip()
        if not nombre:
            raise ValidationError('El nombre es obligatorio.')
        return nombre.title()
    
    def clean_Apellido_Paterno(self):
        """Validar apellido paterno"""
        apellido = self.cleaned_data.get('Apellido_Paterno', '').strip()
        if not apellido:
            raise ValidationError('El apellido paterno es obligatorio.')
        return apellido.title()
    
    def clean_Apellido_Materno(self):
        """Validar apellido materno"""
        apellido = self.cleaned_data.get('Apellido_Materno', '').strip()
        if not apellido:
            raise ValidationError('El apellido materno es obligatorio.')
        return apellido.title()
    
    def save(self, commit=True):
        """Guardar la persona con validaciones adicionales"""
        persona = super().save(commit=False)
        
        # Establecer Activo por defecto si no está definido
        if persona.Activo is None:
            persona.Activo = True
        
        if commit:
            try:
                persona.save()
                print(f"✅ Persona guardada exitosamente: {persona.Rut}")
            except Exception as e:
                print(f"❌ Error al guardar persona: {str(e)}")
                raise ValidationError(f'Error al guardar: {str(e)}')
        
        return persona


# ============================================
# FORMULARIO DE PACIENTE
# ============================================

class PacienteForm(forms.ModelForm):
    """Formulario para vincular paciente a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_paciente',
            'autocomplete': 'off'
        }),
        help_text="Ingrese el RUT de la persona a vincular como paciente"
    )
    
    class Meta:
        model = Paciente
        fields = [ 'persona', 'Estado_civil', 'Previcion', 'Acompañante', 'Contacto_emergencia' ]
        widgets = {

            'Estado_civil': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Previcion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'Acompañante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del acompañante'
            }),
            'Contacto_emergencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56912345678'
            })
        }
        labels = {
            'Edad': 'Edad',
            'Estado_civil': 'Estado Civil',
            'Previcion': 'Previsión',
            'Acompañante': 'Acompañante',
            'Contacto_emergencia': 'Contacto de Emergencia'
        }
    
    def clean_rut_persona(self):
        """Validar que la persona exista y no sea ya paciente"""
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                
                # Verificar si ya tiene el rol de paciente
                if hasattr(persona, 'paciente'):
                    raise ValidationError('Esta persona ya está registrada como paciente.')
                
                # Guardar el objeto persona para usarlo en save()
                self._persona_obj = persona
                return persona
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No existe una persona registrada con este RUT. '
                    'Por favor, registre primero los datos básicos de la persona.'
                )
        return rut
    
    def clean_Edad(self):
        """Validar rango de edad"""
        edad = self.cleaned_data.get('Edad')
        if edad:
            if edad < 12 or edad > 60:
                raise ValidationError('La edad debe estar entre 12 y 60 años.')
        return edad
    
    def save(self, commit=True):
        """Guardar el paciente vinculando la persona"""
        paciente = super().save(commit=False)
        
        # Obtener el objeto persona desde el campo limpio
        persona = getattr(self, '_persona_obj', None)
        if persona is None:
            raise ValidationError('Debe seleccionar una persona válida.')
        
        # Vincular la persona al paciente
        paciente.persona = persona
        
        if commit:
            try:
                paciente.save()
                print(f"✅ Paciente guardado exitosamente: {persona.Rut}")
            except Exception as e:
                print(f"❌ Error al guardar paciente: {str(e)}")
                raise ValidationError(f'Error al guardar: {str(e)}')
        
        return paciente


# ============================================
# FORMULARIO DE MÉDICO
# ============================================

class MedicoForm(forms.ModelForm):
    """Formulario para vincular médico a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_medico'
        }),
        help_text="Ingrese el RUT de la persona a vincular como médico"
    )
    
    class Meta:
        model = Medico
        fields = ['Especialidad', 'Registro_medico', 'Años_experiencia', 'Turno']
        widgets = {
            'Especialidad': forms.Select(attrs={'class': 'form-select'}),
            'Registro_medico': forms.TextInput(attrs={'class': 'form-control'}),
            'Años_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'Turno': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_rut_persona(self):
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                if hasattr(persona, 'medico'):
                    raise ValidationError('Esta persona ya está registrada como médico.')
                self._persona_obj = persona
                return persona
            except Persona.DoesNotExist:
                raise ValidationError('No existe una persona registrada con este RUT.')
        return rut
    
    def clean_Registro_medico(self):
        registro = self.cleaned_data.get('Registro_medico')
        if registro and Medico.objects.filter(Registro_medico=registro).exists():
            raise ValidationError('Este número de registro médico ya existe.')
        return registro
    
    def save(self, commit=True):
        medico = super().save(commit=False)
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
    """Formulario para vincular matrona a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_matrona'
        }),
        help_text="Ingrese el RUT de la persona a vincular como matrona"
    )
    
    class Meta:
        model = Matrona
        fields = ['Especialidad', 'Registro_medico', 'Años_experiencia', 'Turno']
        widgets = {
            'Especialidad': forms.Select(attrs={'class': 'form-select'}),
            'Registro_medico': forms.TextInput(attrs={'class': 'form-control'}),
            'Años_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'Turno': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_rut_persona(self):
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                if hasattr(persona, 'matrona'):
                    raise ValidationError('Esta persona ya está registrada como matrona.')
                self._persona_obj = persona
                return persona
            except Persona.DoesNotExist:
                raise ValidationError('No existe una persona registrada con este RUT.')
        return rut
    
    def clean_Registro_medico(self):
        registro = self.cleaned_data.get('Registro_medico')
        if registro and Matrona.objects.filter(Registro_medico=registro).exists():
            raise ValidationError('Este número de registro ya existe.')
        return registro
    
    def save(self, commit=True):
        matrona = super().save(commit=False)
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
    """Formulario para vincular TENS a una persona existente"""
    
    rut_persona = forms.CharField(
        max_length=12,
        label="RUT de la Persona",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12345678-9',
            'id': 'rut_persona_tens'
        }),
        help_text="Ingrese el RUT de la persona a vincular como TENS"
    )
    
    class Meta:
        model = Tens
        fields = ['Nivel', 'Años_experiencia', 'Turno', 'Certificaciones']
        widgets = {
            'Nivel': forms.Select(attrs={'class': 'form-select'}),
            'Años_experiencia': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'Turno': forms.Select(attrs={'class': 'form-select'}),
            'Certificaciones': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_rut_persona(self):
        rut = self.cleaned_data.get('rut_persona')
        if rut:
            rut_normalizado = normalizar_rut(rut)
            try:
                persona = Persona.objects.get(Rut=rut_normalizado)
                if hasattr(persona, 'tens'):
                    raise ValidationError('Esta persona ya está registrada como TENS.')
                self._persona_obj = persona
                return persona
            except Persona.DoesNotExist:
                raise ValidationError('No existe una persona registrada con este RUT.')
        return rut
    
    def save(self, commit=True):
        tens = super().save(commit=False)
        persona = getattr(self, '_persona_obj', None)
        if persona:
            tens.persona = persona
        if commit:
            tens.save()
        return tens