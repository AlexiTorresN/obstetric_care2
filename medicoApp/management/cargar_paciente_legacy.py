# ============================================
# UBICACIÓN: medicoApp/management/commands/cargar_paciente_legacy.py
# Crea una paciente que tiene controles previos en la base de datos LEGACY
# ============================================

from django.core.management.base import BaseCommand
from django.db import transaction
from gestionApp.models import Persona, Paciente
from datetime import date


class Command(BaseCommand):
    help = 'Carga paciente con historial en base de datos LEGACY (RUT: 16293109-1)'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # RUT que tiene controles previos en la BD legacy
                rut = '16293109-1'
                
                self.stdout.write(self.style.WARNING('\n📋 Cargando Paciente con Historial LEGACY...'))
                
                # Verificar si ya existe
                if Persona.objects.filter(Rut=rut).exists():
                    self.stdout.write(
                        self.style.WARNING(f"  ⚠️  La paciente con RUT {rut} ya existe")
                    )
                    return
                
                # Datos de la paciente
                paciente_data = {
                    'rut': '16293109-1',
                    'nombre': 'Isabel',
                    'apellido_paterno': 'Sandoval',
                    'apellido_materno': 'Flores',
                    'sexo': 'Femenino',
                    'fecha_nacimiento': date(1993, 12, 10),  # 31 años
                    'telefono': '+56992345678',
                    'direccion': 'Calle Los Pinos 890, Coronel',
                    'email': 'isabel.sandoval@email.cl',
                    'edad': 31,
                    'estado_civil': 'CASADA',
                    'prevision': 'FONASA_D',
                    'acompanante': 'Roberto Sandoval (Esposo)',
                    'contacto_emergencia': '+56943210987',
                }
                
                # Crear Persona
                persona = Persona.objects.create(
                    Rut=paciente_data['rut'],
                    Nombre=paciente_data['nombre'],
                    Apellido_Paterno=paciente_data['apellido_paterno'],
                    Apellido_Materno=paciente_data['apellido_materno'],
                    Sexo=paciente_data['sexo'],
                    Fecha_nacimiento=paciente_data['fecha_nacimiento'],
                    Telefono=paciente_data['telefono'],
                    Direccion=paciente_data['direccion'],
                    Email=paciente_data['email'],
                    Activo=True
                )
                
                # Crear Paciente vinculado a la persona
                Paciente.objects.create(
                    persona=persona,
                    Edad=paciente_data['edad'],
                    Estado_civil=paciente_data['estado_civil'],
                    Previcion=paciente_data['prevision'],
                    Acompañante=paciente_data['acompanante'],
                    Contacto_emergencia=paciente_data['contacto_emergencia'],
                    activo=True
                )
                
                # Resumen
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✅ Paciente creada exitosamente'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  👤 Nombre: {paciente_data["nombre"]} {paciente_data["apellido_paterno"]} {paciente_data["apellido_materno"]}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  🆔 RUT: {paciente_data["rut"]}'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  📅 Edad: {paciente_data["edad"]} años'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        '\n📊 HISTORIAL LEGACY DISPONIBLE:'
                    )
                )
                self.stdout.write('  ✓ Esta paciente tiene 5 controles previos en la base de datos LEGACY')
                self.stdout.write('  ✓ Controles desde: 2021-09-10 hasta 2025-05-14')
                self.stdout.write('  ✓ Los controles se mostrarán automáticamente en el sistema')
                
                self.stdout.write(
                    self.style.WARNING(
                        '\n💡 INSTRUCCIONES:'
                    )
                )
                self.stdout.write('  1. Busca la paciente por RUT: 16293109-1')
                self.stdout.write('  2. En el detalle de la paciente verás la sección "Controles de Rutina Previos (LEGACY)"')
                self.stdout.write('  3. Allí aparecerán los 5 controles históricos automáticamente')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error al cargar paciente con historial legacy: {str(e)}')
            )
            raise