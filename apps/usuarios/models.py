from django.db import models

from django.db import models

class Modulo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)  # Descrição opcional

    def __str__(self):
        return self.nome

class Transacao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)  # Descrição opcional
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)  # Associação com o módulo

    def __str__(self):
        return self.nome
