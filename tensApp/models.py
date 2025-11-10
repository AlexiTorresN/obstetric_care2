from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from gestionApp.models import Tens, Paciente
from matronaApp.models import FichaObstetrica, MedicamentoFicha


# ============================================
# MODELO: REGISTRO TENS (Signos Vitales)
# ============================================

class RegistroTens(models.Model):
    """
    Registro de signos vitales por TENS
    Los TENS registran temperatura, presión arterial, etc.
    """
    
    TURNO_CHOICES = [
        ('MANANA', 'Mañana'),
        ('TARDE', 'Tarde'),
        ('NOCHE', 'Noche'),
    ]
    
    # Relaciones
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='registros_tens',
        verbose_name='Ficha Obstétrica'
    )
    
    tens_responsable = models.ForeignKey(
        Tens,
        on_delete=models.PROTECT,
        related_name='registros_signos_vitales',
        null=True,
        blank=True,
        verbose_name='TENS Responsable'
    )
    
    # Datos del registro
    fecha = models.DateField(
        default=timezone.now,
        verbose_name='Fecha del Registro'
    )
    
    turno = models.CharField(
        max_length=10,
        choices=TURNO_CHOICES,
        blank=True,
        verbose_name='Turno'
    )
    
    # Signos vitales
    temperatura = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        blank=True,
        null=True,
        verbose_name='Temperatura (°C)',
        help_text='Ej: 36.5',
        validators=[MinValueValidator(30), MaxValueValidator(45)]
    )
    
    frecuencia_cardiaca = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Frecuencia Cardíaca (lpm)',
        help_text='Latidos por minuto',
        validators=[MinValueValidator(30), MaxValueValidator(200)]
    )
    
    presion_arterial_sistolica = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Presión Arterial Sistólica',
        help_text='Ej: 120'
    )
    
    presion_arterial_diastolica = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Presión Arterial Diastólica',
        help_text='Ej: 80'
    )
    
    frecuencia_respiratoria = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Frecuencia Respiratoria (rpm)',
        help_text='Respiraciones por minuto',
        validators=[MinValueValidator(8), MaxValueValidator(40)]
    )
    
    saturacion_oxigeno = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='Saturación de Oxígeno (%)',
        help_text='Porcentaje de saturación (SpO2)',
        validators=[MinValueValidator(50), MaxValueValidator(100)]
    )
    
    # Observaciones
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones',
        help_text='Observaciones adicionales del TENS'
    )
    
    # Metadatos
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro en Sistema'
    )
    
    class Meta:
        ordering = ['-fecha', '-fecha_registro']
        verbose_name = 'Registro TENS'
        verbose_name_plural = 'Registros TENS'
        indexes = [
            models.Index(fields=['ficha', '-fecha']),
            models.Index(fields=['tens_responsable', '-fecha']),
        ]
    
    def __str__(self):
        return f"Registro TENS - Ficha {self.ficha.numero_ficha} - {self.fecha}"
    
    @property
    def presion_arterial(self):
        """Retorna la presión arterial en formato 120/80"""
        if self.presion_arterial_sistolica and self.presion_arterial_diastolica:
            return f"{self.presion_arterial_sistolica}/{self.presion_arterial_diastolica}"
        return "No registrada"


# ============================================
# MODELO: TRATAMIENTO APLICADO
# ============================================

class Tratamiento_aplicado(models.Model):
    """
    Registro de tratamientos/medicamentos aplicados por TENS
    Vinculado a una ficha obstétrica y opcionalmente a un medicamento prescrito
    """
    
    VIA_ADMINISTRACION_CHOICES = [
        ('oral', 'Oral'),
        ('endovenosa', 'Endovenosa'),
        ('intramuscular', 'Intramuscular'),
        ('subcutanea', 'Subcutánea'),
        ('topica', 'Tópica'),
        ('inhalatoria', 'Inhalatoria'),
    ]
    
    # ============================================
    # RELACIONES
    # ============================================
    
    ficha = models.ForeignKey(
        FichaObstetrica,
        on_delete=models.CASCADE,
        related_name='tratamientos_aplicados',
        verbose_name='Ficha Obstétrica'
    )
    
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='tratamientos_recibidos',
        verbose_name='Paciente'
    )
    
    tens = models.ForeignKey(
        Tens,
        on_delete=models.PROTECT,
        related_name='tratamientos_aplicados',
        verbose_name='TENS que Aplicó'
    )
    
    medicamento_ficha = models.ForeignKey(
        MedicamentoFicha,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='aplicaciones_tens',
        verbose_name='Medicamento de Ficha',
        help_text='Si aplica un medicamento prescrito en la ficha'
    )
    
    # ============================================
    # DATOS DEL TRATAMIENTO
    # ============================================
    
    nombre_medicamento = models.CharField(
        max_length=200,
        verbose_name='Nombre del Medicamento/Tratamiento'
    )
    
    dosis = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Dosis Aplicada',
        help_text='Ej: 500mg, 10ml, 2 comprimidos'
    )
    
    via_administracion = models.CharField(
        max_length=50,
        choices=VIA_ADMINISTRACION_CHOICES,
        default='oral',
        verbose_name='Vía de Administración'
    )
    
    fecha_aplicacion = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Aplicación'
    )
    
    hora_aplicacion = models.TimeField(
        default=timezone.now,
        verbose_name='Hora de Aplicación'
    )
    
    # ============================================
    # PROCEDIMIENTO
    # ============================================
    
    se_realizo_lavado_manos = models.BooleanField(
        default=False,
        verbose_name='¿Se realizó lavado de manos?'
    )
    
    aplicado_exitosamente = models.BooleanField(
        default=True,
        verbose_name='¿Se aplicó exitosamente?'
    )
    
    motivo_no_aplicacion = models.TextField(
        blank=True,
        verbose_name='Motivo de No Aplicación',
        help_text='Completar solo si no se aplicó'
    )
    
    # ============================================
    # OBSERVACIONES Y REACCIONES
    # ============================================
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones',
        help_text='Detalles adicionales sobre la aplicación'
    )
    
    reacciones_adversas = models.TextField(
        blank=True,
        verbose_name='Reacciones Adversas',
        help_text='Cualquier reacción adversa observada'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Los tratamientos pueden desactivarse pero no eliminarse'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro en Sistema'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Última Modificación'
    )
    
    class Meta:
        ordering = ['-fecha_aplicacion', '-hora_aplicacion']
        verbose_name = 'Tratamiento Aplicado'
        verbose_name_plural = 'Tratamientos Aplicados'
        indexes = [
            models.Index(fields=['ficha', '-fecha_aplicacion']),
            models.Index(fields=['paciente', '-fecha_aplicacion']),
            models.Index(fields=['tens', '-fecha_aplicacion']),
            models.Index(fields=['medicamento_ficha', '-fecha_aplicacion']),
        ]
    
    def __str__(self):
        return f"{self.nombre_medicamento} - {self.paciente.persona.Nombre} {self.paciente.persona.Apellido_Paterno} ({self.fecha_aplicacion})"
    
    @property
    def fecha_hora_completa(self):
        """Retorna fecha y hora combinadas"""
        from datetime import datetime, time
        if isinstance(self.hora_aplicacion, time):
            return datetime.combine(self.fecha_aplicacion, self.hora_aplicacion)
        return self.fecha_aplicacion