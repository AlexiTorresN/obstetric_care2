#!/usr/bin/env python
"""
Script de validación para verificar la consolidación de autenticación
Uso: python validation_script.py
"""
import os
import sys
from pathlib import Path

# Colores para terminal
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_status(message, status='info'):
    """Imprime mensaje con color según el estado"""
    if status == 'success':
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
    elif status == 'warning':
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
    elif status == 'error':
        print(f"{Colors.RED}❌ {message}{Colors.END}")
    else:
        print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def check_file_exists(filepath, required=True):
    """Verifica si un archivo existe"""
    exists = Path(filepath).exists()
    if exists:
        print_status(f"Archivo encontrado: {filepath}", 'success')
    else:
        if required:
            print_status(f"Archivo REQUERIDO no encontrado: {filepath}", 'error')
        else:
            print_status(f"Archivo opcional no encontrado: {filepath}", 'warning')
    return exists

def check_directory_exists(dirpath):
    """Verifica si un directorio existe"""
    exists = Path(dirpath).is_dir()
    if exists:
        print_status(f"Directorio encontrado: {dirpath}", 'success')
    else:
        print_status(f"Directorio NO encontrado: {dirpath}", 'error')
    return exists

def check_string_in_file(filepath, search_string, description):
    """Verifica si una cadena existe en un archivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if search_string in content:
                print_status(f"{description} - Configurado correctamente", 'success')
                return True
            else:
                print_status(f"{description} - NO configurado", 'error')
                return False
    except FileNotFoundError:
        print_status(f"Archivo no encontrado: {filepath}", 'error')
        return False

def main():
    """Función principal de validación"""
    print("\n" + "="*60)
    print("🔍 VALIDACIÓN DE CONSOLIDACIÓN DE AUTENTICACIÓN")
    print("="*60 + "\n")

    issues = []
    
    # ============================================
    # PASO 1: Verificar estructura de directorios
    # ============================================
    print("\n📁 PASO 1: Verificando estructura de directorios...\n")
    
    dirs_to_check = [
        "authentication",
        "authentication/middleware",
        "authentication/management",
        "authentication/management/commands",
    ]
    
    for dir_path in dirs_to_check:
        if not check_directory_exists(dir_path):
            issues.append(f"Falta directorio: {dir_path}")
    
    # ============================================
    # PASO 2: Verificar archivos requeridos
    # ============================================
    print("\n📄 PASO 2: Verificando archivos requeridos...\n")
    
    required_files = [
        "authentication/__init__.py",
        "authentication/apps.py",
        "authentication/views.py",
        "authentication/forms.py",
        "authentication/urls.py",
        "authentication/middleware/__init__.py",
        "authentication/middleware/role_gatekeeper.py",
        "authentication/management/__init__.py",
        "authentication/management/commands/__init__.py",
        "authentication/management/commands/setup_roles.py",
    ]
    
    for file_path in required_files:
        if not check_file_exists(file_path, required=True):
            issues.append(f"Falta archivo requerido: {file_path}")
    
    # ============================================
    # PASO 3: Verificar configuración en settings.py
    # ============================================
    print("\n⚙️  PASO 3: Verificando configuración en settings.py...\n")
    
    settings_checks = [
        ("obstetric_care/settings.py", "'authentication'", 
         "authentication en INSTALLED_APPS"),
        ("obstetric_care/settings.py", 
         "authentication.middleware.role_gatekeeper.RoleGatekeeperMiddleware",
         "RoleGatekeeperMiddleware en MIDDLEWARE"),
    ]
    
    for filepath, search_str, desc in settings_checks:
        if not check_string_in_file(filepath, search_str, desc):
            issues.append(f"Configuración faltante: {desc}")
    
    # ============================================
    # PASO 4: Verificar configuración de URLs
    # ============================================
    print("\n🔗 PASO 4: Verificando configuración de URLs...\n")
    
    url_checks = [
        ("obstetric_care/urls.py", 
         "include('authentication.urls')",
         "authentication.urls incluido en urls principales"),
        ("authentication/urls.py", 
         "app_name = 'authentication'",
         "app_name definido en authentication/urls.py"),
    ]
    
    for filepath, search_str, desc in url_checks:
        if not check_string_in_file(filepath, search_str, desc):
            issues.append(f"Configuración de URL faltante: {desc}")
    
    # ============================================
    # PASO 5: Verificar que core/views.py está limpio
    # ============================================
    print("\n🧹 PASO 5: Verificando limpieza de core/views.py...\n")
    
    try:
        with open("core/views.py", 'r', encoding='utf-8') as f:
            content = f.read()
            if "def login_view(" in content and "def login_view(" not in content.split('#')[0]:
                print_status("login_view está comentado correctamente en core/views.py", 'success')
            elif "def login_view(" not in content:
                print_status("login_view removido de core/views.py", 'success')
            else:
                print_status("login_view todavía activo en core/views.py", 'warning')
                issues.append("login_view debe ser comentado/removido de core/views.py")
    except FileNotFoundError:
        print_status("core/views.py no encontrado", 'warning')
    
    # ============================================
    # RESUMEN FINAL
    # ============================================
    print("\n" + "="*60)
    print("📊 RESUMEN DE VALIDACIÓN")
    print("="*60 + "\n")
    
    if not issues:
        print_status("¡VALIDACIÓN EXITOSA! ✨", 'success')
        print_status("Todos los archivos y configuraciones están correctos", 'success')
        print_status("\nPróximos pasos:", 'info')
        print("  1. python manage.py makemigrations")
        print("  2. python manage.py migrate")
        print("  3. python manage.py setup_roles")
        print("  4. python manage.py runserver")
    else:
        print_status(f"Se encontraron {len(issues)} problema(s):", 'error')
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        print_status("\n⚠️  Por favor, revisa la guía de implementación y corrige los problemas", 'warning')
        sys.exit(1)
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    main()