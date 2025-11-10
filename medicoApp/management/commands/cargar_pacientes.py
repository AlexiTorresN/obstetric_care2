# ============================================
# UBICACIÓN: medicoApp/management/commands/cargar_pacientes.py
# ============================================

from django.core.management.base import BaseCommand
from django.db import transaction
from gestionApp.models import Persona, Paciente
from datetime import date


class Command(BaseCommand):
    help = 'Carga pacientes de prueba (mujeres en edad fértil)'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                pacientes_creados = 0

                self.stdout.write(self.style.WARNING('\n📋 Cargando Pacientes...'))
                
                # Datos de pacientes (mujeres en edad fértil)
                pacientes_data = [
                    {
                        'rut': '18901234-9',
                        'nombre': 'Ana',
                        'apellido_paterno': 'Morales',
                        'apellido_materno': 'Díaz',
                        'sexo': 'Femenino',
                        'fecha_nacimiento': date(1995, 3, 15),
                        'telefono': '+56978901234',
                        'direccion': 'Av. Los Aromos 123, Concepción',
                        'email': 'ana.morales@email.cl',
                        'edad': 30,
                        'estado_civil': 'CASADA',
                        'prevision': 'FONASA_B',
                        'acompanante': 'Carlos Morales (Esposo)',
                        'contacto_emergencia': '+56987654321',
                    },
                    {
                        'rut': '19012345-6',
                        'nombre': 'Carolina',
                        'apellido_paterno': 'Fernández',
                        'apellido_materno': 'Soto',
                        'sexo': 'Femenino',
                        'fecha_nacimiento': date(1992, 7, 22),
                        'telefono': '+56989012345',
                        'direccion': 'Calle Los Robles 456, Talcahuano',
                        'email': 'carolina.fernandez@email.cl',
                        'edad': 33,
                        'estado_civil': 'SOLTERA',
                        'prevision': 'ISAPRE',
                        'acompanante': 'Rosa Soto (Madre)',
                        'contacto_emergencia': '+56976543210',
                    },
                    {
                        'rut': '20123456-5',
                        'nombre': 'Daniela',
                        'apellido_paterno': 'Castro',
                        'apellido_materno': 'Muñoz',
                        'sexo': 'Femenino',
                        'fecha_nacimiento': date(1998, 11, 8),
                        'telefono': '+56990123456',
                        'direccion': 'Pasaje Las Flores 789, Chiguayante',
                        'email': 'daniela.castro@email.cl',
                        'edad': 27,
                        'estado_civil': 'CASADA',
                        'prevision': 'FONASA_C',
                        'acompanante': 'Pedro Castro (Esposo)',
                        'contacto_emergencia': '+56965432109',
                    },
                    {
                        'rut': '21234567-9',
                        'nombre': 'Valentina',
                        'apellido_paterno': 'Herrera',
                        'apellido_materno': 'Pino',
                        'sexo': 'Femenino',
                        'fecha_nacimiento': date(1990, 5, 30),
                        'telefono': '+56991234567',
                        'direccion': 'Av. Colón 321, Concepción',
                        'email': 'valentina.herrera@email.cl',
                        'edad': 35,
                        'estado_civil': 'CONVIVIENTE',
                        'prevision': 'ISAPRE',
                        'acompanante': 'Miguel Pino (Pareja)',
                        'contacto_emergencia': '+56954321098',
                    },
                ]

                for data in pacientes_data:
                    # Verificar si ya existe la persona
                    if Persona.objects.filter(Rut=data['rut']).exists():
                        self.stdout.write(
                            self.style.WARNING(
                                f"  ⚠️  Paciente {data['nombre']} {data['apellido_paterno']} ya existe"
                            )
                        )
                        continue

                    # Crear Persona
                    persona = Persona.objects.create(
                        Rut=data['rut'],
                        Nombre=data['nombre'],
                        Apellido_Paterno=data['apellido_paterno'],
                        Apellido_Materno=data['apellido_materno'],
                        Sexo=data['sexo'],
                        Fecha_nacimiento=data['fecha_nacimiento'],
                        Telefono=data['telefono'],
                        Direccion=data['direccion'],
                        Email=data['email'],
                        Activo=True
                    )

                    # Crear Paciente vinculado a la persona
                    Paciente.objects.create(
                        persona=persona,
                        Edad=data['edad'],
                        Estado_civil=data['estado_civil'],
                        Previcion=data['prevision'],
                        Acompañante=data['acompanante'],
                        Contacto_emergencia=data['contacto_emergencia'],
                        activo=True
                    )

                    pacientes_creados += 1
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"  ✅ Paciente creada: {data['nombre']} {data['apellido_paterno']} "
                            f"({data['edad']} años)"
                        )
                    )

                # Resumen final
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✅ COMPLETADO: Se crearon {pacientes_creados} pacientes de prueba'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS('\n📌 Pacientes disponibles para pruebas:')
                )
                self.stdout.write('  🤰 4 Pacientes mujeres en edad fértil')
                self.stdout.write('  📊 Edades: 27, 30, 33 y 35 años')
                self.stdout.write('  💳 Previsión: 2 Fonasa, 2 Isapre')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error al cargar pacientes: {str(e)}')
            )
            raise