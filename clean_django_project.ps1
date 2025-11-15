Write-Host "🧹 Limpiando proyecto Django..."

# Eliminar __pycache__ y archivos .pyc
Get-ChildItem -Recurse -Force -Include "__pycache__" | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
Get-ChildItem -Recurse -Force -Include "*.pyc" | Remove-Item -Force -ErrorAction SilentlyContinue

# Eliminar migraciones (excepto __init__.py)
Get-ChildItem -Recurse -Directory -Filter "migrations" | ForEach-Object {
    Get-ChildItem $_.FullName -Exclude "__init__.py" | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
}

# Eliminar cachés y logs
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue ".pytest_cache", ".cache", "*.log"

# Eliminar base de datos SQLite si existe
if (Test-Path "db.sqlite3") {
    Remove-Item -Force "db.sqlite3"
}

Write-Host "✅ Limpieza completada correctamente."