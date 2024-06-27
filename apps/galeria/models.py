from django.db import models
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import Group as DjangoGroup


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

        # Adicionar permissões aos grupos associados ao módulo que não as possuem
        for grupo in self.grupos.all():
            for permissao in self.permissions.all():
                if not grupo.permissions.filter(pk=permissao.pk).exists():
                    print(f"Adicionando permissão {permissao.codename} ao grupo {grupo.name}")
                    grupo.permissions.add(permissao)

        # Remover permissões dos grupos que não estão mais associados ao módulo
        for grupo in Group.objects.exclude(modulos=self):
            for permissao in grupo.permissions.all():
                if self.permissions.filter(pk=permissao.pk).exists():
                    print(f"Removendo permissão {permissao.codename} do grupo {grupo.name}")
                    grupo.permissions.remove(permissao)

        # Remover permissões dos grupos que não devem mais possuir devido à remoção do módulo
        for grupo in Group.objects.filter(modulos=self):
            for permissao in grupo.permissions.all():
                if permissao not in self.permissions.all():
                    print(f"Removendo permissão {permissao.codename} do grupo {grupo.name}")
                    grupo.permissions.remove(permissao)


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