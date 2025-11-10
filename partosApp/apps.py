from django.apps import AppConfig


class PartosappConfig(AppConfig):
    """
    Configuración de la aplicación partosApp
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'partosApp'
    verbose_name = 'Módulo de Partos'
    
    def ready(self):
        """
        Método que se ejecuta cuando la aplicación está lista
        Aquí se pueden importar signals si es necesario
        """
        pass