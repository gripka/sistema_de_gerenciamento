import logging

logger = logging.getLogger(__name__)

from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Modulo

@receiver(post_save, sender=Modulo)
def propagate_permissions(sender, instance, **kwargs):
    logger.info(f"Sinal recebido para post_save em Modulo: {instance.nome}")
    instance.propagate_permissions()

@receiver(m2m_changed, sender=Modulo.grupos.through)
def propagate_permissions_on_group_change(sender, instance, action, pk_set, **kwargs):
    if isinstance(instance, Modulo):
        if action == "post_add" and instance.pk:  # Certifique-se que o módulo existe
            logger.info(f"Sinal recebido para m2m_changed em Modulo: {instance.nome}, action: {action}")
            for grupo_id in pk_set:
                try:
                    grupo = Group.objects.get(pk=grupo_id)
                    grupo.permissions.add(*instance.permissions.all())
                    logger.info(f"Permissões propagadas para o grupo: {grupo.name}")
                except Group.DoesNotExist:
                    logger.error(f"Grupo com ID {grupo_id} não existe.")
        elif action in ["post_remove", "post_clear"] and instance.pk:  # Certifique-se que o módulo existe
            logger.info(f"Sinal recebido para m2m_changed em Modulo: {instance.nome}, action: {action}")
            for grupo_id in pk_set:
                try:
                    grupo = Group.objects.get(pk=grupo_id)
                    grupo.permissions.remove(*instance.permissions.all())
                    logger.info(f"Permissões removidas do grupo: {grupo.name}")
                except Group.DoesNotExist:
                    logger.error(f"Grupo com ID {grupo_id} não existe.")
    elif isinstance(instance, Group):
        if action == "post_add" and instance.pk:  # Certifique-se que o grupo existe
            logger.info(f"Sinal recebido para m2m_changed em Grupo: {instance.name}, action: {action}")
            for modulo_id in pk_set:
                try:
                    modulo = Modulo.objects.get(pk=modulo_id)
                    instance.permissions.add(*modulo.permissions.all())
                    logger.info(f"Permissões propagadas para o grupo: {instance.name} a partir do módulo: {modulo.nome}")
                except Modulo.DoesNotExist:
                    logger.error(f"Módulo com ID {modulo_id} não existe.")
        elif action in ["post_remove", "post_clear"] and instance.pk:  # Certifique-se que o grupo existe
            logger.info(f"Sinal recebido para m2m_changed em Grupo: {instance.name}, action: {action}")
            for modulo_id in pk_set:
                try:
                    modulo = Modulo.objects.get(pk=modulo_id)
                    instance.permissions.remove(*modulo.permissions.all())
                    logger.info(f"Permissões removidas do grupo: {instance.name} a partir do módulo: {modulo.nome}")
                except Modulo.DoesNotExist:
                    logger.error(f"Módulo com ID {modulo_id} não existe.")