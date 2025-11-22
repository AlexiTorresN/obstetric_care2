#!/usr/bin/env python
"""
Script para cerrar todas las sesiones activas del sistema
Uso: python cerrar_sesiones.py
"""
import os
import sys
import django
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'obstetric_care.settings')
django.setup()

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.utils import timezone

# Colores para terminal
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
CYAN = '\033[96m'
END = '\033[0m'
BOLD = '\033[1m'

def print_header():
    """Imprime el encabezado del script"""
    print("\n" + "="*70)
    print(f"{BOLD}{CYAN}🔐 CERRAR TODAS LAS SESIONES ACTIVAS{END}")
    print("="*70 + "\n")

def get_session_info():
    """Obtiene información sobre las sesiones activas"""
    now = timezone.now()
    
    # Todas las sesiones
    all_sessions = Session.objects.all()
    total_sessions = all_sessions.count()
    
    # Sesiones activas (no expiradas)
    active_sessions = all_sessions.filter(expire_date__gte=now)
    active_count = active_sessions.count()
    
    # Sesiones expiradas
    expired_sessions = all_sessions.filter(expire_date__lt=now)
    expired_count = expired_sessions.count()
    
    return {
        'total': total_sessions,
        'active': active_count,
        'expired': expired_count,
        'active_sessions': active_sessions,
        'expired_sessions': expired_sessions
    }

def show_active_sessions(active_sessions):
    """Muestra información de las sesiones activas"""
    if not active_sessions.exists():
        print(f"{YELLOW}ℹ️  No hay sesiones activas en este momento{END}\n")
        return
    
    print(f"{BOLD}📋 Sesiones Activas:{END}\n")
    
    for i, session in enumerate(active_sessions, 1):
        session_data = session.get_decoded()
        user_id = session_data.get('_auth_user_id')
        
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                username = user.username
                full_name = user.get_full_name() or "Sin nombre"
            except User.DoesNotExist:
                username = "Usuario eliminado"
                full_name = ""
        else:
            username = "Sesión anónima"
            full_name = ""
        
        expire_date = session.expire_date.strftime("%d/%m/%Y %H:%M:%S")
        
        print(f"  {i}. {BLUE}{username}{END}")
        if full_name:
            print(f"     Nombre: {full_name}")
        print(f"     Expira: {expire_date}")
        print(f"     Session Key: {session.session_key[:20]}...")
        print()

def confirm_action():
    """Solicita confirmación del usuario"""
    print(f"{YELLOW}⚠️  ADVERTENCIA:{END}")
    print("   Esta acción cerrará TODAS las sesiones activas del sistema.")
    print("   Los usuarios deberán volver a iniciar sesión.\n")
    
    response = input(f"{BOLD}¿Desea continuar? (si/no): {END}").strip().lower()
    return response in ['si', 's', 'yes', 'y', 'sí']

def close_all_sessions():
    """Cierra todas las sesiones activas"""
    print(f"\n{BLUE}🔄 Cerrando sesiones...{END}\n")
    
    # Obtener información antes de eliminar
    info = get_session_info()
    
    # Eliminar todas las sesiones
    deleted_count = Session.objects.all().delete()[0]
    
    print(f"{GREEN}✅ Sesiones cerradas exitosamente!{END}\n")
    print(f"   • Sesiones activas cerradas: {info['active']}")
    print(f"   • Sesiones expiradas eliminadas: {info['expired']}")
    print(f"   • Total de sesiones eliminadas: {deleted_count}")
    print()

def close_active_sessions_only():
    """Cierra solo las sesiones activas (no expiradas)"""
    print(f"\n{BLUE}🔄 Cerrando solo sesiones activas...{END}\n")
    
    now = timezone.now()
    active_sessions = Session.objects.filter(expire_date__gte=now)
    active_count = active_sessions.count()
    
    if active_count == 0:
        print(f"{YELLOW}ℹ️  No hay sesiones activas para cerrar{END}\n")
        return
    
    # Eliminar solo sesiones activas
    active_sessions.delete()
    
    print(f"{GREEN}✅ Sesiones activas cerradas exitosamente!{END}\n")
    print(f"   • Sesiones cerradas: {active_count}")
    print()

def clean_expired_sessions():
    """Elimina solo las sesiones expiradas"""
    print(f"\n{BLUE}🧹 Limpiando sesiones expiradas...{END}\n")
    
    now = timezone.now()
    expired_sessions = Session.objects.filter(expire_date__lt=now)
    expired_count = expired_sessions.count()
    
    if expired_count == 0:
        print(f"{YELLOW}ℹ️  No hay sesiones expiradas para limpiar{END}\n")
        return
    
    # Eliminar sesiones expiradas
    expired_sessions.delete()
    
    print(f"{GREEN}✅ Sesiones expiradas eliminadas!{END}\n")
    print(f"   • Sesiones eliminadas: {expired_count}")
    print()

def show_menu():
    """Muestra el menú de opciones"""
    print(f"{BOLD}Seleccione una opción:{END}\n")
    print("  1. Ver sesiones activas")
    print("  2. Cerrar TODAS las sesiones (activas + expiradas)")
    print("  3. Cerrar solo sesiones activas")
    print("  4. Limpiar solo sesiones expiradas")
    print("  5. Salir")
    print()

def main():
    """Función principal"""
    print_header()
    
    # Obtener información inicial
    info = get_session_info()
    
    print(f"{BOLD}📊 Estado Actual del Sistema:{END}\n")
    print(f"   • Total de sesiones: {info['total']}")
    print(f"   • Sesiones activas: {GREEN}{info['active']}{END}")
    print(f"   • Sesiones expiradas: {YELLOW}{info['expired']}{END}")
    print()
    
    while True:
        show_menu()
        
        try:
            option = input(f"{BOLD}Ingrese su opción (1-5): {END}").strip()
            
            if option == '1':
                # Ver sesiones activas
                print("\n" + "-"*70 + "\n")
                show_active_sessions(info['active_sessions'])
                input(f"{BOLD}Presione Enter para continuar...{END}")
                print("\n" + "="*70 + "\n")
                
            elif option == '2':
                # Cerrar todas las sesiones
                print("\n" + "-"*70 + "\n")
                show_active_sessions(info['active_sessions'])
                if confirm_action():
                    close_all_sessions()
                else:
                    print(f"\n{YELLOW}❌ Operación cancelada{END}\n")
                break
                
            elif option == '3':
                # Cerrar solo activas
                print("\n" + "-"*70 + "\n")
                show_active_sessions(info['active_sessions'])
                if confirm_action():
                    close_active_sessions_only()
                else:
                    print(f"\n{YELLOW}❌ Operación cancelada{END}\n")
                break
                
            elif option == '4':
                # Limpiar expiradas
                print("\n" + "-"*70 + "\n")
                clean_expired_sessions()
                break
                
            elif option == '5':
                # Salir
                print(f"\n{BLUE}👋 ¡Hasta pronto!{END}\n")
                break
                
            else:
                print(f"\n{RED}❌ Opción inválida. Por favor ingrese un número del 1 al 5{END}\n")
                
        except KeyboardInterrupt:
            print(f"\n\n{YELLOW}❌ Operación cancelada por el usuario{END}\n")
            break
        except Exception as e:
            print(f"\n{RED}❌ Error: {str(e)}{END}\n")
            break
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()