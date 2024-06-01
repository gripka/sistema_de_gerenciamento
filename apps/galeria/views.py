# apps/galeria/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView  # Importar do módulo correto
from .forms import CadastroForm  # Certifique-se de importar o formulário correto
from django.contrib.messages import success
from django.db.models import Q

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User, Group

from django.contrib import messages

from django.core.paginator import Paginator



def index(request):
    if not request.user.is_authenticated:  # Verifica se o usuário está autenticado
        return redirect('usuarios:login')  # Redireciona para o login se não estiver

    return render(request, 'galeria/index.html')

def meu_perfil(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')  
    return render(request, 'galeria/meu_perfil.html')

#Gerenciar usuarios ///
@login_required
def gerenciar_usuarios(request):
    busca = request.GET.get('q', '')

    usuarios = User.objects.all().prefetch_related('groups')
    if busca:
        usuarios = usuarios.filter(
            Q(username__icontains=busca) | 
            Q(first_name__icontains=busca) | 
            Q(last_name__icontains=busca) |
            Q(email__icontains=busca)
        )

    grupos = Group.objects.all()

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        try:
            usuario = User.objects.get(id=usuario_id)
            usuario.delete()
            messages.success(request, 'Usuário excluído com sucesso!')
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
        
        return redirect('galeria:gerenciar_usuarios')  # Redireciona para evitar reenvio do formulário

    grupos = Group.objects.all()  
    return render(request, 'galeria/gerenciar_usuarios.html', {'usuarios': usuarios, 'grupos': grupos, 'busca': busca})



class UserCreateView(CreateView):
    form_class = CadastroForm  # Usar o nome correto do formulário
    template_name = 'galeria/cadastro.html'

    def form_valid(self, form):
        user = form.save()
        success(self.request, 'Novo usuário cadastrado com sucesso!')  # Adiciona a mensagem de sucesso
        return render(self.request, self.template_name, {'form': self.form_class()})  # Renderiza o formulário em branco novamente
    
    def form_invalid(self, form):
        return render(self.request, self.template_name, {'form': form})  # Renderiza o formulário com os erros

@login_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('galeria:gerenciar_usuarios')  # Redireciona para a página de gerenciar usuários após a edição
    else:
        form = UserChangeForm(instance=usuario)

    return render(request, 'galeria/editar_usuario.html', {'form': form, 'usuario': usuario})

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

@login_required
def excluir_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        usuario.delete()
        return redirect('galeria:gerenciar_usuarios')