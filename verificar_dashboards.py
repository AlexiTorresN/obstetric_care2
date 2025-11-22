#!/usr/bin/env python
"""
Script de verificación rápida para Splash Screen y Dashboards
Ejecutar: python verificar_dashboards.py
"""
import os
import sys
from pathlib import Path

# Colores para terminal
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
END = '\033[0m'

def print_status(message, status='info'):
    """Imprime mensaje con color"""
    if status == 'success':
        print(f"{GREEN}✅ {message}{END}")
    elif status == 'warning':
        print(f"{YELLOW}⚠️  {message}{END}")
    elif status == 'error':
        print(f"{RED}❌ {message}{END}")
    else:
        print(f"{BLUE}ℹ️  {message}{END}")

def check_file(filepath, required=True):
    """Verifica si un archivo existe"""
    exists = Path(filepath).exists()
    if exists:
        print_status(f"{filepath}", 'success')
    else:
        status = 'error' if required else 'warning'
        print_status(f"{filepath} - NO ENCONTRADO", status)
    return exists

def check_content_in_file(filepath, search_strings, description):
    """Verifica contenido en un archivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for search_str in search_strings:
                if search_str not in content:
                    print_status(f"{description} - Falta: {search_str}", 'error')
                    return False
            print_status(f"{description}", 'success')
            return True
    except FileNotFoundError:
        print_status(f"{filepath} no encontrado", 'error')
        return False

def main():
    print("\n" + "="*70)
    print("🔍 VERIFICACIÓN DE SPLASH SCREEN Y DASHBOARDS")
    print("="*70 + "\n")

    issues = []
    
    # ============================================
    # PASO 1: Verificar Templates
    # ============================================
    print("\n📄 PASO 1: Verificando templates...\n")
    
    templates = {
        'templates/base.html': True,
        'templates/inicio/home.html': True,
        'templates/authentication/dashboards/dashboard_admin.html': True,
        'templates/authentication/dashboards/dashboard_medico.html': True,
        'templates/authentication/dashboards/dashboard_matrona.html': True,
        'templates/authentication/dashboards/dashboard_tens.html': True,
    }
    
    for template, required in templates.items():
        if not check_file(template, required):
            issues.append(f"Falta template: {template}")
    
    # ============================================
    # PASO 2: Verificar Vistas
    # ============================================
    print("\n👁️  PASO 2: Verificando vistas...\n")
    
    views_checks = [
        ('authentication/views.py', 
         ['DashboardAdminView', 'DashboardMedicoView', 'DashboardMatronaView', 'DashboardTensView'],
         'Vistas de dashboards en authentication/views.py'),
        ('inicioApp/views.py',
         ['def home(request):', 'if request.user.is_authenticated:'],
         'Vista home con redirección en inicioApp/views.py'),
    ]
    
    for filepath, search_strs, desc in views_checks:
        if not check_content_in_file(filepath, search_strs, desc):
            issues.append(f"Falta configuración en: {filepath}")
    
    # ============================================
    # PASO 3: Verificar URLs
    # ============================================
    print("\n🔗 PASO 3: Verificando URLs...\n")
    
    url_checks = [
        ('authentication/urls.py',
         ["path('dashboard/admin/'", "path('dashboard/medico/'", 
          "path('dashboard/matrona/'", "path('dashboard/tens/'"],
         'Rutas de dashboards en authentication/urls.py'),
        ('obstetric_care/urls.py',
         ["include('authentication.urls')", "inicio_views.home"],
         'Configuración principal de URLs'),
    ]
    
    for filepath, search_strs, desc in url_checks:
        if not check_content_in_file(filepath, search_strs, desc):
            issues.append(f"Falta configuración en URLs: {filepath}")
    
    # ============================================
    # PASO 4: Verificar Settings
    # ============================================
    print("\n⚙️  PASO 4: Verificando settings.py...\n")
    
    settings_checks = [
        ('obstetric_care/settings.py',
         ["'authentication'", "'inicioApp'", "BASE_DIR / 'templates'"],
         'Configuración en settings.py'),
    ]
    
    for filepath, search_strs, desc in settings_checks:
        if not check_content_in_file(filepath, search_strs, desc):
            issues.append(f"Falta configuración en settings")
    
    # ============================================
    # PASO 5: Verificar estructura de directorios
    # ============================================
    print("\n📁 PASO 5: Verificando estructura de directorios...\n")
    
    directories = [
        'templates',
        'templates/inicio',
        'templates/authentication',
        'templates/authentication/dashboards',
    ]
    
    for directory in directories:
        if Path(directory).is_dir():
            print_status(f"Directorio: {directory}", 'success')
        else:
            print_status(f"Directorio: {directory} - NO EXISTE", 'error')
            issues.append(f"Falta directorio: {directory}")
    
    # ============================================
    # RESUMEN FINAL
    # ============================================
    print("\n" + "="*70)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*70 + "\n")
    
    if not issues:
        print_status("¡VERIFICACIÓN EXITOSA! ✨", 'success')
        print_status("Todos los archivos y configuraciones están correctos", 'success')
        print("\n" + BLUE + "Próximos pasos:" + END)
        print("  1. python manage.py runserver")
        print("  2. Visita: http://127.0.0.1:8000/")
        print("  3. Haz clic en 'Iniciar Sesión'")
        print("  4. Inicia sesión con tus credenciales")
        print("  5. Serás redirigido a tu dashboard según tu rol")
    else:
        print_status(f"Se encontraron {len(issues)} problema(s):", 'error')
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print("\n" + YELLOW + "⚠️  Revisa la guía de implementación y corrige los problemas" + END)
        sys.exit(1)
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()