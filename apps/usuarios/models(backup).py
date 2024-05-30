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
class UsuarioPerfil(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    data_associacao = models.DateTimeField(auto_now_add=True)  # Adiciona automaticamente a data/hora

class PerfilTransacao(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    transacao = models.ForeignKey(Transacao, on_delete=models.CASCADE)

class PerfilModulo(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)

class ModuloFuncao(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE)
    funcao = models.ForeignKey(Funcao, on_delete=models.CASCADE)
