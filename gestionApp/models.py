from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from utilidad.rut_validator import validar_rut, normalizar_rut, validar_rut_chileno
from datetime import date
from django.utils import timezone


# ============================================
# MODELO BASE: PERSONA
# ============================================
class Persona(models.Model):
    SEXO_CHOICES = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('Intersexual', 'Intersexual'),
    ]
    INMIGRANTE_CHOICES = [
        ('No', 'No'),
        ('Si', 'Si'), 
    ]
    NACIONALIDAD_CHOICES = [
        ('Chile', 'Chile'),
        ('Argentina', 'Argentina'),
        ('Uruguay', 'Uruguay'),
        ('Colombia', 'Colombia'),
        ('Peru', 'Perú'),
        ('Venezuela', 'Venezuela'),
        ('Ecuador', 'Ecuador'),
        ('Brasil', 'Brasil'),
        ('Mexico', 'México'),
        ('Bolivia', 'Bolivia'),
        ('Paraguay', 'Paraguay'),
    ]
    PUEBLOS_ORIGINARIOS_CHOICES = [
        ('No pertenece', 'No pertenece'),
        ('Mapuche', 'Mapuche'),
        ('Aymara', 'Aymara'),
        ('Quechua', 'Quechua'),
        ('Guaraní', 'Guaraní'),
        ('Rapa Nui', 'Rapa Nui'),
        ('Diaguita', 'Diaguita'),
    ]
    DISCAPACIDAD_CHOICES = [
        ('No', 'No'),
        ('Si', 'Si'), 
    ]
    PRIVADA_LIBERTAD_CHOICES = [
        ('No', 'No'),
        ('Si', 'Si'), 
    ]
    TRANS_MASCULINO_CHOICES = [
        ('No', 'No'),
        ('Si', 'Si'), 
    ]
    
    Rut = models.CharField(max_length=100, unique=True, validators=[validar_rut_chileno], verbose_name="RUT", help_text="Ingrese RUT de la persona (formato: 12345678-9)")
    Nombre = models.CharField(max_length=100, verbose_name="Nombre")
    Apellido_Paterno = models.CharField(max_length=100, verbose_name="Apellido Paterno")
    Apellido_Materno = models.CharField(max_length=100, verbose_name="Apellido Materno")
    Fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")
    Sexo = models.CharField(max_length=100, choices=SEXO_CHOICES, verbose_name="Sexo")
    Inmigrante = models.CharField(max_length=10, choices=INMIGRANTE_CHOICES, default='No', verbose_name="Inmigrante")
    Nacionalidad = models.CharField(max_length=100, choices=NACIONALIDAD_CHOICES, default='Chile', verbose_name="Nacionalidad")
    Pueblos_originarios = models.CharField(max_length=100, choices=PUEBLOS_ORIGINARIOS_CHOICES, default='No pertenece', verbose_name="Pueblos originarios")
    Discapacidad = models.CharField(max_length=10, choices=DISCAPACIDAD_CHOICES, default='No', verbose_name="Discapacidad")
    Tipo_de_Discapacidad = models.CharField(max_length=200, blank=True, null=True, verbose_name="Tipo de Discapacidad", help_text="Especificar solo si tiene discapacidad")
    Privada_de_Libertad = models.CharField(max_length=10, choices=PRIVADA_LIBERTAD_CHOICES, default='No', verbose_name="Privada de Libertad")
    Trans_Masculino = models.CharField(max_length=10, choices=TRANS_MASCULINO_CHOICES, default='No', verbose_name="Trans Masculino")
    Telefono = models.CharField(max_length=100, verbose_name="Telefono", blank=True)
    Direccion = models.CharField(max_length=100, verbose_name="Direccion", blank=True)
    Email = models.CharField(max_length=100, verbose_name="Email", blank=True)
    Activo = models.BooleanField(default=True, verbose_name="Activo")
    
    def calcular_edad(self):
        """Calcula la edad actual basada en la fecha de nacimiento"""
        if not self.Fecha_nacimiento:
            return None
        hoy = date.today()
        edad = hoy.year - self.Fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.Fecha_nacimiento.month, self.Fecha_nacimiento.day))
        return edad
    
    def clean(self):
        super().clean()
        if self.Discapacidad == 'Si':
            if not self.Tipo_de_Discapacidad or self.Tipo_de_Discapacidad.strip() == '':
                raise ValidationError({'Tipo_de_Discapacidad': 'Debe especificar el tipo de discapacidad si seleccionó "Sí"'})
        if self.Discapacidad == 'No':
            self.Tipo_de_Discapacidad = None
        if self.Fecha_nacimiento:
            edad = self.calcular_edad()
            if edad and edad < 0:
                raise ValidationError({'Fecha_nacimiento': 'La fecha de nacimiento no puede ser futura.'})
    
    def save(self, *args, **kwargs):
        if self.Rut:
            self.Rut = normalizar_rut(self.Rut)
            validar_rut_chileno(self.Rut)
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.Nombre} {self.Apellido_Paterno} {self.Apellido_Materno} - {self.Rut}"


# ============================================
# MODELO PACIENTE
# ============================================
class Paciente(models.Model):
    """Rol de Paciente vinculado a Persona"""
    ESTADO_CIVIL_CHOICES = [
        ('SOLTERA', 'Soltera'),
        ('CASADA', 'Casada'),
        ('CONVIVIENTE', 'Conviviente'),
        ('DIVORCIADA', 'Divorciada'),
        ('VIUDA', 'Viuda'),
    ]
    PREVISION_CHOICES = [
        ('FONASA_A', 'FONASA A'),
        ('FONASA_B', 'FONASA B'),
        ('FONASA_C', 'FONASA C'),
        ('FONASA_D', 'FONASA D'),
        ('ISAPRE', 'Isapre'),
        ('PARTICULAR', 'Particular'),
    ]
    CONSULTORIO_CHOICES = [
        ('SIN_ESPECIFICAR', 'Sin Especificar'),
        ('CESFAM_ULTRAESTACION_DR_RAUL_SAN_MARTIN', 'CESFAM Ultraestación Dr. Raúl San Martín González (Chillán)'),
        ('CESFAM_LOS_VOLCANES', 'CESFAM Los Volcanes (Chillán)'),
        ('CESFAM_ISABEL_RIQUELME', 'CESFAM Isabel Riquelme (Chillán)'),
        ('CESFAM_QUINCHAMALI', 'CESFAM Quinchamalí (Chillán comuna)'),
        ('CESFAM_TERESA_BALDECHI', 'CESFAM Teresa Baldechi (San Carlos)'),
        ('CESFAM_DR_ALBERTO_GYHRA_SOTO', 'CESFAM Dr. Alberto Gyhra Soto (Quillón)'),
        ('CESFAM_MICHELL_CHANDIA_ALARCON', 'CESFAM Michell Chandia Alarcon (Coihueco)'),
    ]
    DUCTUS_VENOSUS_CHOICES = [
        ('SIN_ESPECIFICAR', 'Sin Especificar'),
        ('DUCTUS_VENOSUS', 'Ductus Venosus'),
        ('DUCTUS_VENOSUS_SIN_CONTROL', 'Ductus Venosus Sin Control'),
        ('DUCTUS_VENOSUS_CONTROL', 'Ductus Venosus Con Control'),
        ('DUCTUS_VENOSUS_CONTROL_SIN_PREVENCION', 'Ductus Venosus Con Control Sin Prevención'),
        ('DUCTUS_VENOSUS_CONTROL_PREVENCION', 'Ductus Venosus Con Control Con Prevención'),
        ('DUCTUS_VENOSUS_CONTROL_PREVENCION_SIN_CONTROL', 'Ductus Venosus Con Control Con Prevención Sin Control'),
    ]
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, related_name='paciente', primary_key=True)
    Estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, verbose_name="Estado Civil")
    Previcion = models.CharField("Previsión", max_length=20, choices=PREVISION_CHOICES)
    paridad = models.CharField(max_length=50, verbose_name="Paridad", blank=True, help_text="Ejemplo: G3P2A0")
    Ductus_Venosus = models.CharField(max_length=70, choices=DUCTUS_VENOSUS_CHOICES, default='SIN_ESPECIFICAR', verbose_name="Ductus Venosus")
    control_prenatal = models.BooleanField(default=True, verbose_name="¿Tuvo Control Prenatal?")
    Consultorio = models.CharField(max_length=100, choices=CONSULTORIO_CHOICES, default='SIN_ESPECIFICAR', verbose_name="Consultorio de Origen")
    IMC = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(10), MaxValueValidator(60)], verbose_name="IMC", null=True, blank=True, help_text="Índice de Masa Corporal (10-60)")
    Preeclampsia_Severa = models.BooleanField(default=False, verbose_name="Preeclampsia Severa")
    Eclampsia = models.BooleanField(default=False, verbose_name="Eclampsia")
    Sepsis_o_Infeccion_SiST = models.BooleanField(default=False, verbose_name="Sepsis o Infección Sistémica Grave")
    Infeccion_Ovular_o_Corioamnionitis = models.BooleanField(default=False, verbose_name="Infección Ovular o Corioamnionitis")
    Acompañante = models.CharField(max_length=120, blank=True, verbose_name="Acompañante")
    Contacto_emergencia = models.CharField(max_length=30, blank=True, verbose_name="Contacto de Emergencia")
    Fecha_y_Hora_Ingreso = models.DateTimeField(default=timezone.now, verbose_name="Fecha y Hora de Ingreso")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    
    @property
    def edad(self):
        """Property para obtener la edad de la persona"""
        return self.persona.calcular_edad()
    
    def calcular_imc(self, peso_kg, talla_cm):
        """Calcula el IMC basado en peso y talla"""
        if peso_kg and talla_cm and talla_cm > 0:
            talla_m = talla_cm / 100
            self.imc = round(peso_kg / (talla_m ** 2), 2)
            return self.imc
        return None
    
    def tiene_condiciones_criticas(self):
        """Verifica si tiene alguna condición crítica"""
        return (self.Preeclampsia_Severa or self.Eclampsia or self.Sepsis_o_Infeccion_SiST or self.Infeccion_Ovular_o_Corioamnionitis)
    
    def clean(self):
        super().clean()
        edad_actual = self.edad
        if edad_actual and (edad_actual < 12 or edad_actual > 60):
            raise ValidationError({'persona': f'La edad de la paciente ({edad_actual} años) debe estar entre 12 y 60 años.'})
        if self.imc:
            if self.imc < 10 or self.imc > 60:
                raise ValidationError({'imc': 'El IMC debe estar entre 10 y 60.'})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Paciente: {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno} ({self.persona.Rut})"
    
    class Meta:
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"


# ============================================
# MODELO MÉDICO
# ============================================
class Medico(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Obstetricia General', 'Obstetricia General'),
        ('Ginecología', 'Ginecología'),
        ('Medicina Materno Fetal', 'Medicina Materno Fetal'),
    ]
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES)
    Registro_medico = models.CharField(max_length=100, unique=True)
    Años_experiencia = models.IntegerField()
    Turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    Activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Dr. {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno} - {self.Especialidad}"


# ============================================
# MODELO MATRONA
# ============================================
class Matrona(models.Model):
    ESPECIALIDAD_CHOICES = [
        ('Atención del Parto', 'Atención del Parto'),
        ('Control Prenatal', 'Control Prenatal'),
        ('Neonatología', 'Neonatología'),
    ]
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Especialidad = models.CharField(max_length=100, choices=ESPECIALIDAD_CHOICES)
    Registro_medico = models.CharField(max_length=100, unique=True)
    Años_experiencia = models.IntegerField()
    Turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    Activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Matrona: {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno}"


# ============================================
# MODELO TENS
# ============================================
class Tens(models.Model):
    NIVEL_CHOICES = [
        ('Preparto', 'Preparto'),
        ('Parto', 'Parto'),
        ('Puerperio', 'Puerperio'),
        ('Neonatología', 'Neonatología'),
    ]
    TURNO_CHOICES = [
        ('Mañana', 'Mañana'),
        ('Tarde', 'Tarde'),
        ('Noche', 'Noche'),
    ]
    CERTIFICACION_CHOICES = [
        ('SVB', 'Soporte Vital Básico'),
        ('Parto Normal', 'Certificación en Parto Normal'),
    ]
    
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    Nivel = models.CharField(max_length=100, choices=NIVEL_CHOICES)
    Años_experiencia = models.IntegerField()
    Turno = models.CharField(max_length=100, choices=TURNO_CHOICES)
    Certificaciones = models.CharField(max_length=100, choices=CERTIFICACION_CHOICES)
    Activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"TENS: {self.persona.Nombre} {self.persona.Apellido_Paterno} {self.persona.Apellido_Materno} - {self.Nivel}"