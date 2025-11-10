# ============================================
# UBICACIÓN: medicoApp/management/commands/cargar_usuarios.py
# ============================================

from django.core.management.base import BaseCommand
from django.db import transaction
from gestionApp.models import Persona, Medico, Matrona, Tens
from datetime import date


class Command(BaseCommand):
    help = 'Carga usuarios de prueba: 2 médicos, 2 matronas y 2 TENS'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                usuarios_creados = 0

                # ============================================
                # MÉDICOS
                # ============================================
                self.stdout.write(self.style.WARNING('\n📋 Cargando Médicos...'))
                
                medicos_data = [
                    {
                        'rut': '12345678-5',
                        'nombre': 'Juan',
                        'apellido_paterno': 'Pérez',
                        'apellido_materno': 'González',
                        'sexo': 'Masculino',
                        'fecha_nacimiento': date(1975, 5, 15),
                        'telefono': '+56912345678',
                        'email': 'juan.perez@hospital.cl',
                        'especialidad': 'Obstetricia General',
                        'registro_medico': 'MED-2000-001',
                        'anos_experiencia': 25,
                        'turno': 'Mañana',
                    },
                    {
                        'rut': '13456789-9',
                        'nombre': 'María',
                        'apellido_paterno': 'Silva',
                        'apellido_materno': 'Morales',
                        'sexo': 'Femenino',
                        'fecha_nacimiento': date(1980, 8, 20),
                        'telefono': '+56923456789',
                        'email': 'maria.silva@hospital.cl',
                        'especialidad': 'Ginecología',
                        'registro_medico': 'MED-2005-042',
                        'anos_experiencia': 20,
                        'turno': 'Tarde',
                    }
                ]

                for data in medicos_data:
                    if Persona.objects.filter(Rut=data['rut']).exists():
                        self.stdout.write(
                            self.style.WARNING(f"  ⚠️  Médico {data['nombre']} {data['apellido_paterno']} ya existe")
                        )
                        continue

                    persona = Persona.objects.create(
                        Rut=data['rut'],
                        Nombre=data['nombre'],
                        Apellido_Paterno=data['apellido_paterno'],
                        Apellido_Materno=data['apellido_materno'],
                        Sexo=data['sexo'],
                        Fecha_nacimiento=data['fecha_nacimiento'],
                        Telefono=data['telefono'],
                        Email=data['email'],
                        Activo=True
                    )

                    Medico.objects.create(
                        persona=persona,
                        Especialidad=data['especialidad'],
                        Registro_medico=data['registro_medico'],
                        Años_experiencia=data['anos_experiencia'],
                        Turno=data['turno'],
                        Activo=True
                    )

                    usuarios_creados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✅ Médico creado: Dr. {data['nombre']} {data['apellido_paterno']}")
                    )

                # ============================================
                # MATRONAS
                # ============================================
                self.stdout.write(self.style.WARNING('\n📋 Cargando Matronas...'))
                
                matronas_data = [
                    {
                        'rut': '14567890-0',
                        'nombre': 'Carla',
                        'apellido_paterno': 'Ramírez',
                        'apellido_materno': 'López',
                        'sexo': 'Femenino',
                        'fecha_nacimiento': date(1985, 3, 10),
                        'telefono': '+56934567890',
                        'email': 'carla.ramirez@hospital.cl',
                        'especialidad': 'Control Prenatal',
                        'registro_medico': 'MAT-2015-001',
                        'anos_experiencia': 10,
                        'turno': 'Mañana',
                    },
                    {
                        'rut': '15678901-1',
                        'nombre': 'Patricia',
                        'apellido_paterno': 'Torres',
                        'apellido_materno': 'Vega',
                        'sexo': 'Femenino',
                        'fecha_nacimiento': date(1990, 11, 25),
                        'telefono': '+56945678901',
                        'email': 'patricia.torres@hospital.cl',
                        'especialidad': 'Atención del Parto',
                        'registro_medico': 'MAT-2018-045',
                        'anos_experiencia': 7,
                        'turno': 'Tarde',
                    }
                ]

                for data in matronas_data:
                    if Persona.objects.filter(Rut=data['rut']).exists():
                        self.stdout.write(
                            self.style.WARNING(f"  ⚠️  Matrona {data['nombre']} {data['apellido_paterno']} ya existe")
                        )
                        continue

                    persona = Persona.objects.create(
                        Rut=data['rut'],
                        Nombre=data['nombre'],
                        Apellido_Paterno=data['apellido_paterno'],
                        Apellido_Materno=data['apellido_materno'],
                        Sexo=data['sexo'],
                        Fecha_nacimiento=data['fecha_nacimiento'],
                        Telefono=data['telefono'],
                        Email=data['email'],
                        Activo=True
                    )

                    Matrona.objects.create(
                        persona=persona,
                        Especialidad=data['especialidad'],
                        Registro_medico=data['registro_medico'],
                        Años_experiencia=data['anos_experiencia'],
                        Turno=data['turno'],
                        Activo=True
                    )

                    usuarios_creados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✅ Matrona creada: {data['nombre']} {data['apellido_paterno']}")
                    )

                # ============================================
                # TENS
                # ============================================
                self.stdout.write(self.style.WARNING('\n📋 Cargando TENS...'))
                
                tens_data = [
                    {
                        'rut': '16789012-1',
                        'nombre': 'Luis',
                        'apellido_paterno': 'Martínez',
                        'apellido_materno': 'Castro',
                        'sexo': 'Masculino',
                        'fecha_nacimiento': date(1992, 7, 18),
                        'telefono': '+56956789012',
                        'email': 'luis.martinez@hospital.cl',
                        'nivel': 'Preparto',
                        'anos_experiencia': 5,
                        'turno': 'Mañana',
                        'certificaciones': 'SVB',
                    },
                    {
                        'rut': '17890123-0',
                        'nombre': 'Andrea',
                        'apellido_paterno': 'González',
                        'apellido_materno': 'Rojas',
                        'sexo': 'Femenino',
                        'fecha_nacimiento': date(1995, 2, 14),
                        'telefono': '+56967890123',
                        'email': 'andrea.gonzalez@hospital.cl',
                        'nivel': 'Parto',
                        'anos_experiencia': 3,
                        'turno': 'Tarde',
                        'certificaciones': 'Parto Normal',
                    }
                ]

                for data in tens_data:
                    if Persona.objects.filter(Rut=data['rut']).exists():
                        self.stdout.write(
                            self.style.WARNING(f"  ⚠️  TENS {data['nombre']} {data['apellido_paterno']} ya existe")
                        )
                        continue

                    persona = Persona.objects.create(
                        Rut=data['rut'],
                        Nombre=data['nombre'],
                        Apellido_Paterno=data['apellido_paterno'],
                        Apellido_Materno=data['apellido_materno'],
                        Sexo=data['sexo'],
                        Fecha_nacimiento=data['fecha_nacimiento'],
                        Telefono=data['telefono'],
                        Email=data['email'],
                        Activo=True
                    )

                    Tens.objects.create(
                        persona=persona,
                        Nivel=data['nivel'],
                        Años_experiencia=data['anos_experiencia'],
                        Turno=data['turno'],
                        Certificaciones=data['certificaciones'],
                        Activo=True
                    )

                    usuarios_creados += 1
                    self.stdout.write(
                        self.style.SUCCESS(f"  ✅ TENS creado: {data['nombre']} {data['apellido_paterno']}")
                    )

                # ============================================
                # RESUMEN FINAL
                # ============================================
                self.stdout.write(
                    self.style.SUCCESS(
                        f'\n✅ COMPLETADO: Se crearon {usuarios_creados} usuarios de prueba'
                    )
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        '\n📌 Usuarios disponibles para pruebas:'
                    )
                )
                self.stdout.write('  🩺 2 Médicos')
                self.stdout.write('  👶 2 Matronas')
                self.stdout.write('  💉 2 TENS')

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n❌ Error al cargar usuarios: {str(e)}')
            )
            raise