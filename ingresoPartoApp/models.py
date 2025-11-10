from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class FichaParto(models.Model):
    """
    Ficha de ingreso para el proceso de parto
    Se crea cuando la paciente ingresa a la unidad
    Contiene TODOS los datos de admisión y tamizajes
    """
    
    # ============================================
    # RELACIÓN CON FICHA OBSTÉTRICA
    # ============================================
    
    ficha_obstetrica = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.PROTECT,
        related_name='fichas_ingreso_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    numero_ficha_parto = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Ficha de Parto',
        help_text='Se genera automáticamente: FP-000001'
    )
    
    # ============================================
    # SECCIÓN 1: DATOS GENERALES DEL INGRESO
    # ============================================
    
    TIPO_PACIENTE_CHOICES = [
        ('INSTITUCIONAL', 'Institucional'),
        ('PREHOSPITALARIO', 'Prehospitalario'),
        ('FUERA_RED', 'Fuera de la Red Asistencial'),
        ('DOMICILIO_CON_PROF', 'Domicilio con Atención Profesional'),
        ('DOMICILIO_SIN_PROF', 'Domicilio sin Atención Profesional'),
    ]
    
    tipo_paciente = models.CharField(
        max_length=30,
        choices=TIPO_PACIENTE_CHOICES,
        default='INSTITUCIONAL',
        verbose_name='Tipo de Paciente',
        help_text='Clasificación según origen'
    )
    
    ORIGEN_INGRESO_CHOICES = [
        ('SALA', 'Sala'),
        ('UEGO', 'UEGO (Unidad Emergencia Gineco-Obstétrica)'),
    ]
    
    origen_ingreso = models.CharField(
        max_length=20,
        choices=ORIGEN_INGRESO_CHOICES,
        verbose_name='Origen de Ingreso',
        help_text='De dónde viene la paciente'
    )
    
    fecha_ingreso = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de Ingreso'
    )
    
    hora_ingreso = models.TimeField(
        default=timezone.now,
        verbose_name='Hora de Ingreso'
    )
    
    plan_de_parto = models.BooleanField(
        default=False,
        verbose_name='¿Tiene Plan de Parto?',
        help_text='¿La paciente presentó plan de parto?'
    )
    
    visita_guiada = models.BooleanField(
        default=False,
        verbose_name='¿Realizó Visita Guiada?',
        help_text='¿Hizo visita previa a la unidad?'
    )
    
    control_prenatal = models.BooleanField(
        default=True,
        verbose_name='¿Tuvo Control Prenatal?',
        help_text='¿Asistió a controles durante el embarazo?'
    )
    
    consultorio_origen = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Consultorio de Origen',
        help_text='Nombre del consultorio o CESFAM'
    )
    
    # ============================================
    # SECCIÓN 2: PATOLOGÍAS AL INGRESO
    # ============================================
    
    preeclampsia_severa = models.BooleanField(
        default=False,
        verbose_name='Preeclampsia Severa'
    )
    
    eclampsia = models.BooleanField(
        default=False,
        verbose_name='Eclampsia'
    )
    
    sepsis_infeccion_grave = models.BooleanField(
        default=False,
        verbose_name='Sepsis o Infección Sistémica Grave'
    )
    
    infeccion_ovular = models.BooleanField(
        default=False,
        verbose_name='Infección Ovular o Corioamnionitis'
    )
    
    otra_patologia = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Otra Patología',
        help_text='Especificar otra patología si aplica'
    )
    
    # ============================================
    # ✅ SECCIÓN 3: TAMIZAJE VIH (MOVIDO DESDE partosApp)
    # ============================================
    
    numero_aro = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Número ARO',
        help_text='Número de Alto Riesgo Obstétrico'
    )
    
    vih_tomado_prepartos = models.BooleanField(
        default=False,
        verbose_name='Se tomó VIH en Prepartos',
        help_text='¿Se realizó test de VIH al ingresar a prepartos?'
    )
    
    vih_tomado_sala = models.BooleanField(
        default=False,
        verbose_name='Se tomó VIH en Sala',
        help_text='¿Se realizó test de VIH en sala de parto?'
    )
    
    VIH_ORDEN_CHOICES = [
        ('1', 'Primera vez (1°)'),
        ('2', 'Segunda vez (2°)'),
        ('3', 'Tercera vez (3°)'),
    ]
    
    vih_orden_toma = models.CharField(
        max_length=1,
        choices=VIH_ORDEN_CHOICES,
        blank=True,
        verbose_name='Orden de Toma (1°-2°-3°)',
        help_text='Número de vez que se toma el VIH'
    )
    
    # ============================================
    # SECCIÓN 4: TAMIZAJE SGB (Streptococcus Grupo B)
    # ============================================
    
    sgb_pesquisa = models.BooleanField(
        default=False,
        verbose_name='Pesquisa SGB Realizada',
        help_text='¿Se realizó cultivo para SGB?'
    )
    
    SGB_RESULTADO_CHOICES = [
        ('POSITIVO', 'Positivo'),
        ('NEGATIVO', 'Negativo'),
    ]
    
    sgb_resultado = models.CharField(
        max_length=10,
        choices=SGB_RESULTADO_CHOICES,
        blank=True,
        verbose_name='Resultado SGB'
    )
    
    antibiotico_sgb = models.BooleanField(
        default=False,
        verbose_name='Antibiótico por SGB (NO POR RPM)',
        help_text='¿Se administró antibiótico profiláctico por SGB positivo?'
    )
    
    # ============================================
    # SECCIÓN 5: TAMIZAJE VDRL (Sífilis)
    # ============================================
    
    VDRL_RESULTADO_CHOICES = [
        ('NO_REACTIVO', 'No Reactivo'),
        ('REACTIVO', 'Reactivo'),
    ]
    
    vdrl_resultado = models.CharField(
        max_length=15,
        choices=VDRL_RESULTADO_CHOICES,
        blank=True,
        verbose_name='Resultado VDRL durante embarazo',
        help_text='Resultado del test VDRL para sífilis'
    )
    
    tratamiento_sifilis = models.BooleanField(
        default=False,
        verbose_name='Tratamiento ATB por Sífilis al momento del Parto',
        help_text='¿Se administró tratamiento antibiótico para sífilis?'
    )
    
    # ============================================
    # SECCIÓN 6: TAMIZAJE HEPATITIS B
    # ============================================
    
    hepatitis_b_tomado = models.BooleanField(
        default=False,
        verbose_name='Examen Hepatitis B - Tomado',
        help_text='¿Se realizó serología para Hepatitis B?'
    )
    
    derivacion_gastro = models.BooleanField(
        default=False,
        verbose_name='Derivación a Gastro-Hepatólogo',
        help_text='¿Requiere derivación a especialista?'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación del Registro'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Última Modificación'
    )
    
    activa = models.BooleanField(
        default=True,
        verbose_name='Ficha Activa'
    )
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Ficha de Parto (Ingreso)'
        verbose_name_plural = 'Fichas de Parto (Ingresos)'
        indexes = [
            models.Index(fields=['numero_ficha_parto']),
            models.Index(fields=['ficha_obstetrica', '-fecha_ingreso']),
        ]
    
    def __str__(self):
        return f"{self.numero_ficha_parto} - {self.ficha_obstetrica.paciente.persona.Nombre}"
    
    def save(self, *args, **kwargs):
        """Generar número automático si no existe"""
        if not self.numero_ficha_parto:
            ultima = FichaParto.objects.order_by('-id').first()
            if ultima:
                try:
                    numero = int(ultima.numero_ficha_parto.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_ficha_parto = f"FP-{numero:06d}"
        super().save(*args, **kwargs)
    
    def tiene_tamizajes_completos(self):
        """Verifica si todos los tamizajes están completos"""
        return all([
            self.sgb_pesquisa,
            self.vdrl_resultado,
            self.hepatitis_b_tomado,
            self.vih_tomado_prepartos or self.vih_tomado_sala,
        ])
    
    def tiene_patologias_graves(self):
        """Verifica si tiene patologías que requieren atención especial"""
        return any([
            self.preeclampsia_severa,
            self.eclampsia,
            self.sepsis_infeccion_grave,
            self.infeccion_ovular,
        ])
    
    def resumen_tamizajes(self):
        """Retorna un resumen de los tamizajes realizados"""
        resumen = []
        
        if self.sgb_pesquisa:
            resumen.append(f"SGB: {self.sgb_resultado or 'Pendiente'}")
        
        if self.vdrl_resultado:
            resumen.append(f"VDRL: {self.get_vdrl_resultado_display()}")
        
        if self.hepatitis_b_tomado:
            resumen.append("Hepatitis B: Realizado")
        
        if self.vih_tomado_prepartos or self.vih_tomado_sala:
            resumen.append(f"VIH: Toma {self.vih_orden_toma or '1'}°")
        
        return " | ".join(resumen) if resumen else "Sin tamizajes registrados"