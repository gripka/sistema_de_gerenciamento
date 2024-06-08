from django.db import models

class Modulo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)

    class Meta:
        db_table = 'modulo'

    def __str__(self):
        return self.nome

class Transacao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    modulos = models.ManyToManyField(Modulo, related_name='transacoes')

    class Meta:
        db_table = 'transacao'

    def __str__(self):
        return self.nome

