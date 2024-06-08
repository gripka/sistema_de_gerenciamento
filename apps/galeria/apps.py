from django.apps import AppConfig


class GaleriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.galeria'

    def ready(self):
        import apps.galeria.signals  # Certifique-se que esta linha existe
