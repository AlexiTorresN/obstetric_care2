from django.db import models

class Patologias(models.Model):
    """Catálogo de patologías obstétricas"""

    CIE_10_CHOICES = [
        ('O10', 'O10 - Hipertensión preexistente'),
        ('O24', 'O24 - Diabetes mellitus en el embarazo'),
        ('O14', 'O14 - Preeclampsia'),
        ('O99.0', 'O99.0 - Anemia en el embarazo'),
        ('O99.2', 'O99.2 - Enfermedades endocrinas'),
        ('O26', 'O26 - Otras complicaciones del embarazo'),
        ('Otra', 'Otra patología obstétrica'),
    ]

    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    
    NIVEL_RIESGO_CHOICES = [
        ('Bajo', 'Bajo'),
        ('Medio', 'Medio'),
        ('Alto', 'Alto'),
        ('Crítico', 'Crítico'),
    ]

    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre de la patología",
        help_text="Nombre completo de la patología obstétrica"
    )

    codigo_cie_10 = models.CharField(
        max_length=100,
        choices=CIE_10_CHOICES,
        verbose_name="Código CIE-10",
        help_text="Clasificación Internacional de Enfermedades"
    )

    descripcion = models.TextField(
        blank=True,  # ✅ CAMBIADO: Ahora es opcional
        null=True,   # ✅ CAMBIADO: Ahora es opcional
        verbose_name="Descripción",
        help_text="Detalles adicionales sobre la patología"
    )

    nivel_de_riesgo = models.CharField(
        max_length=20,  # ✅ CAMBIADO: Reducido de 50 a 20
        choices=NIVEL_RIESGO_CHOICES,  # ✅ CAMBIADO: Nombre corregido
        verbose_name="Nivel de riesgo",
        help_text="Nivel de riesgo para la gestante"
    )

    protocolo_seguimiento = models.TextField(  # ✅ CAMBIADO: Nombre corregido (era protocologo_de_segimiento)
        blank=True,  # ✅ CAMBIADO: Ahora es opcional
        null=True,   # ✅ CAMBIADO: Ahora es opcional
        verbose_name="Protocolo de seguimiento",
        help_text="Indicaciones médicas para el seguimiento"
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='Activo',
        verbose_name="Estado",
        help_text="Estado actual del registro"
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo_cie_10})"

    class Meta:
        verbose_name = "Patología"
        verbose_name_plural = "Patologías"
        ordering = ['-fecha_creacion']