from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class RegistroParto(models.Model):

    # ============================================
    # RELACIONES
    # ============================================
    
    ficha = models.ForeignKey(
        'matronaApp.FichaObstetrica',
        on_delete=models.PROTECT,
        related_name='registros_parto',
        verbose_name='Ficha Obstétrica'
    )
    
    ficha_ingreso = models.OneToOneField(
        'ingresoPartoApp.FichaParto',
        on_delete=models.PROTECT,
        related_name='registro_parto',
        null=True,
        blank=True,
        verbose_name='Ficha de Ingreso',
        help_text='Vincula con la ficha de ingreso'
    )
    
    numero_registro = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Registro',
        help_text='Se genera automáticamente: PARTO-000001'
    )
    
    # ============================================
    # FECHAS Y HORAS
    # ============================================
    
    fecha_hora_admision = models.DateTimeField(
        default=timezone.now,
        verbose_name='Fecha y Hora de Admisión',
        help_text='Cuando ingresa para el parto'
    )
    
    fecha_hora_parto = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha y Hora del Parto',
        help_text='Momento exacto del nacimiento'
    )
    
    # ============================================
    # SECCIÓN 1: TRABAJO DE PARTO
    # ============================================
    
    # VIH al Ingreso (CAMPOS FALTANTES AGREGADOS)
    vih_tomado_prepartos = models.BooleanField(
        default=False,
        verbose_name='VIH tomado en Prepartos',
        help_text='¿Se tomó VIH al ingresar a prepartos?'
    )
    
    VIH_SALA_CHOICES = [
        ('NO', 'No'),
        ('SALA_1', 'Sala 1'),
        ('SALA_2', 'Sala 2'),
        ('SALA_3', 'Sala 3'),
    ]
    
    vih_tomado_sala = models.CharField(
        max_length=20,
        choices=VIH_SALA_CHOICES,
        default='NO',
        verbose_name='VIH tomado en Sala',
        help_text='Sala donde se tomó el VIH (si aplica)'
    )
    
    # Edad Gestacional
    edad_gestacional_semanas = models.IntegerField(
        validators=[MinValueValidator(20), MaxValueValidator(42)],
        verbose_name='Semanas de Embarazo',
        help_text='Semanas completas al momento del parto'
    )
    
    edad_gestacional_dias = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        verbose_name='Días adicionales',
        help_text='Ej: 38 semanas y 4 días'
    )
    
    # Monitoreo
    monitor_ttc = models.BooleanField(
        default=False,
        verbose_name='Monitor TTC',
        help_text='¿Se usó monitor de contracciones?'
    )
    
    induccion = models.BooleanField(
        default=False,
        verbose_name='Inducción',
        help_text='¿Se indujo el parto?'
    )
    
    aceleracion_correccion = models.BooleanField(
        default=False,
        verbose_name='Aceleración o Corrección',
        help_text='¿Se aceleró el trabajo de parto?'
    )
    
    numero_tactos_vaginales = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Número de Tactos Vaginales (TV)',
        help_text='Número total de exámenes vaginales realizados'
    )
    
    # Rotura de Membranas
    ROTURA_MEMBRANA_CHOICES = [
        ('IOP', 'Inicio Espontáneo (IOP)'),
        ('RAM', 'Rotura Artificial de Membranas (RAM)'),
        ('REM', 'Rotura Espontánea de Membranas (REM)'),
        ('RPM', 'Rotura Prematura de Membranas (RPM)'),
    ]
    
    rotura_membrana = models.CharField(
        max_length=10,
        choices=ROTURA_MEMBRANA_CHOICES,
        blank=True,
        verbose_name='Rotura de Membrana'
    )
    
    tiempo_membranas_rotas = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Membranas Rotas (minutos)',
        help_text='Tiempo transcurrido con membranas rotas'
    )
    
    # Tiempos del Parto
    tiempo_dilatacion = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Dilatación (minutos)',
        help_text='Duración de la fase de dilatación'
    )
    
    tiempo_expulsivo = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo Expulsivo (minutos)',
        help_text='Duración de la fase expulsiva'
    )
    
    # ============================================
    # SECCIÓN 2: INFORMACIÓN DEL PARTO
    # ============================================
    
    libertad_movimiento = models.BooleanField(
        default=True,
        verbose_name='Libertad de Movimiento en Trabajo de Parto',
        help_text='¿La paciente tuvo libertad de movimiento?'
    )
    
    REGIMEN_CHOICES = [
        ('CERO', 'Cero (ayuno absoluto)'),
        ('LIQUIDO', 'Líquido'),
        ('COMUN', 'Común'),
        ('OTRO', 'Otro'),
    ]
    
    tipo_regimen = models.CharField(
        max_length=10,
        choices=REGIMEN_CHOICES,
        default='LIQUIDO',
        verbose_name='Tipo de Régimen en Trabajo de Parto'
    )
    
    TIPO_PARTO_CHOICES = [
        ('EUTOCICO', 'Eutócico (normal)'),
        ('DISTOCICO', 'Distócico (con complicaciones)'),
        ('CESAREA_URGENCIA', 'Cesárea de Urgencia'),
        ('CESAREA_ELECTIVA', 'Cesárea Electiva'),
    ]
    
    tipo_parto = models.CharField(
        max_length=20,
        choices=TIPO_PARTO_CHOICES,
        verbose_name='Tipo de Parto'
    )
    
    alumbramiento_dirigido = models.BooleanField(
        default=True,
        verbose_name='Alumbramiento Dirigido',
        help_text='¿Se realizó alumbramiento dirigido?'
    )
    
    # Clasificación de Robson
    ROBSON_CHOICES = [
        ('Grupo 1', 'Grupo 1 - Nulíparas, único, cefálico, ≥37 sem, espontáneo'),
        ('Grupo 2.A', 'Grupo 2.A - Nulíparas, único, cefálico, ≥37 sem, inducción'),
        ('Grupo 2.B', 'Grupo 2.B - Nulíparas, único, cefálico, ≥37 sem, cesárea antes trabajo'),
        ('Grupo 3', 'Grupo 3 - Multíparas, único, cefálico, ≥37 sem, espontáneo'),
        ('Grupo 4', 'Grupo 4 - Multíparas, único, cefálico, ≥37 sem, inducción o cesárea'),
        ('Grupo 5.1', 'Grupo 5.1 - Multíparas, único, cefálico, ≥37 sem, cesárea previa, espontáneo'),
        ('Grupo 5.2', 'Grupo 5.2 - Multíparas, único, cefálico, ≥37 sem, cesárea previa, inducción'),
        ('Grupo 6', 'Grupo 6 - Nulíparas, único, podálica'),
        ('Grupo 7', 'Grupo 7 - Multíparas, único, podálica'),
        ('Grupo 8', 'Grupo 8 - Embarazos múltiples'),
        ('Grupo 9', 'Grupo 9 - Único, transversa u oblicua'),
        ('Grupo 10', 'Grupo 10 - Único, cefálico, ≤36 sem'),
    ]
    
    clasificacion_robson = models.CharField(
        max_length=30,
        choices=ROBSON_CHOICES,
        verbose_name='Clasificación de Robson',
        help_text='Clasificación de Robson para cesáreas'
    )
    
    # Posición Materna
    POSICION_CHOICES = [
        ('SEMISENTADA', 'Semisentada'),
        ('SENTADA', 'Sentada'),
        ('LITOTOMIA', 'Litotomía (acostada)'),
        ('D_DORSAL', 'Decúbito Dorsal'),
        ('D_LATERAL', 'Decúbito Lateral'),
        ('CUADRUPEDA', 'Cuadrúpeda'),
        ('CUCLILLAS', 'Cuclillas'),
        ('DE_PIE', 'De Pie'),
        ('OTRO', 'Otro'),
    ]
    
    posicion_materna_parto = models.CharField(
        max_length=20,
        choices=POSICION_CHOICES,
        verbose_name='Posición Materna en el Parto'
    )
    
    ofrecimiento_posiciones_alternativas = models.BooleanField(
        default=True,
        verbose_name='Ofrecimiento de Posiciones Alternativas del Parto',
        help_text='¿Se ofrecieron posiciones alternativas?'
    )
    
    # ============================================
    # SECCIÓN 3: PUERPERIO
    # ============================================
    
    ESTADO_PERINE_CHOICES = [
        ('INDEMNE', 'Indemne (sin lesión)'),
        ('DESGARRO_G1', 'Desgarro Grado 1'),
        ('DESGARRO_G2', 'Desgarro Grado 2'),
        ('DESGARRO_G3_A', 'Desgarro Grado 3A'),
        ('DESGARRO_G3_B', 'Desgarro Grado 3B'),
        ('DESGARRO_G3_C', 'Desgarro Grado 3C'),
        ('DESGARRO_G4', 'Desgarro Grado 4'),
        ('FISURA', 'Fisura'),
        ('EPISIOTOMIA', 'Episiotomía'),
    ]
    
    estado_perine = models.CharField(
        max_length=20,
        choices=ESTADO_PERINE_CHOICES,
        verbose_name='Estado del Periné'
    )
    
    esterilizacion = models.BooleanField(
        default=False,
        verbose_name='Esterilización',
        help_text='¿Se realizó esterilización?'
    )
    
    revision = models.BooleanField(
        default=True,
        verbose_name='Revisión del Canal del Parto'
    )
    
    # Complicaciones del Puerperio
    inercia_uterina = models.BooleanField(
        default=False,
        verbose_name='Inercia Uterina'
    )
    
    restos_placentarios = models.BooleanField(
        default=False,
        verbose_name='Restos Placentarios'
    )
    
    trauma = models.BooleanField(
        default=False,
        verbose_name='Trauma'
    )
    
    alteracion_coagulacion = models.BooleanField(
        default=False,
        verbose_name='Alteración de la Coagulación'
    )
    
    manejo_quirurgico_inercia = models.BooleanField(
        default=False,
        verbose_name='Manejo Quirúrgico de Inercia Uterina'
    )
    
    histerectomia_obstetrica = models.BooleanField(
        default=False,
        verbose_name='Histerectomía Obstétrica'
    )
    
    transfusion_sanguinea = models.BooleanField(
        default=False,
        verbose_name='Transfusión Sanguínea'
    )
    
    # ============================================
    # SECCIÓN 4: ANESTESIA Y ANALGESIA
    # ============================================
    
    # Anestesia
    anestesia_neuroaxial = models.BooleanField(
        default=False,
        verbose_name='Anestesia Neuroaxial'
    )
    
    oxido_nitroso = models.BooleanField(
        default=False,
        verbose_name='Óxido Nitroso'
    )
    
    analgesia_endovenosa = models.BooleanField(
        default=False,
        verbose_name='Analgesia Endovenosa'
    )
    
    anestesia_general = models.BooleanField(
        default=False,
        verbose_name='Anestesia General'
    )
    
    anestesia_local = models.BooleanField(
        default=False,
        verbose_name='Anestesia Local'
    )
    
    # Analgesia No Farmacológica
    analgesia_no_farmacologica = models.BooleanField(
        default=False,
        verbose_name='Analgesia NO Farmacológica'
    )
    
    balon_kinesico = models.BooleanField(
        default=False,
        verbose_name='Balón Kinésico'
    )
    
    lenteja_parto = models.BooleanField(
        default=False,
        verbose_name='Lenteja de Parto'
    )
    
    rebozo = models.BooleanField(
        default=False,
        verbose_name='Rebozo'
    )
    
    aromaterapia = models.BooleanField(
        default=False,
        verbose_name='Aromaterapia'
    )
    
    # Anestesia Peridural
    peridural_solicitada_paciente = models.BooleanField(
        default=False,
        verbose_name='Peridural Solicitada por Paciente'
    )
    
    peridural_indicada_medico = models.BooleanField(
        default=False,
        verbose_name='Peridural Indicada por Médico GO'
    )
    
    peridural_administrada = models.BooleanField(
        default=False,
        verbose_name='Peridural Administrada'
    )
    
    tiempo_espera_peridural = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo de espera entre indicación y administración (minutos)',
        help_text='Tiempo de espera para administración de peridural'
    )
    
    # ============================================
    # SECCIÓN 5: INFORMACIÓN DE LOS PROFESIONALES
    # ============================================
    
    profesional_responsable = models.CharField(
        max_length=200,
        verbose_name='Profesional Responsable (Nombre - apellido)',
        help_text='Profesional a cargo del parto'
    )
    
    alumno = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Alumno (Nombre - apellido)',
        help_text='Estudiante que participó en el parto'
    )
    
    causa_cesarea = models.TextField(
        blank=True,
        verbose_name='Causa de Cesárea',
        help_text='Motivo por el cual se realizó cesárea'
    )
    
    observaciones = models.TextField(
        blank=True,
        verbose_name='Observaciones',
        help_text='Observaciones generales del parto'
    )
    
    uso_sala_saip = models.BooleanField(
        default=False,
        verbose_name='USO DE SALA SAIP (SI/NO)',
        help_text='¿Se usó la sala SAIP (Sala de Atención Integral del Parto)?'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Modificación'
    )
    
    activo = models.BooleanField(
        default=True,
        verbose_name='Registro Activo'
    )
    
    class Meta:
        ordering = ['-fecha_hora_admision']
        verbose_name = 'Registro de Parto'
        verbose_name_plural = 'Registros de Parto'
        indexes = [
            models.Index(fields=['numero_registro']),
            models.Index(fields=['ficha', '-fecha_hora_admision']),
            models.Index(fields=['-fecha_hora_parto']),
        ]
    
    def __str__(self):
        return f"{self.numero_registro} - {self.ficha.paciente.persona.Nombre}"
    
    def save(self, *args, **kwargs):
        """Generar número automático si no existe"""
        if not self.numero_registro:
            ultimo = RegistroParto.objects.order_by('-id').first()
            if ultimo:
                try:
                    numero = int(ultimo.numero_registro.split('-')[1]) + 1
                except (IndexError, ValueError):
                    numero = 1
            else:
                numero = 1
            self.numero_registro = f"PARTO-{numero:06d}"
        super().save(*args, **kwargs)
    
    def duracion_total_parto(self):
        """Calcula duración total del parto en minutos"""
        if self.tiempo_dilatacion and self.tiempo_expulsivo:
            return self.tiempo_dilatacion + self.tiempo_expulsivo
        return None
    
    def tiene_complicaciones(self):
        """Verifica si hubo complicaciones"""
        return (
            self.inercia_uterina or
            self.restos_placentarios or
            self.trauma or
            self.alteracion_coagulacion or
            self.histerectomia_obstetrica or
            self.transfusion_sanguinea
        )
    
    def tipo_analgesia_utilizada(self):
        """Retorna lista de tipos de analgesia utilizados"""
        analgesias = []
        
        if self.anestesia_neuroaxial:
            analgesias.append('Neuroaxial')
        if self.oxido_nitroso:
            analgesias.append('Óxido Nitroso')
        if self.analgesia_endovenosa:
            analgesias.append('Endovenosa')
        if self.anestesia_general:
            analgesias.append('General')
        if self.anestesia_local:
            analgesias.append('Local')
        if self.analgesia_no_farmacologica:
            analgesias.append('No Farmacológica')
        
        return ', '.join(analgesias) if analgesias else 'Sin analgesia registrada'