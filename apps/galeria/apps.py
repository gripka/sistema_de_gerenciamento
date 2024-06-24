from django.apps import AppConfig

class GaleriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.galeria'

    def ready(self):
        import apps.galeria.signals
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        from .models import Modulo

        content_type = ContentType.objects.get_for_model(Modulo)
        Permission.objects.get_or_create(
            codename='view_relatorios',
            name='Can view relatorios',
            content_type=content_type,
        )