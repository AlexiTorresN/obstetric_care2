from django import forms
from django.core.exceptions import ValidationError
from matronaApp.models import FichaObstetrica, MedicamentoFicha, IngresoPaciente
from gestionApp.models import Persona, Paciente, Matrona
from medicoApp.models import Patologias
from utilidad.rut_validator import normalizar_rut, RutValidator
from django.utils import timezone
from datetime import date


# ============================================
# FORMULARIO 1: BÚSQUEDA DE PACIENTE POR RUT
# ============================================

class BuscarPacienteFichaForm(forms.Form):
    """
    Formulario para buscar un paciente por RUT antes de crear la ficha obstétrica.
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
                        'Esta persona no está registrada como paciente. '
                        'Debe registrarla primero como paciente.'
                    )
                
                # Guardar el paciente encontrado
                cleaned_data['paciente'] = persona.paciente
                
            except Persona.DoesNotExist:
                raise ValidationError(
                    'No se encontró ninguna persona con este RUT.'
                )
        
        return cleaned_data


# ============================================
# FORMULARIO 2: FICHA OBSTÉTRICA COMPLETA
# ============================================

class FichaObstetricaForm(forms.ModelForm):
    """
    Formulario completo para crear y editar fichas obstétricas.
    Incluye todos los campos del modelo con validaciones robustas.
    """
    
    # Campo oculto para el ID del paciente
    paciente_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=True
    )
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'paciente_id',
            'matrona_responsable',
            'nombre_acompanante',
            # Antecedentes obstétricos
            'numero_gestas',
            'numero_partos',
            'partos_vaginales',
            'partos_cesareas',
            'numero_abortos',
            'nacidos_vivos',
            # Embarazo actual
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            # Datos antropométricos
            'peso_actual',
            'talla',
            # Patologías
            'patologias',
            'descripcion_patologias',
            'patologias_criticas',
            # Tamizaje VIH
            'vih_tomado',
            'vih_resultado',
            'vih_aro',
            # Tamizaje SGB
            'sgb_pesquisa',
            'sgb_resultado',
            'sgb_antibiotico',
            # Tamizaje VDRL
            'vdrl_resultado',
            'vdrl_tratamiento_atb',
            # Tamizaje Hepatitis B
            'hepatitis_b_tomado',
            'hepatitis_b_resultado',
            'hepatitis_b_derivacion',
            # Otros
            'observaciones',
            'activa'
        ]
        
        widgets = {
            # Responsables
            'matrona_responsable': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'nombre_acompanante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del acompañante'
            }),
            
            # Antecedentes obstétricos
            'numero_gestas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'numero_partos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'partos_vaginales': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'partos_cesareas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'numero_abortos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            'nacidos_vivos': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '20'
            }),
            
            # Embarazo actual
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '42'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6'
            }),
            
            # Antropometría
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1',
                'min': '30',
                'max': '200',
                'placeholder': 'kg'
            }),
            'talla': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '120',
                'max': '220',
                'placeholder': 'cm'
            }),
            
            # Patologías
            'patologias': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
            'descripcion_patologias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada de patologías'
            }),
            'patologias_criticas': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Tamizaje VIH
            'vih_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vih_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vih_aro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número ARO'
            }),
            
            # Tamizaje SGB
            'sgb_pesquisa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'sgb_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'sgb_antibiotico': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Antibiótico administrado'
            }),
            
            # Tamizaje VDRL
            'vdrl_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'vdrl_tratamiento_atb': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Tamizaje Hepatitis B
            'hepatitis_b_tomado': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'hepatitis_b_resultado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'hepatitis_b_derivacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            
            # Otros
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observaciones generales de la ficha'
            }),
            'activa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        
        labels = {
            'paciente_id': 'Paciente',
            'matrona_responsable': 'Matrona Responsable',
            'nombre_acompanante': 'Nombre del Acompañante',
            'numero_gestas': 'Número de Gestas (G)',
            'numero_partos': 'Número de Partos (P)',
            'partos_vaginales': 'Partos Vaginales',
            'partos_cesareas': 'Partos por Cesárea',
            'numero_abortos': 'Número de Abortos (A)',
            'nacidos_vivos': 'Nacidos Vivos',
            'fecha_ultima_regla': 'Fecha Última Regla (FUR)',
            'fecha_probable_parto': 'Fecha Probable de Parto (FPP)',
            'edad_gestacional_semanas': 'Edad Gestacional (semanas)',
            'edad_gestacional_dias': 'Días adicionales',
            'peso_actual': 'Peso Actual (kg)',
            'talla': 'Talla (cm)',
            'patologias': 'Patologías Diagnosticadas',
            'descripcion_patologias': 'Descripción de Patologías',
            'patologias_criticas': '¿Tiene Patologías Críticas?',
            'vih_tomado': '¿Se tomó examen VIH?',
            'vih_resultado': 'Resultado VIH',
            'vih_aro': 'Número ARO (VIH)',
            'sgb_pesquisa': '¿Se realizó Pesquisa SGB?',
            'sgb_resultado': 'Resultado SGB',
            'sgb_antibiotico': 'Antibiótico para SGB',
            'vdrl_resultado': 'Resultado VDRL',
            'vdrl_tratamiento_atb': '¿Recibió tratamiento antibiótico?',
            'hepatitis_b_tomado': '¿Se tomó examen Hepatitis B?',
            'hepatitis_b_resultado': 'Resultado Hepatitis B',
            'hepatitis_b_derivacion': '¿Requiere derivación?',
            'observaciones': 'Observaciones Generales',
            'activa': 'Ficha Activa'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar solo matronas activas
        self.fields['matrona_responsable'].queryset = Matrona.objects.filter(
            Activo=True
        ).select_related('persona')
        
        # Filtrar solo patologías activas
        self.fields['patologias'].queryset = Patologias.objects.filter(
            estado=True
        ).order_by('nombre')
    
    def clean_paciente_id(self):
        """Validar que el paciente exista y esté activo"""
        pk = self.cleaned_data.get('paciente_id')
        
        try:
            paciente = Paciente.objects.get(pk=pk, activo=True)
            # Guardar el objeto para usarlo en save()
            self._paciente_obj = paciente
            return pk
        except Paciente.DoesNotExist:
            raise ValidationError('El paciente no existe o no está activo.')
    
    def clean(self):
        """Validaciones cruzadas"""
        cleaned_data = super().clean()
        
        # Validar que partos vaginales + cesáreas = número de partos
        num_partos = cleaned_data.get('numero_partos', 0) or 0
        partos_vag = cleaned_data.get('partos_vaginales', 0) or 0
        partos_ces = cleaned_data.get('partos_cesareas', 0) or 0
        
        if (partos_vag + partos_ces) > num_partos:
            raise ValidationError({
                'numero_partos': 'La suma de partos vaginales y cesáreas no puede ser mayor al número total de partos.'
            })
        
        # Validar edad gestacional
        semanas = cleaned_data.get('edad_gestacional_semanas')
        if semanas is not None and (semanas < 0 or semanas > 42):
            raise ValidationError({
                'edad_gestacional_semanas': 'La edad gestacional debe estar entre 0 y 42 semanas.'
            })
        
        dias = cleaned_data.get('edad_gestacional_dias')
        if dias is not None and (dias < 0 or dias > 6):
            raise ValidationError({
                'edad_gestacional_dias': 'Los días deben estar entre 0 y 6.'
            })
        
        # Validar talla
        talla = cleaned_data.get('talla')
        if talla is not None and (talla < 120 or talla > 220):
            raise ValidationError({
                'talla': 'La talla debe estar entre 120 y 220 cm.'
            })
        
        # Validar peso
        peso = cleaned_data.get('peso_actual')
        if peso is not None and (peso < 30 or peso > 200):
            raise ValidationError({
                'peso_actual': 'El peso debe estar entre 30 y 200 kg.'
            })
        
        # Validar fechas
        fur = cleaned_data.get('fecha_ultima_regla')
        fpp = cleaned_data.get('fecha_probable_parto')
        
        if fur and fpp:
            if fpp <= fur:
                raise ValidationError({
                    'fecha_probable_parto': 'La fecha probable de parto debe ser posterior a la fecha de última regla.'
                })
        
        # Validar que si se tomó VIH, debe tener resultado
        if cleaned_data.get('vih_tomado') and not cleaned_data.get('vih_resultado'):
            raise ValidationError({
                'vih_resultado': 'Debe especificar el resultado del examen VIH.'
            })
        
        # Validar que si se tomó SGB, debe tener resultado
        if cleaned_data.get('sgb_pesquisa') and not cleaned_data.get('sgb_resultado'):
            raise ValidationError({
                'sgb_resultado': 'Debe especificar el resultado de la pesquisa SGB.'
            })
        
        return cleaned_data
    
    def save(self, commit=True):
        """Guardar la ficha con el paciente correcto"""
        ficha = super().save(commit=False)
        
        # Asignar el paciente desde el campo oculto
        paciente = getattr(self, '_paciente_obj', None)
        if paciente:
            ficha.paciente = paciente
        
        if commit:
            ficha.save()
            # Guardar las relaciones ManyToMany (patologías)
            self.save_m2m()
        
        return ficha


# ============================================
# FORMULARIO 3: FICHA OBSTÉTRICA SIMPLIFICADA
# ============================================

class FichaObstetricaSimpleForm(forms.ModelForm):
    """
    Formulario simplificado para crear fichas rápidamente.
    Solo incluye los campos esenciales.
    """
    
    paciente_id = forms.IntegerField(widget=forms.HiddenInput(), required=True)
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'paciente_id',
            'matrona_responsable',
            'fecha_ultima_regla',
            'fecha_probable_parto',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'peso_actual',
            'talla'
        ]
        
        widgets = {
            'matrona_responsable': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ultima_regla': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_probable_parto': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '42'
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6'
            }),
            'peso_actual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.1'
            }),
            'talla': forms.NumberInput(attrs={'class': 'form-control'})
        }


# ============================================
# FORMULARIO 4: ASIGNAR MEDICAMENTO A FICHA
# ============================================

class MedicamentoFichaForm(forms.ModelForm):
    """
    Formulario para que la matrona asigne medicamentos a una ficha obstétrica.
    """
    
    class Meta:
        model = MedicamentoFicha
        fields = [
            'nombre_medicamento',
            'dosis',
            'via_administracion',
            'frecuencia',
            'fecha_inicio',
            'fecha_termino',
            'observaciones'
        ]
        
        widgets = {
            'nombre_medicamento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Paracetamol 500mg',
                'required': True
            }),
            'dosis': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 1 tableta / 5ml',
                'required': True
            }),
            'via_administracion': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'frecuencia': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True,
                'value': timezone.now().strftime('%Y-%m-%d')
            }),
            'fecha_termino': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indicaciones especiales...'
            })
        }
        
        labels = {
            'nombre_medicamento': 'Nombre del Medicamento',
            'dosis': 'Dosis',
            'via_administracion': 'Vía de Administración',
            'frecuencia': 'Frecuencia',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_termino': 'Fecha de Término',
            'observaciones': 'Observaciones'
        }
    
    def clean(self):
        """Validar fechas"""
        cleaned_data = super().clean()
        
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_termino = cleaned_data.get('fecha_termino')
        
        if fecha_inicio and fecha_termino:
            if fecha_termino < fecha_inicio:
                raise ValidationError({
                    'fecha_termino': 'La fecha de término debe ser posterior a la fecha de inicio.'
                })
        
        return cleaned_data


# ============================================
# FORMULARIO 5: ASIGNAR PATOLOGÍAS
# ============================================

class AsignarPatologiasFichaForm(forms.ModelForm):
    """
    Formulario para que la matrona asocie patologías a una ficha.
    Las patologías son gestionadas por el médico.
    """
    
    patologias = forms.ModelMultipleChoiceField(
        queryset=Patologias.objects.filter(estado=True).order_by('nombre'),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'form-check-input'
        }),
        required=False,
        label='Seleccione las patologías diagnosticadas',
        help_text='Puede seleccionar una o varias patologías'
    )
    
    class Meta:
        model = FichaObstetrica
        fields = ['patologias', 'descripcion_patologias', 'patologias_criticas']
        
        widgets = {
            'descripcion_patologias': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción detallada de las patologías...'
            }),
            'patologias_criticas': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ordenar patologías por código CIE-10
        self.fields['patologias'].queryset = Patologias.objects.filter(
            estado=True
        ).order_by('codigo_cie_10', 'nombre')


# ============================================
# FORMULARIO 6: BUSCAR PATOLOGÍA
# ============================================

class BuscarPatologiaForm(forms.Form):
    """
    Formulario simple para buscar patologías en el catálogo.
    """
    
    busqueda = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por nombre o código CIE-10...',
            'id': 'buscar_patologia'
        }),
        label='Buscar en el Catálogo'
    )


# ============================================
# FORMULARIO 7: INGRESO PACIENTE (OPCIONAL)
# ============================================

class IngresoPacienteForm(forms.ModelForm):
    """
    Formulario para registrar el ingreso de una paciente.
    """
    
    class Meta:
        model = IngresoPaciente
        fields = [
            'paciente',
            'motivo_ingreso',
            'fecha_ingreso',
            'hora_ingreso',
            'edad_gestacional_semanas',
            'derivacion',
            'observaciones'
        ]
        
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'motivo_ingreso': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describa el motivo de ingreso...'
            }),
            'fecha_ingreso': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'value': timezone.now().strftime('%Y-%m-%d')
            }),
            'hora_ingreso': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time',
                'value': timezone.now().strftime('%H:%M')
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '42'
            }),
            'derivacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hospital o servicio que deriva'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            })
        }


# ============================================
# FORMULARIO 8: EDICIÓN RÁPIDA DE FICHA
# ============================================

class FichaObstetricaEdicionRapidaForm(forms.ModelForm):
    """
    Formulario para edición rápida de campos comunes de la ficha.
    """
    
    class Meta:
        model = FichaObstetrica
        fields = [
            'matrona_responsable',
            'peso_actual',
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'observaciones',
            'activa'
        ]
        
        widgets = {
            'matrona_responsable': forms.Select(attrs={'class': 'form-select'}),
            'peso_actual': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'edad_gestacional_semanas': forms.NumberInput(attrs={'class': 'form-control'}),
            'edad_gestacional_dias': forms.NumberInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
