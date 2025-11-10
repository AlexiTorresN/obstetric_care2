from django import forms
from django.core.exceptions import ValidationError
from matronaApp.models import AdministracionMedicamento, MedicamentoFicha
from gestionApp.models import Tens
from django.utils import timezone


# ============================================
# FORMULARIO: ADMINISTRACIÓN DE MEDICAMENTO
# ============================================
class AdministracionMedicamentoForm(forms.ModelForm):
    """Formulario para registrar la administración de medicamentos por TENS"""
    
    medicamento_ficha_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    class Meta:
        model = AdministracionMedicamento
        fields = [
            'medicamento_ficha_id',
            'tens',
            'fecha_hora_administracion',
            'se_realizo_lavado',
            'administrado_exitosamente',
            'observaciones',
            'reacciones_adversas',
            'motivo_no_administracion',
        ]
        
        widgets = {
            'tens': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_hora_administracion': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }, format='%Y-%m-%dT%H:%M'),
            'se_realizo_lavado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'administrado_exitosamente': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
                'id': 'id_administrado_exitosamente'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones durante la administración'
            }),
            'reacciones_adversas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa cualquier reacción adversa observada',
                'id': 'id_reacciones_adversas'
            }),
            'motivo_no_administracion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Explique por qué no se administró el medicamento',
                'id': 'id_motivo_no_administracion'
            }),
        }
        
        labels = {
            'tens': 'TENS que Administra',
            'fecha_hora_administracion': 'Fecha y Hora de Administración',
            'se_realizo_lavado': '¿Se realizó lavado de manos?',
            'administrado_exitosamente': '¿Se administró exitosamente?',
            'observaciones': 'Observaciones',
            'reacciones_adversas': 'Reacciones Adversas',
            'motivo_no_administracion': 'Motivo de No Administración',
        }
        
        help_texts = {
            'fecha_hora_administracion': 'Fecha y hora exacta de la administración',
            'se_realizo_lavado': 'Protocolo de seguridad',
            'administrado_exitosamente': 'Marque si el medicamento se administró correctamente',
            'reacciones_adversas': 'Documentar cualquier reacción inmediata del paciente',
            'motivo_no_administracion': 'Completar SOLO si NO se administró',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configurar formato de datetime
        self.fields['fecha_hora_administracion'].input_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%d %H:%M:%S']
        
        # Filtrar solo TENS activos
        self.fields['tens'].queryset = Tens.objects.filter(
            Activo=True
        ).select_related('persona')
        
        # Hacer campos opcionales
        self.fields['observaciones'].required = False
        self.fields['reacciones_adversas'].required = False
        self.fields['motivo_no_administracion'].required = False
        
        # Valores por defecto
        if not self.instance.pk:
            self.initial['fecha_hora_administracion'] = timezone.now()
            self.initial['administrado_exitosamente'] = True
            self.initial['se_realizo_lavado'] = True
    
    def clean_medicamento_ficha_id(self):
        """Validar que el medicamento exista y esté activo"""
        pk = self.cleaned_data.get('medicamento_ficha_id')
        try:
            medicamento = MedicamentoFicha.objects.get(pk=pk, activo=True)
        except (MedicamentoFicha.DoesNotExist, TypeError, ValueError):
            raise ValidationError('Debe seleccionar un medicamento válido.')
        
        self._medicamento_obj = medicamento
        return pk
    
    def clean_fecha_hora_administracion(self):
        """Validar fecha y hora de administración"""
        fecha_hora = self.cleaned_data.get('fecha_hora_administracion')
        if fecha_hora:
            # No puede ser futura
            if fecha_hora > timezone.now():
                raise ValidationError('La fecha y hora de administración no puede ser futura.')
            
            # No puede ser demasiado antigua (más de 7 días)
            diferencia_dias = (timezone.now() - fecha_hora).days
            if diferencia_dias > 7:
                raise ValidationError('La fecha de administración no puede ser mayor a 7 días en el pasado.')
        
        return fecha_hora
    
    def clean(self):
        """Validaciones cruzadas"""
        cleaned_data = super().clean()
        
        administrado = cleaned_data.get('administrado_exitosamente')
        motivo_no_admin = cleaned_data.get('motivo_no_administracion')
        
        # Si NO se administró, debe especificar motivo
        if not administrado:
            if not motivo_no_admin or motivo_no_admin.strip() == '':
                raise ValidationError({
                    'motivo_no_administracion': 'Debe especificar el motivo si el medicamento NO se administró exitosamente.'
                })
        
        # Si SÍ se administró, limpiar motivo de no administración
        if administrado:
            cleaned_data['motivo_no_administracion'] = ''
        
        return cleaned_data
    
    def save(self, commit=True):
        """Guardar administración con el medicamento correcto"""
        administracion = super().save(commit=False)
        
        # Asignar el medicamento desde el campo oculto
        medicamento = getattr(self, '_medicamento_obj', None)
        if medicamento:
            administracion.medicamento_ficha = medicamento
        
        if commit:
            administracion.save()
        
        return administracion


# ============================================
# FORMULARIO: REGISTRO RÁPIDO DE ADMINISTRACIÓN
# ============================================
class RegistroRapidoAdministracionForm(forms.ModelForm):
    """Formulario simplificado para registro rápido de administración"""
    
    medicamento_ficha_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    class Meta:
        model = AdministracionMedicamento
        fields = [
            'medicamento_ficha_id',
            'tens',
            'se_realizo_lavado',
            'observaciones',
        ]
        
        widgets = {
            'tens': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'se_realizo_lavado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Observaciones (opcional)'
            }),
        }
        
        labels = {
            'tens': 'TENS',
            'se_realizo_lavado': '¿Lavado de manos?',
            'observaciones': 'Observaciones',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar solo TENS activos
        self.fields['tens'].queryset = Tens.objects.filter(
            Activo=True
        ).select_related('persona')
        
        self.fields['observaciones'].required = False
        
        # Valores por defecto
        if not self.instance.pk:
            self.initial['se_realizo_lavado'] = True
    
    def clean_medicamento_ficha_id(self):
        """Validar que el medicamento exista"""
        pk = self.cleaned_data.get('medicamento_ficha_id')
        try:
            medicamento = MedicamentoFicha.objects.get(pk=pk, activo=True)
        except (MedicamentoFicha.DoesNotExist, TypeError, ValueError):
            raise ValidationError('Debe seleccionar un medicamento válido.')
        
        self._medicamento_obj = medicamento
        return pk
    
    def save(self, commit=True):
        """Guardar con valores por defecto"""
        administracion = super().save(commit=False)
        
        # Asignar valores automáticos
        medicamento = getattr(self, '_medicamento_obj', None)
        if medicamento:
            administracion.medicamento_ficha = medicamento
        
        administracion.fecha_hora_administracion = timezone.now()
        administracion.administrado_exitosamente = True
        
        if commit:
            administracion.save()
        
        return administracion


# ============================================
# FORMULARIO: REPORTAR REACCIÓN ADVERSA
# ============================================
class ReportarReaccionAdversaForm(forms.Form):
    """Formulario para reportar una reacción adversa post-administración"""
    
    reacciones_adversas = forms.CharField(
        label="Descripción de Reacciones Adversas",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describa detalladamente las reacciones adversas observadas',
            'required': True
        })
    )
    
    def clean_reacciones_adversas(self):
        """Validar que la descripción no esté vacía"""
        reacciones = self.cleaned_data.get('reacciones_adversas')
        if not reacciones or reacciones.strip() == '':
            raise ValidationError('Debe describir las reacciones adversas.')
        return reacciones.strip()