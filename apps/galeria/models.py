from django.db import models
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import Group as DjangoGroup
from django.contrib.auth.models import User

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
        print(f"Propagando permissões para o módulo: {self.nome}")

        # Atribuir permissões aos grupos associados ao módulo
        for grupo in self.grupos.all():
            for permissao in self.permissions.all():
                grupo.permissions.add(permissao)
                print(f"Adicionando permissão {permissao.codename} ao grupo {grupo.name}")

            # Atribuir permissões aos usuários do grupo
            for user in grupo.user_set.all():
                user.user_permissions.add(*self.permissions.all())
                print(f"Adicionando permissões {self.permissions.all()} ao usuário {user.username}")

        # Remover permissões dos grupos que não estão mais associados ao módulo
        for grupo in Group.objects.exclude(modulos=self):
            for permissao in grupo.permissions.all():
                grupo.permissions.remove(permissao)
                print(f"Removendo permissão {permissao.codename} do grupo {grupo.name}")

        # Remover permissões dos grupos que não devem mais possuir devido à remoção do módulo
        for grupo in Group.objects.filter(modulos=self):
            for permissao in grupo.permissions.all():
                if permissao not in self.permissions.all():
                    grupo.permissions.remove(permissao)
                    print(f"Removendo permissão {permissao.codename} do grupo {grupo.name}")

        # Atualizar as permissões diretas dos usuários
        for user in User.objects.all():
            user_permissions = set(user.user_permissions.values_list('id', flat=True))
            group_permissions = set()
            for group in user.groups.all():
                group_permissions.update(group.permissions.values_list('id', flat=True))
            if user_permissions != group_permissions:
                user.user_permissions.set(group_permissions)
                print(f"Atualizando permissões do usuário {user.username} para {group_permissions}")


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