# apps/galeria/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from django.views.generic.edit import CreateView  # Importar do módulo correto
from .forms import CadastroForm  # Certifique-se de importar o formulário correto
from django.contrib.messages import success
from django.db.models import Q, Case, When, Value, CharField

from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User, Group

from django.contrib import messages

from django.core.paginator import Paginator

from .forms import CadastroForm, EditarUsuarioForm

from django.db.models.functions import Lower, Substr
from django.db.models.functions import Concat, Lower, Substr, Coalesce

from dal import autocomplete

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
    page_number = request.GET.get('page')

    usuarios = User.objects.annotate(
        primeira_letra=Lower(Substr(Coalesce('first_name', 'username'), 1, 1))
    ).order_by('primeira_letra')

    if busca:
        usuarios = usuarios.filter(
            Q(username__icontains=busca) | 
            Q(first_name__icontains=busca) | 
            Q(last_name__icontains=busca) |
            Q(email__icontains=busca)
        )

    paginator = Paginator(usuarios, 7)  # 7 usuários por página
    page_obj = paginator.get_page(page_number)

    grupos = Group.objects.all()

    # Excluir usuário
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        try:
            usuario = User.objects.get(id=usuario_id)
            usuario.delete()
            messages.success(request, 'Usuário excluído com sucesso!')
        except User.DoesNotExist:
            messages.error(request, 'Usuário não encontrado.')
        
        return redirect('galeria:gerenciar_usuarios')  # Redireciona para evitar reenvio do formulário



    # Cadastro de novo usuário
    if request.method == 'POST' and 'cadastrar_usuario' in request.POST:
        form = CadastroForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # Imprime os dados do formulário
            usuario = form.save()
            print(usuario)  # Imprime o objeto User criado
            messages.success(request, 'Novo usuário cadastrado com sucesso!')
            return redirect(f'{request.path}?page={page_obj.number}&q={busca}')  # Redireciona com página e busca
    else:
        form = CadastroForm()
        
    # Edição de perfis de usuário existente
    if request.method == 'POST' and 'editar_perfis' in request.POST:
        usuario_id = request.POST.get('usuario_id')
        perfis_selecionados = request.POST.getlist('perfis')

        usuario = get_object_or_404(User, pk=usuario_id)
        grupos_atuais = usuario.groups.all()

        for grupo in grupos_atuais:
            if str(grupo.id) not in perfis_selecionados:
                usuario.groups.remove(grupo)

        for perfil_id in perfis_selecionados:
            grupo = Group.objects.get(pk=perfil_id)
            usuario.groups.add(grupo)

        messages.success(request, 'Perfis do usuário atualizados com sucesso!')
        return redirect(f'{request.path}?page={page_obj.number}&q={busca}')  # Redireciona com página e busca

    return render(request, 'galeria/gerenciar_usuarios.html', {
        'usuarios': page_obj, 
        'grupos': grupos, 
        'busca': busca,
        'form': form,  # Passa o formulário para o template
    })


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
        form = EditarUsuarioForm(request.POST, instance=usuario)  # Use o formulário personalizado
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário editado com sucesso!')
            form = UserChangeForm(instance=usuario)  # Cria um novo formulário com os dados atualizados
        else:
            messages.error(request, 'Erro ao editar usuário. Verifique os dados.')

    else:
        form = EditarUsuarioForm(instance=usuario)
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
    

