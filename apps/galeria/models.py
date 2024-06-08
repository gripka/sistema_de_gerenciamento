from django.db import models

class Modulo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)  # Descrição opcional

    class Meta:
        db_table = 'modulo'  # Nome da tabela no banco de dados

    def __str__(self):
        return self.nome

class Transacao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)  # Descrição opcional
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)  # Associação com o módulo
    
    class Meta:
        db_table = 'transacao'  # Nome da tabela no banco de dados

    def __str__(self):
        return self.nome
