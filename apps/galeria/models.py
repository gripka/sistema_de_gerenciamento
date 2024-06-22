from django.db import models
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.models import Group as DjangoGroup

class Modulo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    grupos = models.ManyToManyField(Group)

    class Meta:
        db_table = 'modulo'

    def __str__(self):
        return self.nome

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
