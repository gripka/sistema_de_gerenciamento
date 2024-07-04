import logging

from django.db.models.signals import m2m_changed, post_delete, post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import Group, User

from .models import Modulo

logger = logging.getLogger(__name__)


def update_user_permissions(user):
    user.user_permissions.clear()
    for group in user.groups.all():
        user.user_permissions.add(*group.permissions.all())


def update_group_permissions(group):
    """Atualiza as permissões de um grupo com base nos módulos relacionados."""
    group.permissions.clear()
    for modulo in group.modulos.all():
        group.permissions.add(*modulo.permissions.all())


@receiver(m2m_changed, sender=Modulo.grupos.through)
def propagate_permissions_on_group_change(sender, instance, action, pk_set, **kwargs):
    logger.info(f"Sinal recebido para m2m_changed em: {instance}, action: {action}")

    if action in ["post_add", "post_remove", "post_clear"]:
        if isinstance(instance, Modulo):
            if pk_set is None:
                grupos_alterados = []
            elif action == "post_add":
                grupos_alterados = Group.objects.filter(pk__in=pk_set)
            else:  
                grupos_alterados = instance.grupos.exclude(pk__in=pk_set)
        elif isinstance(instance, Group):
            grupos_alterados = [instance]
        else:
            logger.error(f"Tipo de instância inesperado: {type(instance)}")
            return

        if grupos_alterados: 
            for grupo in grupos_alterados:
                update_group_permissions(grupo)
                logger.info(f"Permissões do grupo {grupo.name} atualizadas.")

                # Atualizar permissões dos usuários do grupo
                for user in grupo.user_set.all():
                    update_user_permissions(user)
                    user.save()


from .models import Modulo
@receiver(pre_delete, sender=Modulo)
def remove_permissions_on_module_delete(sender, instance, **kwargs):
    logger.info(f"Sinal recebido para pre_delete em Modulo: {instance.nome}")

    grupos_afetados = list(instance.grupos.all())  
    instance.grupos.clear() 

    for grupo in grupos_afetados:
        update_group_permissions(grupo)
        logger.info(f"Permissões do grupo {grupo.name} atualizadas após exclusão do módulo.")


@receiver(post_save, sender=Modulo)
def update_permissions_on_module_save(sender, instance, **kwargs):
    logger.info(f"Sinal recebido para post_save em Modulo: {instance.nome}")
    for grupo in instance.grupos.all():
        update_group_permissions(grupo)
        logger.info(f"Permissões do grupo {grupo.name} atualizadas após salvar o módulo.")

@receiver(post_delete, sender=Group)
def update_permissions_on_group_delete(sender, instance, **kwargs):
    """Atualiza as permissões dos usuários quando um grupo é excluído."""
    logger.info(f"Sinal recebido para post_delete em Group: {instance.name}")
    for user in instance.user_set.all():
        update_user_permissions(user)
        logger.info(f"Permissões do usuário {user.username} atualizadas após exclusão do grupo.")