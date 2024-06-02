from apps.usuarios.models import Usuario  # Importe seu modelo de usuário
from django.contrib.auth.hashers import make_password  # Para criptografar a senha

usuario = Usuario(
    nome_usuario='teste6',
    email='teste6@example.com',
    password=make_password('admin')  # Criptografe a senha
)
usuario.save()
