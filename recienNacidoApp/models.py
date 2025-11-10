from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# ============================================
# ✅ REGISTRO DE RECIÉN NACIDO (ÚNICO LUGAR)
# ============================================

class RegistroRecienNacido(models.Model):
    """
    Registro del recién nacido
    Se crea después del parto
    Contiene datos del RN, apego y acompañamiento
    """
    
    # ============================================
    # RELACIÓN
    # ============================================
    
    registro_parto = models.ForeignKey(
        'partosApp.RegistroParto',
        on_delete=models.CASCADE,
        related_name='recien_nacidos',
        verbose_name='Registro de Parto'
    )
    
    # ============================================
    # SECCIÓN 1: DATOS DEL RECIÉN NACIDO
    # ============================================
    
    SEXO_CHOICES = [
        ('MASCULINO', 'Masculino'),
        ('FEMENINO', 'Femenino'),
        ('INDETERMINADO', 'Indeterminado'),
    ]
    
    sexo = models.CharField(
        max_length=20,
        choices=SEXO_CHOICES,
        verbose_name='Sexo',
        help_text='Sexo del recién nacido'
    )
    
    peso = models.IntegerField(
        validators=[MinValueValidator(500), MaxValueValidator(8000)],
        verbose_name='Peso (gramos)',
        help_text='Peso al nacer en gramos'
    )
    
    talla = models.IntegerField(
        validators=[MinValueValidator(30), MaxValueValidator(70)],
        verbose_name='Talla (cm)',
        help_text='Longitud al nacer en centímetros'
    )
    
    ligadura_tardia_cordon = models.BooleanField(
        default=False,
        verbose_name='Ligadura Tardía del Cordón (> 1 minuto)',
        help_text='¿Se realizó ligadura tardía del cordón umbilical?'
    )
    
    apgar_1_minuto = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar al Minuto',
        help_text='Puntaje de Apgar al primer minuto de vida'
    )
    
    apgar_5_minutos = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Apgar a los 5 Minutos',
        help_text='Puntaje de Apgar a los 5 minutos de vida'
    )
    
    fecha_nacimiento = models.DateTimeField(
        verbose_name='Fecha y Hora de Nacimiento',
        help_text='Momento exacto del nacimiento'
    )
    
    # ============================================
    # SECCIÓN 2: APEGO
    # ============================================
    
    tiempo_apego = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Tiempo de Apego (minutos)',
        help_text='Duración del apego piel con piel'
    )
    
    apego_canguro = models.BooleanField(
        default=False,
        verbose_name='Apego Canguro',
        help_text='¿Se realizó método canguro?'
    )
    
    # ============================================
    # SECCIÓN 3: ACOMPAÑAMIENTO
    # ============================================
    
    acompanamiento_preparto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento en Preparto',
        help_text='¿Hubo acompañante en preparto?'
    )
    
    acompanamiento_parto = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento en Parto',
        help_text='¿Hubo acompañante durante el parto?'
    )
    
    acompanamiento_rn = models.BooleanField(
        default=False,
        verbose_name='Acompañamiento del RN',
        help_text='¿Hubo acompañante con el recién nacido?'
    )
    
    MOTIVO_NO_ACOMP_CHOICES = [
        ('NO_DESEA', 'No desea'),
        ('NO_LLEGA', 'No llega acompañante'),
        ('URGENCIA', 'Urgencia'),
        ('NO_TIENE', 'No tiene acompañante'),
        ('RURALIDAD', 'Ruralidad'),
        ('SIN_PASE', 'Sin pase de movilidad'),
    ]
    
    motivo_no_acompanado = models.CharField(
        max_length=20,
        choices=MOTIVO_NO_ACOMP_CHOICES,
        blank=True,
        verbose_name='Motivo Parto NO Acompañado',
        help_text='Razón por la cual no hubo acompañamiento'
    )
    
    PERSONA_ACOMP_CHOICES = [
        ('PAREJA', 'Pareja'),
        ('MADRE', 'Madre'),
        ('HERMANA', 'Hermana'),
        ('AMIGA', 'Amiga'),
        ('OTRO', 'Otro'),
        ('NADIE', 'Nadie'),
    ]
    
    persona_acompanante = models.CharField(
        max_length=10,
        choices=PERSONA_ACOMP_CHOICES,
        blank=True,
        verbose_name='Persona Acompañante',
        help_text='Quién acompañó a la paciente'
    )
    
    acompanante_secciona_cordon = models.BooleanField(
        default=False,
        verbose_name='Acompañante Secciona Cordón',
        help_text='¿El acompañante cortó el cordón umbilical?'
    )
    
    # ============================================
    # METADATOS
    # ============================================
    
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación del Registro'
    )
    
    class Meta:
        ordering = ['-fecha_nacimiento']
        verbose_name = 'Registro de Recién Nacido'
        verbose_name_plural = 'Registros de Recién Nacidos'
        indexes = [
            models.Index(fields=['registro_parto', '-fecha_nacimiento']),
        ]
    
    def __str__(self):
        return f"RN - {self.registro_parto.numero_registro} - {self.sexo}"
    
    def clasificacion_peso(self):
        """Clasifica el peso del RN según OMS"""
        if self.peso < 2500:
            return "Bajo peso al nacer"
        elif 2500 <= self.peso <= 4000:
            return "Peso normal"
        else:
            return "Macrosómico"
    
    def estado_apgar(self):
        """Evalúa el estado según Apgar a los 5 minutos"""
        if self.apgar_5_minutos >= 7:
            return "Normal"
        elif 4 <= self.apgar_5_minutos <= 6:
            return "Asfixia moderada"
        else:
            return "Asfixia severa"
    
    def tuvo_acompanamiento_completo(self):
        """Verifica si hubo acompañamiento en todas las etapas"""
        return all([
            self.acompanamiento_preparto,
            self.acompanamiento_parto,
            self.acompanamiento_rn,
        ])


# ============================================
# ✅ DOCUMENTOS DE PARTO (MOVIDO DESDE partosApp)
# ============================================

class DocumentosParto(models.Model):
    """
    Documentos y procedimientos post-parto
    Incluye: placenta, registro civil, Ley Dominga
    """
    
    # ============================================
    # RELACIÓN
    # ============================================
    
    registro_recien_nacido = models.OneToOneField(
        RegistroRecienNacido,
        on_delete=models.CASCADE,
        related_name='documentos',
        verbose_name='Registro de Recién Nacido'
    )
    
    # ============================================
    # LEY N° 21.372 DOMINGA (Recuerdos)
    # ============================================
    
    recuerdos_entregados = models.TextField(
        blank=True,
        verbose_name='Cuales Recuerdos (De no entregar justificar motivo)',
        help_text='Descripción de recuerdos entregados según Ley Dominga'
    )
    
    # ============================================
    # PLACENTA
    # ============================================
    
    retira_placenta = models.BooleanField(
        default=False,
        verbose_name='Retira Placenta',
        help_text='¿La familia retira la placenta?'
    )
    
    estampado_placenta = models.BooleanField(
        default=False,
        verbose_name='Estampado de Placenta',
        help_text='¿Se realizó estampado de placenta?'
    )
    
    # ============================================
    # REGISTRO CIVIL
    # ============================================
    
    folio_valido = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='FOLIO VÁLIDO',
        help_text='Número de folio válido del Registro Civil'
    )
    
    folios_nulos = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='FOLIO/S NULO/S',
        help_text='Folios anulados (si aplica)'
    )
    
    # ============================================
    # OTROS
    # ============================================
    
    manejo_dolor_no_farmacologico = models.TextField(
        blank=True,
        verbose_name='Manejo del Dolor No Farmacológico',
        help_text='Descripción de métodos no farmacológicos utilizados'
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
        verbose_name='Fecha de Última Modificación'
    )
    
    class Meta:
        verbose_name = 'Documentos de Parto'
        verbose_name_plural = 'Documentos de Partos'
    
    def __str__(self):
        return f"Documentos - RN {self.registro_recien_nacido.id}"
    
    def tiene_documentacion_completa(self):
        """Verifica si la documentación está completa"""
        return bool(self.folio_valido)
    
    def resumen_documentos(self):
        """Retorna un resumen de la documentación"""
        docs = []
        
        if self.folio_valido:
            docs.append(f"Folio RC: {self.folio_valido}")
        
        if self.retira_placenta:
            docs.append("Placenta retirada")
        
        if self.estampado_placenta:
            docs.append("Estampado realizado")
        
        if self.recuerdos_entregados:
            docs.append("Recuerdos Ley Dominga entregados")
        
        return " | ".join(docs) if docs else "Sin documentación registrada"