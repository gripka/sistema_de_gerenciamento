# apps/galeria/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    if not request.user.is_authenticated:  # Verifica se o usuário está autenticado
        return redirect('usuarios:login')  # Redireciona para o login se não estiver

    return render(request, 'galeria/index.html')

def meu_perfil(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')  
    return render(request, 'galeria/meu_perfil.html')

def gerenciar_usuarios(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')
    return render(request, 'galeria/gerenciar_usuarios.html')

def modulos(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')
    return render(request, 'galeria/modulos.html')

def transacoes(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')
    return render(request, 'galeria/transacoes.html')

def gestao_de_perfis(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')
    return render(request, 'galeria/gestao_de_perfis.html')