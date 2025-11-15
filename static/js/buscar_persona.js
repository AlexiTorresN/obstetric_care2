document.addEventListener('DOMContentLoaded', function() {
    const rutInput = document.querySelector('input[name="rut_persona"]');
    const personaInfoContainer = document.getElementById('persona-info');
    
    if (!rutInput || !personaInfoContainer) {
        console.warn('⚠️ Elementos de búsqueda de persona no encontrados');
        return;
    }
    
    let timeoutId = null;
    
    /**
     * Evento: Al perder el foco del campo RUT
     * Dispara búsqueda automática de la persona
     */
    rutInput.addEventListener('blur', function() {
        const rut = this.value.trim();
        
        if (!rut) {
            limpiarInfoPersona();
            return;
        }
        
        buscarPersona(rut);
    });
    
    /**
     * Evento: Al escribir en el campo RUT
     * Búsqueda con delay para evitar múltiples peticiones
     */
    rutInput.addEventListener('input', function() {
        clearTimeout(timeoutId);
        
        timeoutId = setTimeout(() => {
            const rut = this.value.trim();
            
            if (rut && rut.length >= 9) { // RUT completo mínimo: 1234567-8
                buscarPersona(rut);
            } else {
                limpiarInfoPersona();
            }
        }, 800); // 800ms de delay
    });
    
    /**
     * Función principal: Buscar persona por RUT via AJAX
     */
    function buscarPersona(rut) {
        // Mostrar loading
        mostrarLoading();
        
        // Petición AJAX
        fetch(`/gestion/api/persona/buscar/?rut=${encodeURIComponent(rut)}`, {
            method: 'GET',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la petición');
            }
            return response.json();
        })
        .then(data => {
            if (data.encontrado) {
                mostrarInfoPersona(data.persona);
            } else {
                mostrarPersonaNoEncontrada(data.mensaje);
            }
        })
        .catch(error => {
            console.error('❌ Error al buscar persona:', error);
            mostrarError('Error de conexión. Intente nuevamente.');
        });
    }
    
    /**
     * Mostrar indicador de carga
     */
    function mostrarLoading() {
        personaInfoContainer.innerHTML = `
            <div class="alert alert-info">
                <div class="spinner-border spinner-border-sm me-2" role="status">
                    <span class="visually-hidden">Buscando...</span>
                </div>
                Buscando persona...
            </div>
        `;
    }
    
    /**
     * Mostrar información de persona encontrada
     */
    function mostrarInfoPersona(persona) {
        personaInfoContainer.innerHTML = `
            <div class="alert alert-success">
                <h6 class="alert-heading">
                    <i class="bi bi-check-circle"></i> Persona Encontrada
                </h6>
                <hr>
                <div class="row">
                    <div class="col-md-6">
                        <p class="mb-1"><strong>RUT:</strong> ${persona.rut}</p>
                        <p class="mb-1"><strong>Nombre:</strong> ${persona.nombre_completo}</p>
                        <p class="mb-1"><strong>Sexo:</strong> ${persona.sexo}</p>
                    </div>
                    <div class="col-md-6">
                        <p class="mb-1"><strong>Fecha Nac:</strong> ${persona.fecha_nacimiento}</p>
                        <p class="mb-1"><strong>Teléfono:</strong> ${persona.telefono}</p>
                        <p class="mb-1"><strong>Email:</strong> ${persona.email}</p>
                    </div>
                </div>
            </div>
        `;
        
        console.log('✅ Persona encontrada:', persona);
    }
    
    /**
     * Mostrar mensaje de persona no encontrada
     */
    function mostrarPersonaNoEncontrada(mensaje) {
        personaInfoContainer.innerHTML = `
            <div class="alert alert-warning">
                <h6 class="alert-heading">
                    <i class="bi bi-exclamation-triangle"></i> Persona No Encontrada
                </h6>
                <p class="mb-2">${mensaje}</p>
                <hr>
                <p class="mb-0 small">
                    <i class="bi bi-info-circle"></i>
                    Debe <a href="/gestion/persona/registrar/" target="_blank" class="alert-link">
                        registrar la persona
                    </a> antes de asignar este rol.
                </p>
            </div>
        `;
        
        console.warn('⚠️ Persona no encontrada:', mensaje);
    }
    
    /**
     * Mostrar mensaje de error
     */
    function mostrarError(mensaje) {
        personaInfoContainer.innerHTML = `
            <div class="alert alert-danger">
                <i class="bi bi-x-circle"></i>
                <strong>Error:</strong> ${mensaje}
            </div>
        `;
    }
    
    /**
     * Limpiar información de persona
     */
    function limpiarInfoPersona() {
        personaInfoContainer.innerHTML = '';
    }
    
    /**
     * Validación básica de RUT (formato)
     */
    function validarFormatoRUT(rut) {
        // Formato: 12345678-9 o 12345678-K
        const rutRegex = /^\d{7,8}-[\dkK]$/;
        return rutRegex.test(rut);
    }
    
    // Validación al enviar formulario
    const form = rutInput.closest('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const rut = rutInput.value.trim();
            
            if (!rut) {
                e.preventDefault();
                alert('⚠️ Debe ingresar un RUT');
                rutInput.focus();
                return false;
            }
            
            if (!validarFormatoRUT(rut)) {
                e.preventDefault();
                alert('⚠️ El formato del RUT no es válido.\nFormato correcto: 12345678-9');
                rutInput.focus();
                return false;
            }
            
            // Si hay contenido de error, prevenir envío
            const alertDanger = personaInfoContainer.querySelector('.alert-danger');
            const alertWarning = personaInfoContainer.querySelector('.alert-warning');
            
            if (alertDanger || alertWarning) {
                e.preventDefault();
                alert('⚠️ Debe buscar y seleccionar una persona válida antes de continuar');
                rutInput.focus();
                return false;
            }
        });
    }
    
    console.log('✅ Sistema de búsqueda de persona cargado correctamente');
});
