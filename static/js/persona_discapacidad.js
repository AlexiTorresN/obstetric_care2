document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos
    const discapacidadSelect = document.getElementById('id_discapacidad');
    const tipoDiscapacidadContainer = document.getElementById('tipo_discapacidad_container');
    const tipoDiscapacidadInput = document.getElementById('id_tipo_discapacidad');
    
    // Verificar que existen los elementos
    if (!discapacidadSelect || !tipoDiscapacidadContainer) {
        return; // Si no existen, salir
    }
    
    // Función para mostrar/ocultar
    function toggleTipoDiscapacidad() {
        if (discapacidadSelect.value === 'Si') {
            // Mostrar el campo
            tipoDiscapacidadContainer.style.display = 'block';
            tipoDiscapacidadInput.required = true;
        } else {
            // Ocultar el campo
            tipoDiscapacidadContainer.style.display = 'none';
            tipoDiscapacidadInput.required = false;
            tipoDiscapacidadInput.value = ''; // Limpiar valor
        }
    }
    
    // Ejecutar al cargar la página
    toggleTipoDiscapacidad();
    
    // Ejecutar cuando cambie el select
    discapacidadSelect.addEventListener('change', toggleTipoDiscapacidad);
});
