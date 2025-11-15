document.addEventListener('DOMContentLoaded', function() {
    const pesoInput = document.getElementById('id_peso');
    const tallaInput = document.getElementById('id_talla');
    const imcInput = document.getElementById('id_imc');
    const imcDisplay = document.getElementById('imc_display');
    
    if (!pesoInput || !tallaInput || !imcInput) {
        return; // Si no existen los campos, salir
    }
    
    function calcularIMC() {
        const peso = parseFloat(pesoInput.value);
        const talla = parseFloat(tallaInput.value);
        
        if (peso && talla && talla > 0) {
            // Convertir talla de cm a metros
            const tallaMetros = talla / 100;
            
            // Calcular IMC: peso / talla²
            const imc = (peso / (tallaMetros * tallaMetros)).toFixed(2);
            
            // Asignar al campo
            imcInput.value = imc;
            
            // Mostrar clasificación si existe el elemento display
            if (imcDisplay) {
                let clasificacion = '';
                let color = '';
                
                if (imc < 18.5) {
                    clasificacion = 'Bajo peso';
                    color = 'text-warning';
                } else if (imc >= 18.5 && imc < 25) {
                    clasificacion = 'Peso normal';
                    color = 'text-success';
                } else if (imc >= 25 && imc < 30) {
                    clasificacion = 'Sobrepeso';
                    color = 'text-warning';
                } else {
                    clasificacion = 'Obesidad';
                    color = 'text-danger';
                }
                
                imcDisplay.innerHTML = `<span class="${color}">IMC: ${imc} - ${clasificacion}</span>`;
            }
            
            // Validar rango 10-60
            if (imc < 10 || imc > 60) {
                imcInput.setCustomValidity('El IMC debe estar entre 10 y 60');
                if (imcDisplay) {
                    imcDisplay.innerHTML = '<span class="text-danger">⚠️ IMC fuera de rango válido (10-60)</span>';
                }
            } else {
                imcInput.setCustomValidity('');
            }
        } else {
            imcInput.value = '';
            if (imcDisplay) {
                imcDisplay.innerHTML = '';
            }
        }
    }
    
    // Calcular cuando cambien peso o talla
    pesoInput.addEventListener('input', calcularIMC);
    tallaInput.addEventListener('input', calcularIMC);
    
    // Calcular al cargar si ya hay valores
    calcularIMC();

});