from django.db import models

#Modelos Principais
class Usuario(models.Model):
    nome_usuario = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    matricula = models.CharField(max_length=50, unique=True)  # Novo campo para a matrícula
    senha = models.CharField(max_length=255)

class Perfil(models.Model):
    nome_perfil = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True)  # Permite descrições em branco

class Transacao(models.Model):
    nome_transacao = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True)

class Modulo(models.Model):
    nome_modulo = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True)

class Funcao(models.Model):
    nome_funcao = models.CharField(max_length=255, unique=True)
    descricao = models.TextField(blank=True)

#Modelos de Relacionamento
