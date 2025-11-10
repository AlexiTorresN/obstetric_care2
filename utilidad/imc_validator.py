from django.core.exceptions import ValidationError

def calcular_imc(peso_kg, talla_cm):
    """
    Calcula el IMC basado en peso en kg y talla en cm
    
    Args:
        peso_kg (float): Peso en kilogramos
        talla_cm (float): Talla en centímetros
        
    Returns:
        float: IMC calculado con 2 decimales
        
    Raises:
        ValueError: Si los valores son inválidos
    """
    if not peso_kg or not talla_cm:
        raise ValueError("Peso y talla son requeridos")
    
    if peso_kg <= 0:
        raise ValueError("El peso debe ser mayor a 0")
    
    if talla_cm <= 0:
        raise ValueError("La talla debe ser mayor a 0")
    
    # Convertir talla de cm a metros
    talla_m = talla_cm / 100
    
    # Calcular IMC: peso / talla²
    imc = round(peso_kg / (talla_m ** 2), 2)
    
    return imc


def validar_imc(value):
    """
    Validador Django para el campo IMC
    Valida que el IMC esté en el rango 10-60
    """
    if value is None:
        return  # Permitir valores nulos
    
    if value < 10:
        raise ValidationError(
            f'El IMC ({value}) es demasiado bajo. Debe ser mayor o igual a 10.',
            code='imc_bajo'
        )
    
    if value > 60:
        raise ValidationError(
            f'El IMC ({value}) es demasiado alto. Debe ser menor o igual a 60.',
            code='imc_alto'
        )


def clasificar_imc(imc):
    """
    Clasifica el IMC según los estándares de la OMS
    
    Args:
        imc (float): Valor del IMC
        
    Returns:
        tuple: (clasificacion, nivel_riesgo)
    """
    if imc is None:
        return ('No calculado', 'sin_datos')
    
    if imc < 18.5:
        return ('Bajo peso', 'bajo')
    elif imc < 25:
        return ('Peso normal', 'normal')
    elif imc < 30:
        return ('Sobrepeso', 'moderado')
    elif imc < 35:
        return ('Obesidad grado I', 'alto')
    elif imc < 40:
        return ('Obesidad grado II', 'muy_alto')
    else:
        return ('Obesidad grado III (mórbida)', 'extremo')


def imc_para_embarazadas(imc, semanas_gestacion):
    """
    Interpreta el IMC considerando el embarazo
    El IMC normal durante el embarazo varía según el trimestre
    
    Args:
        imc (float): IMC actual
        semanas_gestacion (int): Semanas de gestación
        
    Returns:
        tuple: (clasificacion, recomendacion_ganancia_peso)
    """
    if imc is None or semanas_gestacion is None:
        return ('No calculable', 'Consulte con su médico')
    
    # Clasificación según IMC pre-gestacional
    if imc < 18.5:
        ganancia = '12.5-18 kg'
        clasificacion = 'Bajo peso pre-gestacional'
    elif imc < 25:
        ganancia = '11.5-16 kg'
        clasificacion = 'Peso normal pre-gestacional'
    elif imc < 30:
        ganancia = '7-11.5 kg'
        clasificacion = 'Sobrepeso pre-gestacional'
    else:
        ganancia = '5-9 kg'
        clasificacion = 'Obesidad pre-gestacional'
    
    return (clasificacion, f'Ganancia de peso recomendada: {ganancia}')


# Ejemplo de uso en el modelo:
"""
from utilidad.imc_validator import calcular_imc, validar_imc

class Paciente(models.Model):
    imc = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[validar_imc],
        verbose_name="IMC", 
        null=True, 
        blank=True
    )
    
    def calcular_imc_actual(self, peso_kg, talla_cm):
        from utilidad.imc_validator import calcular_imc
        try:
            self.imc = calcular_imc(peso_kg, talla_cm)
            return self.imc
        except ValueError as e:
            raise ValidationError(str(e))
"""