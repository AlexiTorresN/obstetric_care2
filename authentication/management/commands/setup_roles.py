# authentication/management/commands/setup_roles.py
"""
Comando Django para configurar grupos y roles del sistema
Uso: python manage.py setup_roles
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Crea los grupos/roles del sistema y asigna permisos básicos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('\n🔧 Iniciando configuración de roles...\n'))

        # Definir roles del sistema
        roles_config = {
            'Administrador': {
                'descripcion': 'Acceso total al sistema',
                'permisos': 'all'
            },
            'Médico': {
                'descripcion': 'Gestión de patologías y consultas médicas',
                'permisos': ['view', 'add', 'change']
            },
            'Matrona': {
                'descripcion': 'Gestión de fichas obstétricas e ingresos',
                'permisos': ['view', 'add', 'change']
            },
            'TENS': {
                'descripcion': 'Administración de medicamentos y tratamientos',
                'permisos': ['view', 'add']
            },
        }

        for role_name, config in roles_config.items():
            group, created = Group.objects.get_or_create(name=role_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Rol creado: {role_name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Rol ya existe: {role_name}')
                )
            
            # Asignar permisos
            if config['permisos'] == 'all':
                # Administrador tiene todos los permisos
                group.permissions.set(Permission.objects.all())
                self.stdout.write(
                    self.style.SUCCESS(
                        f'   → Asignados todos los permisos a {role_name}'
                    )
                )
            else:
                # Asignar permisos específicos según el rol
                self._assign_role_permissions(group, config['permisos'])

        self.stdout.write(
            self.style.SUCCESS('\n✅ Configuración de roles completada exitosamente!\n')
        )
        
        # Mostrar resumen
        self._print_summary()

    def _assign_role_permissions(self, group, permission_types):
        """
        Asigna permisos específicos a un grupo
        """
        relevant_models = [
            'persona', 'paciente', 'medico', 'matrona', 'tens',
            'fichaobstetrica', 'ingresopaciente', 'registroparto',
            'patologias', 'medicamentoficha', 'administracionmedicamento',
            'registrotens', 'tratamiento_aplicado'
        ]
        
        permissions = Permission.objects.filter(
            codename__startswith=tuple(f'{pt}_' for pt in permission_types),
            content_type__model__in=relevant_models
        )
        
        group.permissions.set(permissions)
        self.stdout.write(
            self.style.SUCCESS(
                f'   → Asignados {permissions.count()} permisos a {group.name}'
            )
        )

    def _print_summary(self):
        """
        Muestra un resumen de los grupos creados
        """
        self.stdout.write(self.style.WARNING('📊 Resumen de grupos:'))
        for group in Group.objects.all():
            user_count = group.user_set.count()
            perm_count = group.permissions.count()
            self.stdout.write(
                f'   • {group.name}: {user_count} usuarios, {perm_count} permisos'
            )