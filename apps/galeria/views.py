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

#Gerenciar usuarios ///
def gerenciar_usuarios(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')
    return render(request, 'galeria/gerenciar_usuarios.html')

def cadastro(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')
    return render(request, 'galeria/cadastro.html')

def editar_usuario(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')
    return render(request, 'galeria/editar_usuario.html')
#Gerenciar usuarios \\\

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