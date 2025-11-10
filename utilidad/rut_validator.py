"""
VALIDADOR DE RUT CHILENO - VERSIÓN MEJORADA
Sistema completo de validación, formateo y separación de RUT
Compatible con Django y uso independiente
"""

import re
from django.core.exceptions import ValidationError
from typing import Tuple, Dict


class RutValidator:
    """Clase para validar y manipular RUTs chilenos"""
    
    @staticmethod
    def limpiar(rut: str) -> str:
        """
        Limpia el RUT eliminando puntos, guiones y espacios.
        Convierte a mayúsculas.
        
        Args:
            rut: RUT a limpiar
            
        Returns:
            RUT limpio en mayúsculas
            
        Ejemplo:
            >>> RutValidator.limpiar('12.345.678-9')
            '123456789'
        """
        if not rut:
            return ''
        
        return str(rut).replace('.', '').replace('-', '').replace(' ', '').upper()
    
    @staticmethod
    def separar(rut: str) -> Dict[str, str]:
        """
        Separa el RUT en cuerpo y dígito verificador.
        
        Args:
            rut: RUT completo
            
        Returns:
            Diccionario con 'cuerpo' y 'dv'
            
        Ejemplo:
            >>> RutValidator.separar('12345678-9')
            {'cuerpo': '12345678', 'dv': '9'}
        """
        rut_limpio = RutValidator.limpiar(rut)
        
        if len(rut_limpio) < 2:
            return {'cuerpo': '', 'dv': ''}
        
        return {
            'cuerpo': rut_limpio[:-1],
            'dv': rut_limpio[-1]
        }
    
    @staticmethod
    def calcular_dv(cuerpo: str) -> str:
        """
        Calcula el dígito verificador de un RUT.
        
        Args:
            cuerpo: Cuerpo del RUT (sin DV)
            
        Returns:
            Dígito verificador calculado ('0'-'9' o 'K')
            
        Ejemplo:
            >>> RutValidator.calcular_dv('12345678')
            '5'
        """
        # Limpiar el cuerpo (solo números)
        cuerpo_limpio = re.sub(r'\D', '', str(cuerpo))
        
        if not cuerpo_limpio:
            return ''
        
        suma = 0
        multiplicador = 2
        
        # Recorrer de derecha a izquierda
        for digito in reversed(cuerpo_limpio):
            suma += int(digito) * multiplicador
            multiplicador = 7 if multiplicador == 7 else multiplicador + 1
            if multiplicador > 7:
                multiplicador = 2
        
        resto = suma % 11
        dv_calculado = 11 - resto
        
        # Retornar el DV correspondiente
        if dv_calculado == 11:
            return '0'
        elif dv_calculado == 10:
            return 'K'
        else:
            return str(dv_calculado)
    
    @staticmethod
    def validar(rut: str) -> bool:
        """
        Valida si un RUT es correcto.
        
        Args:
            rut: RUT completo a validar
            
        Returns:
            True si es válido, False en caso contrario
            
        Ejemplo:
            >>> RutValidator.validar('12.345.678-5')
            True
        """
        rut_limpio = RutValidator.limpiar(rut)
        
        # Validar longitud mínima
        if len(rut_limpio) < 2:
            return False
        
        # Validar formato: 7-8 dígitos + dígito verificador
        if not re.match(r'^\d{7,8}[0-9Kk]$', rut_limpio):
            return False
        
        datos = RutValidator.separar(rut_limpio)
        dv_calculado = RutValidator.calcular_dv(datos['cuerpo'])
        
        return datos['dv'] == dv_calculado
    
    @staticmethod
    def formatear(rut: str) -> str:
        """
        Formatea un RUT con puntos y guión (12.345.678-9).
        
        Args:
            rut: RUT a formatear
            
        Returns:
            RUT formateado
            
        Ejemplo:
            >>> RutValidator.formatear('123456789')
            '12.345.678-9'
        """
        datos = RutValidator.separar(rut)
        
        if not datos['cuerpo'] or not datos['dv']:
            return rut
        
        # Agregar puntos cada 3 dígitos de derecha a izquierda
        cuerpo = datos['cuerpo']
        cuerpo_formateado = ''
        contador = 0
        
        for i in range(len(cuerpo) - 1, -1, -1):
            if contador == 3:
                cuerpo_formateado = '.' + cuerpo_formateado
                contador = 0
            cuerpo_formateado = cuerpo[i] + cuerpo_formateado
            contador += 1
        
        return f"{cuerpo_formateado}-{datos['dv']}"
    
    @staticmethod
    def normalizar(rut: str) -> str:
        """
        Normaliza el RUT al formato sin puntos pero con guión (12345678-9).
        Este es el formato que se guarda en la base de datos.
        
        Args:
            rut: RUT a normalizar
            
        Returns:
            RUT normalizado
            
        Ejemplo:
            >>> RutValidator.normalizar('12.345.678-9')
            '12345678-9'
        """
        datos = RutValidator.separar(rut)
        
        if not datos['cuerpo'] or not datos['dv']:
            return rut
        
        return f"{datos['cuerpo']}-{datos['dv']}"


# ============================================
# FUNCIONES AUXILIARES PARA DJANGO
# ============================================

def validar_rut_chileno(value: str) -> str:
    """
    Validador de Django para campo RUT.
    Lanza ValidationError si el RUT no es válido.
    
    Args:
        value: RUT a validar
        
    Returns:
        RUT normalizado
        
    Raises:
        ValidationError: Si el RUT no es válido
    """
    if not value:
        raise ValidationError('El RUT es obligatorio.')
    
    rut_limpio = RutValidator.limpiar(value)
    
    # Validar formato
    if not re.match(r'^\d{7,8}[0-9Kk]$', rut_limpio):
        raise ValidationError(
            'Formato de RUT inválido. Use el formato: 12345678-9'
        )
    
    # Validar dígito verificador
    if not RutValidator.validar(value):
        raise ValidationError(
            'El dígito verificador del RUT es incorrecto.'
        )
    
    # Retornar normalizado
    return RutValidator.normalizar(value)


def normalizar_rut(rut: str) -> str:
    """
    Alias de RutValidator.normalizar para compatibilidad.
    
    Args:
        rut: RUT a normalizar
        
    Returns:
        RUT normalizado (formato: 12345678-9)
    """
    return RutValidator.normalizar(rut)


def validar_rut(value: str) -> str:
    """
    Alias de validar_rut_chileno para compatibilidad.
    """
    return validar_rut_chileno(value)


# ============================================
# GENERADOR DE RUT ALEATORIO (ÚTIL PARA TESTING)
# ============================================

def generar_rut_aleatorio() -> str:
    """
    Genera un RUT chileno válido aleatorio.
    Útil para pruebas y testing.
    
    Returns:
        RUT válido formateado
        
    Ejemplo:
        >>> rut = generar_rut_aleatorio()
        >>> RutValidator.validar(rut)
        True
    """
    import random
    
    # Generar cuerpo aleatorio (entre 1.000.000 y 99.999.999)
    cuerpo = random.randint(1000000, 99999999)
    dv = RutValidator.calcular_dv(str(cuerpo))
    
    return RutValidator.formatear(f"{cuerpo}{dv}")


# ============================================
# EJEMPLOS DE USO
# ============================================

if __name__ == '__main__':
    print("=== EJEMPLOS DE USO DEL VALIDADOR DE RUT ===\n")
    
    # Ejemplo 1: Validar RUT
    rut_test = '12.345.678-5'
    print(f"1. Validar RUT: {rut_test}")
    print(f"   ¿Es válido? {RutValidator.validar(rut_test)}\n")
    
    # Ejemplo 2: Separar RUT
    print(f"2. Separar RUT: {rut_test}")
    datos = RutValidator.separar(rut_test)
    print(f"   Cuerpo: {datos['cuerpo']}")
    print(f"   DV: {datos['dv']}\n")
    
    # Ejemplo 3: Calcular DV
    cuerpo = '12345678'
    print(f"3. Calcular DV para: {cuerpo}")
    dv = RutValidator.calcular_dv(cuerpo)
    print(f"   DV calculado: {dv}\n")
    
    # Ejemplo 4: Formatear RUT
    rut_sin_formato = '123456785'
    print(f"4. Formatear RUT: {rut_sin_formato}")
    print(f"   Formateado: {RutValidator.formatear(rut_sin_formato)}\n")
    
    # Ejemplo 5: Normalizar RUT
    rut_con_puntos = '12.345.678-5'
    print(f"5. Normalizar RUT: {rut_con_puntos}")
    print(f"   Normalizado: {RutValidator.normalizar(rut_con_puntos)}\n")
    
    # Ejemplo 6: Generar RUT aleatorio
    print("6. Generar RUT aleatorio:")
    rut_aleatorio = generar_rut_aleatorio()
    print(f"   RUT generado: {rut_aleatorio}")
    print(f"   ¿Es válido? {RutValidator.validar(rut_aleatorio)}\n")