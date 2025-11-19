# core/management/commands/setup_roles.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = "Crea los roles del sistema y asigna permisos base"

    def handle(self, *args, **kwargs):
        roles = ["Administrador", "Médico", "Matrona", "TENS"]

        for r in roles:
            group, created = Group.objects.get_or_create(name=r)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Rol creado: {r}"))

        # Administrador tiene todos los permisos
        admin = Group.objects.get(name="Administrador")
        admin.permissions.set(Permission.objects.all())

        self.stdout.write(self.style.SUCCESS("Todos los roles han sido configurados."))
