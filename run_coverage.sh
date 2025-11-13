#!/bin/bash
# run_coverage.sh

echo "🧪 Ejecutando tests con coverage..."

# Limpiar reportes anteriores
rm -f coverage.xml
rm -rf htmlcov/

# Ejecutar tests con coverage
echo "📊 Generando reporte de coverage..."
coverage run --source='.' manage.py test
coverage xml
coverage html
coverage report

# Mostrar resumen
echo "✅ Coverage generado!"
echo "📁 Reporte XML: coverage.xml"
echo "🌐 Reporte HTML: htmlcov/index.html"
echo ""

# Mostrar estadísticas
coverage report | tail -1

# Ejecutar análisis de SonarCloud local (opcional)
if command -v sonar-scanner &> /dev/null; then
    echo "🔍 Ejecutando SonarCloud Scanner..."
    sonar-scanner
else
    echo "⚠️  SonarCloud Scanner no instalado"
fi