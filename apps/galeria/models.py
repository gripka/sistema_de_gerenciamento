from django.db import models
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.models import User


from django.db import models
from django.contrib.auth.models import Group, Permission, User

class Modulo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    grupos = models.ManyToManyField(Group, related_name='modulos')
    permissions = models.ManyToManyField(Permission, blank=True, related_name='modulos')

    class Meta:
        db_table = 'modulo'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.propagate_permissions()

    def propagate_permissions(self):
        from .signals import update_user_permissions
        print(f"Propagando permissões para o módulo: {self.nome}")

        # Obter todas as permissões do módulo
        modulo_permissions = set(self.permissions.all())

        # Iterar sobre os grupos associados ao módulo
        for grupo in self.grupos.all():
            # Obter as permissões atuais do grupo
            group_permissions = set(grupo.permissions.all())

            # Permissões a serem adicionadas ao grupo
            permissions_to_add = modulo_permissions - group_permissions
            grupo.permissions.add(*permissions_to_add)
            for permissao in permissions_to_add:
                print(f"Adicionando permissão {permissao.codename} ao grupo {grupo.name}")

            # Permissões a serem removidas do grupo
            permissions_to_remove = group_permissions - modulo_permissions
            grupo.permissions.remove(*permissions_to_remove)
            for permissao in permissions_to_remove:
                print(f"Removendo permissão {permissao.codename} do grupo {grupo.name}")

            # Atualizar as permissões dos usuários do grupo
            for user in grupo.user_set.all():
                update_user_permissions(user)
                print(f"Atualizando permissões do usuário {user.username}")


class Transacao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    modulos = models.ManyToManyField(Modulo, related_name='transacoes')
    permissoes = models.ManyToManyField(Permission, related_name='transacoes', blank=True)
    grupos = models.ManyToManyField(Group, related_name='transacoes', blank=True)

    class Meta:
        db_table = 'transacao'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for modulo in self.modulos.all():
            modulo.propagate_permissions()


class UrlPermission(models.Model):
    url = models.CharField(max_length=255, unique=True)
    permissions = models.ManyToManyField(Permission)

    def __str__(self):
        permissions_list = ", ".join([perm.codename for perm in self.permissions.all()])
        return f"{self.url} - {permissions_list}"