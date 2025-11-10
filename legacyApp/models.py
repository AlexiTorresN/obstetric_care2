# legacyApp/models.py
from django.db import models

class ControlesPrevios(models.Model):
    paciente_rut = models.CharField(max_length=12)
    fecha_control = models.DateField()
    semanas_gestacion = models.IntegerField(null=True, blank=True)
    presion_sistolica = models.IntegerField(null=True, blank=True)
    presion_diastolica = models.IntegerField(null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    altura_uterina_cm = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    fcf_lpm = models.IntegerField(null=True, blank=True)
    glucosa_mg_dl = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    proteinuria = models.CharField(max_length=10, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'controles_previos'
        ordering = ['-fecha_control']

    def __str__(self):
        return f"Control {self.fecha_control} ({self.paciente_rut})"
