
from django import forms
from django.core.exceptions import ValidationError
from partosApp.models import RegistroParto
from matronaApp.models import FichaObstetrica


class RegistroPartoBaseForm(forms.ModelForm):
    """
    Formulario base con información general del parto
    """
    class Meta:
        model = RegistroParto
        fields = [
            'ficha',
            'fecha_hora_admision',
            'fecha_hora_parto',
        ]
        widgets = {
            'ficha': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'fecha_hora_admision': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
                'required': True
            }),
            'fecha_hora_parto': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'ficha': 'Ficha Obstétrica',
            'fecha_hora_admision': 'Fecha y Hora de Admisión',
            'fecha_hora_parto': 'Fecha y Hora del Parto',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo fichas activas
        self.fields['ficha'].queryset = FichaObstetrica.objects.filter(
            activa=True
        ).select_related('paciente__persona')


class TrabajoDePartoForm(forms.ModelForm):
    """
    Formulario para la sección de Trabajo de Parto
    """
    class Meta:
        model = RegistroParto
        fields = [
            # VIH al ingreso
            'vih_tomado_prepartos',
            'vih_tomado_sala',
            # Trabajo de parto
            'edad_gestacional_semanas',
            'edad_gestacional_dias',
            'monitor_ttc',
            'induccion',
            'aceleracion_correccion',
            'numero_tactos_vaginales',
            'rotura_membrana',
            'tiempo_membranas_rotas',
            'tiempo_dilatacion',
            'tiempo_expulsivo',
        ]
        widgets = {
            'vih_tomado_prepartos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'vih_tomado_sala': forms.Select(attrs={
                'class': 'form-select'
            }),
            'edad_gestacional_semanas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '20',
                'max': '42',
                'required': True
            }),
            'edad_gestacional_dias': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'max': '6',
                'value': '0'
            }),
            'monitor_ttc': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'induccion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'aceleracion_correccion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'numero_tactos_vaginales': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
            'rotura_membrana': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'tiempo_membranas_rotas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Horas'
            }),
            'tiempo_dilatacion': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Minutos'
            }),
            'tiempo_expulsivo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Minutos'
            }),
        }
        labels = {
            'vih_tomado_prepartos': '¿VIH tomado en Prepartos?',
            'vih_tomado_sala': 'VIH tomado en Sala',
            'edad_gestacional_semanas': 'Edad Gestacional (semanas)',
            'edad_gestacional_dias': 'Edad Gestacional (días)',
            'monitor_ttc': 'Monitor TTC',
            'induccion': 'Inducción',
            'aceleracion_correccion': 'Aceleración o Corrección',
            'numero_tactos_vaginales': 'Número de Tactos Vaginales',
            'rotura_membrana': 'Rotura de Membrana',
            'tiempo_membranas_rotas': 'Tiempo Membranas Rotas (horas)',
            'tiempo_dilatacion': 'Tiempo de Dilatación (minutos)',
            'tiempo_expulsivo': 'Tiempo Expulsivo (minutos)',
        }


class InformacionPartoForm(forms.ModelForm):
    """
    Formulario para la información específica del parto
    """
    class Meta:
        model = RegistroParto
        fields = [
            'libertad_movimiento',
            'tipo_regimen',
            'tipo_parto',
            'alumbramiento_dirigido',
            'clasificacion_robson',
            'posicion_materna_parto',
        ]
        widgets = {
            'libertad_movimiento': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tipo_regimen': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'tipo_parto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'alumbramiento_dirigido': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'clasificacion_robson': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'posicion_materna_parto': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }
        labels = {
            'libertad_movimiento': 'Libertad de Movimiento',
            'tipo_regimen': 'Tipo de Régimen',
            'tipo_parto': 'Tipo de Parto',
            'alumbramiento_dirigido': 'Alumbramiento Dirigido',
            'clasificacion_robson': 'Clasificación de Robson',
            'posicion_materna_parto': 'Posición Materna',
        }


class PuerperioForm(forms.ModelForm):
    """
    Formulario para la sección de Puerperio
    """
    class Meta:
        model = RegistroParto
        fields = [
            'ofrecimiento_posiciones_alternativas',
            'estado_perine',
            'esterilizacion',
            'revision',
            'inercia_uterina',
            'restos_placentarios',
            'trauma',
            'alteracion_coagulacion',
            'manejo_quirurgico_inercia',
        ]
        widgets = {
            'ofrecimiento_posiciones_alternativas': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'estado_perine': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'esterilizacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'revision': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'inercia_uterina': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'restos_placentarios': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'trauma': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'alteracion_coagulacion': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'manejo_quirurgico_inercia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'ofrecimiento_posiciones_alternativas': 'Ofrecimiento de Posiciones Alternativas',
            'estado_perine': 'Estado del Periné',
            'esterilizacion': 'Esterilización',
            'revision': 'Revisión',
            'inercia_uterina': 'Inercia Uterina',
            'restos_placentarios': 'Restos Placentarios',
            'trauma': 'Trauma',
            'alteracion_coagulacion': 'Alteración de la Coagulación',
            'manejo_quirurgico_inercia': 'Manejo Quirúrgico de Inercia',
        }


class AnestesiaAnalgesiaForm(forms.ModelForm):
    """
    Formulario para Anestesia y Analgesia
    """
    class Meta:
        model = RegistroParto
        fields = [
            'histerectomia_obstetrica',
            'transfusion_sanguinea',
            'anestesia_neuroaxial',
            'oxido_nitroso',
            'analgesia_endovenosa',
            'anestesia_general',
            'anestesia_local',
            'analgesia_no_farmacologica',
            'balon_kinesico',
            'lenteja_parto',
            'rebozo',
            'aromaterapia',
            'peridural_solicitada_paciente',
            'peridural_indicada_medico',
            'peridural_administrada',
            'tiempo_espera_peridural',
        ]
        widgets = {
            'histerectomia_obstetrica': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'transfusion_sanguinea': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'anestesia_neuroaxial': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'oxido_nitroso': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'analgesia_endovenosa': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'anestesia_general': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'anestesia_local': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'analgesia_no_farmacologica': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'balon_kinesico': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'lenteja_parto': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'rebozo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'aromaterapia': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'peridural_solicitada_paciente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'peridural_indicada_medico': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'peridural_administrada': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'tiempo_espera_peridural': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': 'Minutos'
            }),
        }


class ProfesionalesForm(forms.ModelForm):
    """
    Formulario para información de profesionales
    """
    class Meta:
        model = RegistroParto
        fields = [
            'profesional_responsable',
            'alumno',
            'causa_cesarea',
            'observaciones',
            'uso_sala_saip',
        ]
        widgets = {
            'profesional_responsable': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del profesional',
                'required': True
            }),
            'alumno': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del alumno (si aplica)'
            }),
            'causa_cesarea': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Indicación médica para cesárea'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Observaciones generales del parto'
            }),
            'uso_sala_saip': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'profesional_responsable': 'Profesional Responsable',
            'alumno': 'Alumno',
            'causa_cesarea': 'Causa de Cesárea',
            'observaciones': 'Observaciones',
            'uso_sala_saip': 'Uso de Sala SAIP',
        }


class RegistroPartoCompletoForm(forms.ModelForm):
    """
    Formulario completo del parto (todas las secciones en uno)
    Usar solo si se quiere capturar todo en una sola vista
    """
    class Meta:
        model = RegistroParto
        exclude = ['numero_registro', 'fecha_creacion', 'fecha_modificacion', 'activo']
        widgets = {
            'ficha': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora_admision': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'fecha_hora_parto': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            # Agregar widgets para todos los campos...
            # (similar a los formularios anteriores)
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar fichas activas
        self.fields['ficha'].queryset = FichaObstetrica.objects.filter(
            activa=True
        ).select_related('paciente__persona')
        
        # Hacer campos opcionales según corresponda
        campos_opcionales = [
            'fecha_hora_parto',
            'tiempo_membranas_rotas',
            'tiempo_dilatacion',
            'tiempo_expulsivo',
            'tiempo_espera_peridural',
            'alumno',
            'causa_cesarea',
            'observaciones',
        ]
        for campo in campos_opcionales:
            if campo in self.fields:
                self.fields[campo].required = False