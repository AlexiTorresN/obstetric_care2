from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from gestionApp.models import Paciente, Matrona, Tens
from medicoApp.models import Patologias


# ============================================
# MODELO: INGRESO PACIENTE
# ============================================

class IngresoPaciente(models.Model):
    """
    Registro del ingreso de una paciente a la unidad obstétrica
    """
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='ingresos',
        verbose_name='Paciente'
    )
    
    motivo_ingreso = models.TextField(
        verbose_name='Motivo de Ingreso',
        help_text='Descripción del motivo de ingreso'
    )
    
    fecha_ingreso = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Ingreso'
    )
    
    hora_ingreso = models.TimeField(
        default=timezone.now,
        verbose_name='Hora de Ingreso'
    )
    
    edad_gestacional_semanas = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(42)],
        verbose_name='Edad Gestacional (semanas)'
    )
    
    derivacion = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Derivación',
        help_text='Hospital o servicio que deriva (si aplica)'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones del Ingreso'
    )
    
    numero_ficha = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha de Ingreso'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        verbose_name = 'Ingreso de Paciente'
        verbose_name_plural = 'Ingresos de Pacientes'
        ordering = ['-fecha_ingreso']
    
    def __str__(self):
        return f"Ingreso {self.numero_ficha} - {self.paciente.persona.Nombre} {self.paciente.persona.Apellido_Paterno}"


# ============================================
# MODELO: FICHA OBSTÉTRICA
# ============================================

class FichaObstetrica(models.Model):
    """
    Ficha clínica obstétrica completa de una paciente
    Contiene todos los antecedentes y datos del embarazo
    """
    
    # Relaciones principales
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='fichas_obstetricas',
        verbose_name='Paciente'
    )
    
    matrona_responsable = models.ForeignKey(
        Matrona,
        on_delete=models.PROTECT,
        related_name='fichas_asignadas',
        verbose_name='Matrona Responsable'
    )
    
    # Identificación de la ficha
    numero_ficha = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha',
        help_text='Se genera automáticamente'
    )
    
    # Acompañante
    nombre_acompanante = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Nombre del Acompañante'
    )
    
    # ============================================
    # ANTECEDENTES OBSTÉTRICOS
    # ============================================
    
    numero_gestas = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Número de Gestas',
        help_text='Total de embarazos incluyendo el actual'
    )
    
    numero_partos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Número de Partos',
        help_text='Total de partos anteriores'
    )
    
    partos_vaginales = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Partos Vaginales',
        help_text='Número de partos vaginales previos'
    )
    
    partos_cesareas = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Partos por Cesárea',
        help_text='Número de cesáreas previas'
    )
    
    numero_abortos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Número de Abortos',
        help_text='Abortos espontáneos o inducidos previos'
    )
    
    nacidos_vivos = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Nacidos Vivos',
        help_text='Número de hijos nacidos vivos'
    )
    
    # ============================================
    # EMBARAZO ACTUAL
    # ============================================
    
    fecha_ultima_regla = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de Última Regla (FUR)',
        help_text='Primer día de la última menstruación'
    )
    
    fecha_probable_parto = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha Probable de Parto (FPP)',
        help_text='Calculada a partir de FUR o ecografía'
    )
    
    edad_gestacional_semanas = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(42)],
        verbose_name='Edad Gestacional (Semanas)',
        help_text='Semanas completas de gestación'
    )
    
    edad_gestacional_dias = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        verbose_name='Edad Gestacional (Días)',
        help_text='Días adicionales a las semanas'
    )
    
    # ============================================
    # DATOS ANTROPOMÉTRICOS
    # ============================================
    
    peso_actual = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(30), MaxValueValidator(200)],
        verbose_name='Peso Actual (kg)',
        help_text='Peso de la paciente en kilogramos'
    )
    
    talla = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(120), MaxValueValidator(220)],
        verbose_name='Talla (cm)',
        help_text='Estatura de la paciente en centímetros'
    )
    
    # ============================================
    # PATOLOGÍAS
    # ============================================
    
    patologias = models.ManyToManyField(
        Patologias,
        blank=True,
        related_name='fichas_con_patologia',
        verbose_name='Patologías Asociadas'
    )
    
    descripcion_patologias = models.TextField(
        blank=True,
        verbose_name='Descripción Detallada de Patologías',
        help_text='Detalles adicionales sobre las patologías'
    )
    
    PATOLOGIAS_CRITICAS_CHOICES = [
        ('NINGUNA', 'Ninguna'),
        ('PREECLAMPSIA_SEVERA', 'Preeclampsia Severa'),
        ('ECLAMPSIA', 'Eclampsia'),
        ('SEPSIS', 'Sepsis o Infección Sistémica Grave'),
        ('CORIOAMNIONITIS', 'Infección Ovular o Corioamnionitis'),
    ]
    
    patologias_criticas = models.CharField(
        max_length=100,
        choices=PATOLOGIAS_CRITICAS_CHOICES,
        default='NINGUNA',
        verbose_name='Patologías Críticas',
        help_text='Patologías de alto riesgo vital'
    )
    
    # ============================================
    # TAMIZAJE VIH
    # ============================================
    
    vih_tomado = models.BooleanField(
        default=False,
        verbose_name='Toma de VIH Realizada',
        help_text='¿Se realizó la prueba de VIH durante el embarazo?'
    )
    
    VIH_RESULTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('NEGATIVO', 'Negativo'),
        ('POSITIVO', 'Positivo'),
        ('NO_REALIZADO', 'No Realizado'),
    ]
    
    vih_resultado = models.CharField(
        max_length=20,
        choices=VIH_RESULTADO_CHOICES,
        blank=True,
        default='PENDIENTE',
        verbose_name='Resultado VIH',
        help_text='Resultado de la prueba de VIH'
    )
    
    vih_aro = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Nº ARO (si otra patología)',
        help_text='Número ARO si se detecta otra patología'
    )
    
    # ============================================
    # TAMIZAJE ESTREPTOCOCO GRUPO B (SGB)
    # ============================================
    
    sgb_pesquisa = models.BooleanField(
        default=False,
        verbose_name='Pesquisa SGB Realizada',
        help_text='¿Se realizó pesquisa de Estreptococo Grupo B?'
    )
    
    SGB_RESULTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('POSITIVO', 'Positivo'),
        ('NEGATIVO', 'Negativo'),
        ('NO_REALIZADO', 'No Realizado'),
    ]
    
    sgb_resultado = models.CharField(
        max_length=20,
        choices=SGB_RESULTADO_CHOICES,
        blank=True,
        default='PENDIENTE',
        verbose_name='Resultado SGB',
        help_text='Resultado de la pesquisa'
    )
    
    sgb_antibiotico = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Antibiótico para SGB',
        help_text='Antibiótico indicado si SGB positivo'
    )
    
    # ============================================
    # TAMIZAJE VDRL (SÍFILIS)
    # ============================================
    
    VDRL_RESULTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('NO_REACTIVO', 'No Reactivo'),
        ('REACTIVO', 'Reactivo'),
        ('NO_REALIZADO', 'No Realizado'),
    ]
    
    vdrl_resultado = models.CharField(
        max_length=20,
        choices=VDRL_RESULTADO_CHOICES,
        blank=True,
        default='PENDIENTE',
        verbose_name='Resultado VDRL',
        help_text='Resultado del tamizaje de sífilis'
    )
    
    vdrl_tratamiento_atb = models.BooleanField(
        default=False,
        verbose_name='Tratamiento Antibiótico VDRL',
        help_text='¿Recibió tratamiento antibiótico por VDRL reactivo?'
    )
    
    # ============================================
    # TAMIZAJE HEPATITIS B
    # ============================================
    
    hepatitis_b_tomado = models.BooleanField(
        default=False,
        verbose_name='Examen Hepatitis B Realizado',
        help_text='¿Se tomó examen de Hepatitis B?'
    )
    
    HEPATITIS_B_RESULTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('NEGATIVO', 'Negativo'),
        ('POSITIVO', 'Positivo'),
        ('NO_REALIZADO', 'No Realizado'),
    ]
    
    hepatitis_b_resultado = models.CharField(
        max_length=20,
        choices=HEPATITIS_B_RESULTADO_CHOICES,
        blank=True,
        default='PENDIENTE',
        verbose_name='Resultado Hepatitis B',
        help_text='Resultado del examen'
    )
    
    hepatitis_b_derivacion = models.BooleanField(
        default=False,
        verbose_name='Derivación a Gastro-Hepatólogo',
        help_text='¿Requiere derivación por Hepatitis B positiva?'
    )
    
    # ============================================
    # OBSERVACIONES Y METADATOS
    # ============================================
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones Generales',
        help_text='Observaciones sobre el embarazo actual'
    )
    
    antecedentes_relevantes = models.TextField(
        blank=True,
        verbose_name='Antecedentes Médicos Relevantes',
        help_text='Antecedentes médicos, quirúrgicos, alergias, etc.'
    )
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Última Modificación'
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Ficha Activa',
        help_text='Indica si la ficha está activa o cerrada'
    )
    
    class Meta:
        verbose_name = 'Ficha Obstétrica'
        verbose_name_plural = 'Fichas Obstétricas'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['numero_ficha']),
            models.Index(fields=['paciente', 'activa']),
            models.Index(fields=['-fecha_creacion']),
        ]
    
    def __str__(self):
        return f"Ficha {self.numero_ficha} - {self.paciente.persona.Nombre} {self.paciente.persona.Apellido_Paterno}"
    
    @property
    def edad_gestacional_completa(self):
        """Retorna la edad gestacional en formato 'XX semanas + X días'"""
        if self.edad_gestacional_semanas is not None:
            if self.edad_gestacional_dias:
                return f"{self.edad_gestacional_semanas} semanas + {self.edad_gestacional_dias} días"
            return f"{self.edad_gestacional_semanas} semanas"
        return "No especificada"


# ============================================
# MODELO: MEDICAMENTO FICHA
# ============================================

class MedicamentoFicha(models.Model):
    """
    Medicamentos asignados a una ficha obstétrica
    Registrados por la matrona para administración por TENS
    """
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='medicamentos',
        verbose_name='Ficha Obstétrica'
    )
    
    nombre_medicamento = models.CharField(
        max_length=200,
        verbose_name='Nombre del Medicamento'
    )
    
    dosis = models.CharField(
        max_length=100,
        verbose_name='Dosis'
    )
    
    VIA_ADMINISTRACION_CHOICES = [
        ('oral', 'Oral'),
        ('endovenosa', 'Endovenosa'),
        ('intramuscular', 'Intramuscular'),
        ('subcutanea', 'Subcutánea'),
        ('topica', 'Tópica'),
    ]
    
    via_administracion = models.CharField(
        max_length=50,
        choices=VIA_ADMINISTRACION_CHOICES,
        verbose_name='Vía de Administración'
    )
    
    FRECUENCIA_CHOICES = [
        ('1_vez_dia', '1 vez al día'),
        ('2_veces_dia', '2 veces al día'),
        ('3_veces_dia', '3 veces al día'),
        ('Cada_8_horas', 'Cada 8 horas'),
        ('Cada_12_horas', 'Cada 12 horas'),
        ('SOS', 'SOS (según necesidad)'),
    ]
    
    frecuencia = models.CharField(
        max_length=50,
        choices=FRECUENCIA_CHOICES,
        verbose_name='Frecuencia'
    )
    
    fecha_inicio = models.DateField(
        verbose_name='Fecha de Inicio',
        help_text='Fecha en que inicia el tratamiento'
    )
    
    fecha_termino = models.DateField(
        verbose_name='Fecha de Término',
        help_text='Fecha en que finaliza el tratamiento'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones',
        help_text='Indicaciones especiales sobre la medicación'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro'
    )
    
    class Meta:
        verbose_name = 'Medicamento de Ficha'
        verbose_name_plural = 'Medicamentos de Fichas'
        ordering = ['-fecha_inicio']
        indexes = [
            models.Index(fields=['ficha', 'activo']),
        ]
    
    def __str__(self):
        return f"{self.nombre_medicamento} - {self.ficha.paciente.persona.Nombre} {self.ficha.paciente.persona.Apellido_Paterno}"


# ============================================
# MODELO: ADMINISTRACIÓN DE MEDICAMENTO (TENS)
# ============================================

class AdministracionMedicamento(models.Model):
    """
    Registro de administración de medicamentos por parte del TENS
    """
    
    medicamento_ficha = models.ForeignKey(
        MedicamentoFicha,
        on_delete=models.CASCADE,
        related_name='administraciones',
        verbose_name='Medicamento Asignado'
    )
    
    tens = models.ForeignKey(
        Tens,
        on_delete=models.PROTECT,
        related_name='administraciones_realizadas',
        verbose_name='TENS que Administró'
    )
    
    fecha_hora_administracion = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Administración'
    )
    
    se_realizo_lavado = models.BooleanField(
        default=False,
        verbose_name='¿Se realizó lavado de manos?'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones de la Administración'
    )
    
    reacciones_adversas = models.TextField(
        blank=True,
        verbose_name='Reacciones Adversas Observadas'
    )
    
    administrado_exitosamente = models.BooleanField(
        default=True,
        verbose_name='¿Se administró exitosamente?'
    )
    
    motivo_no_administracion = models.TextField(
        blank=True,
        verbose_name='Motivo de No Administración',
        help_text='Completar solo si no se administró'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro en Sistema'
    )
    
    class Meta:
        verbose_name = 'Administración de Medicamento'
        verbose_name_plural = 'Administraciones de Medicamentos'
        ordering = ['-fecha_hora_administracion']
        indexes = [
            models.Index(fields=['medicamento_ficha', '-fecha_hora_administracion']),
            models.Index(fields=['tens', '-fecha_hora_administracion']),
        ]
    
    def __str__(self):
        return f"Administración: {self.medicamento_ficha.nombre_medicamento} por {self.tens.persona.Nombre} {self.tens.persona.Apellido_Paterno}"