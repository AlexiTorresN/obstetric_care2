/**
 * VALIDADOR DE RUT CHILENO
 * Sistema completo de validación y formateo de RUT
 * Compatible con todos los formularios del proyecto
 */

class RutValidator {
    /**
     * Limpia el RUT eliminando puntos, guiones y espacios
     * @param {string} rut - RUT a limpiar
     * @returns {string} - RUT limpio
     */
    static limpiar(rut) {
        if (!rut) return '';
        return rut.toString()
            .replace(/\./g, '')
            .replace(/-/g, '')
            .replace(/\s/g, '')
            .toUpperCase();
    }

    /**
     * Separa el RUT en cuerpo y dígito verificador
     * @param {string} rut - RUT a separar
     * @returns {object} - {cuerpo: string, dv: string}
     */
    static separar(rut) {
        const rutLimpio = this.limpiar(rut);
        
        if (rutLimpio.length < 2) {
            return { cuerpo: '', dv: '' };
        }

        return {
            cuerpo: rutLimpio.slice(0, -1),
            dv: rutLimpio.slice(-1).toUpperCase()
        };
    }

    /**
     * Calcula el dígito verificador de un RUT
     * @param {string} cuerpo - Cuerpo del RUT (sin DV)
     * @returns {string} - Dígito verificador calculado
     */
    static calcularDV(cuerpo) {
        const cuerpoLimpio = cuerpo.replace(/\D/g, '');
        
        if (!cuerpoLimpio || cuerpoLimpio.length === 0) {
            return '';
        }

        let suma = 0;
        let multiplicador = 2;

        // Recorrer el cuerpo de derecha a izquierda
        for (let i = cuerpoLimpio.length - 1; i >= 0; i--) {
            suma += parseInt(cuerpoLimpio.charAt(i)) * multiplicador;
            multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
        }

        const resto = suma % 11;
        const dvCalculado = 11 - resto;

        // Retornar el DV correspondiente
        if (dvCalculado === 11) return '0';
        if (dvCalculado === 10) return 'K';
        return dvCalculado.toString();
    }

    /**
     * Valida si un RUT es correcto
     * @param {string} rut - RUT completo a validar
     * @returns {boolean} - true si es válido
     */
    static validar(rut) {
        const rutLimpio = this.limpiar(rut);

        // Validar longitud mínima
        if (rutLimpio.length < 2) {
            return false;
        }

        // Validar formato (solo números y K/k al final)
        if (!/^\d{7,8}[0-9Kk]$/.test(rutLimpio)) {
            return false;
        }

        const { cuerpo, dv } = this.separar(rutLimpio);
        const dvCalculado = this.calcularDV(cuerpo);

        return dv === dvCalculado;
    }

    /**
     * Formatea un RUT con puntos y guión
     * @param {string} rut - RUT a formatear
     * @returns {string} - RUT formateado (ej: 12.345.678-9)
     */
    static formatear(rut) {
        const { cuerpo, dv } = this.separar(rut);

        if (!cuerpo || !dv) {
            return rut;
        }

        // Agregar puntos cada 3 dígitos
        let cuerpoFormateado = '';
        let contador = 0;

        for (let i = cuerpo.length - 1; i >= 0; i--) {
            if (contador === 3) {
                cuerpoFormateado = '.' + cuerpoFormateado;
                contador = 0;
            }
            cuerpoFormateado = cuerpo.charAt(i) + cuerpoFormateado;
            contador++;
        }

        return `${cuerpoFormateado}-${dv}`;
    }

    /**
     * Valida y muestra mensaje de error en un input
     * @param {HTMLInputElement} input - Input del RUT
     * @param {HTMLElement} errorElement - Elemento para mostrar error (opcional)
     * @returns {boolean} - true si es válido
     */
    static validarInput(input, errorElement = null) {
        const rut = input.value;
        const esValido = this.validar(rut);

        // Agregar o quitar clases de Bootstrap
        if (esValido) {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
            if (errorElement) {
                errorElement.textContent = '';
                errorElement.style.display = 'none';
            }
        } else {
            input.classList.remove('is-valid');
            input.classList.add('is-invalid');
            if (errorElement) {
                errorElement.textContent = '❌ RUT inválido. Formato: 12345678-9';
                errorElement.style.display = 'block';
            }
        }

        return esValido;
    }

    /**
     * Auto-formatea el RUT mientras se escribe
     * @param {HTMLInputElement} input - Input del RUT
     */
    static autoFormatear(input) {
        input.addEventListener('input', function(e) {
            const cursorPos = this.selectionStart;
            const valorAnterior = this.value;
            
            // Formatear el RUT
            const rutFormateado = RutValidator.formatear(this.value);
            this.value = rutFormateado;

            // Ajustar posición del cursor
            if (rutFormateado.length > valorAnterior.length) {
                this.setSelectionRange(cursorPos + 1, cursorPos + 1);
            } else {
                this.setSelectionRange(cursorPos, cursorPos);
            }
        });
    }

    /**
     * Genera un RUT aleatorio válido (útil para testing)
     * @returns {string} - RUT válido aleatorio
     */
    static generarAleatorio() {
        const cuerpo = Math.floor(Math.random() * (99999999 - 1000000 + 1)) + 1000000;
        const dv = this.calcularDV(cuerpo.toString());
        return this.formatear(cuerpo.toString() + dv);
    }
}

/**
 * FUNCIONES DE INICIALIZACIÓN
 */

/**
 * Inicializa validación en todos los inputs de RUT de la página
 */
function inicializarValidacionRUT() {
    // Buscar todos los inputs con ID o name que contenga 'rut'
    const rutInputs = document.querySelectorAll('input[id*="rut"], input[name*="rut"], input[id*="Rut"], input[name*="Rut"]');

    rutInputs.forEach(input => {
        // Auto-formatear mientras escribe
        RutValidator.autoFormatear(input);

        // Buscar o crear elemento de error
        let errorElement = input.parentElement.querySelector('.invalid-feedback');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'invalid-feedback';
            input.parentElement.appendChild(errorElement);
        }

        // Validar al perder el foco
        input.addEventListener('blur', function() {
            RutValidator.validarInput(this, errorElement);
        });

        // Validar al enviar formulario
        const form = input.closest('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                if (!RutValidator.validarInput(input, errorElement)) {
                    e.preventDefault();
                    input.focus();
                    alert('❌ Por favor corrija el RUT antes de continuar.');
                    return false;
                }
            });
        }
    });

    console.log(`✅ Validación de RUT inicializada en ${rutInputs.length} campo(s)`);
}

/**
 * Separar RUT en dos campos (cuerpo y DV)
 * Útil para formularios que requieren campos separados
 */
function separarRUTenCampos(inputRut, inputCuerpo, inputDV) {
    inputRut.addEventListener('input', function() {
        const { cuerpo, dv } = RutValidator.separar(this.value);
        inputCuerpo.value = cuerpo;
        inputDV.value = dv;
    });
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inicializarValidacionRUT);
} else {
    inicializarValidacionRUT();
}

// Exportar para uso global
window.RutValidator = RutValidator;
window.inicializarValidacionRUT = inicializarValidacionRUT;
window.separarRUTenCampos = separarRUTenCampos;
