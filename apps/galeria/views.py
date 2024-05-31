# apps/galeria/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView  # Importar do módulo correto
from .forms import CadastroForm  # Certifique-se de importar o formulário correto
from django.contrib.messages import success



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



class UserCreateView(CreateView):
    form_class = CadastroForm  # Usar o nome correto do formulário
    template_name = 'galeria/cadastro.html'

    def form_valid(self, form):
        user = form.save()
        success(self.request, 'Novo usuário cadastrado com sucesso!')  # Adiciona a mensagem de sucesso
        return render(self.request, self.template_name, {'form': self.form_class()})  # Renderiza o formulário em branco novamente
    
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})  # Renderiza o formulário com os erros

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

