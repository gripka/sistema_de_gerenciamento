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
from .filters import GroupFilter  # Se o filtro estiver em um arquivo filters.py



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
    group_filter = GroupFilter(request.GET, queryset=Group.objects.all())

    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.groups.clear()
            for group_id in form.cleaned_data['groups']:
                group = Group.objects.get(pk=group_id)
                usuario.groups.add(group)
            usuario.save()
            messages.success(request, 'Usuário editado com sucesso!')
        else:
            messages.error(request, 'Erro ao editar usuário. Verifique os dados.')

    else:
        form = EditarUsuarioForm(instance=usuario)

    return render(request, 'galeria/editar_usuario.html', {
        'form': form,
        'usuario': usuario,
        'filter': group_filter,
    })





from .models import Transacao  # Certifique-se de importar o modelo Transacao

def transacoes(request):
    if not request.user.is_authenticated:  
        return redirect('usuarios:login')
    
    # Obtendo todas as transações do banco de dados
    transacoes = Transacao.objects.all()
    
    # Passando as transações para o contexto do template
    return render(request, 'galeria/transacoes.html', {'transacoes': transacoes})



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Transacao
from .forms import TransacaoForm
from django.contrib.auth.models import Permission

@login_required
def criar_transacao(request):
    if request.method == 'POST':
        form = TransacaoForm(request.POST)
        if form.is_valid():
            transacao = form.save(commit=False)  # Salvar transação primeiro
            transacao.save()
            form.save_m2m()  # Salvar as relações Many-to-Many depois
            messages.success(request, 'Transação criada com sucesso.')
            return redirect('galeria:editar_transacao', transacao_id=transacao.id)
        else:
            messages.error(request, 'Nome já existente')
    else:
        form = TransacaoForm()

    permissoes = Permission.objects.all()
    permissoes_formatadas = []
    for permissao in permissoes:
        permissoes_formatadas.append({
            'id': permissao.id,
            'name': permissao.name,
            'codename': permissao.codename,
            'checked': False  # Por padrão, nenhuma permissão estará selecionada na criação
        })

    return render(request, 'galeria/criar_transacao.html', {
        'form': form,
        'permissoes': permissoes_formatadas,
    })




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Transacao
from .forms import TransacaoForm
from django.contrib.auth.models import Permission

from django.contrib import messages

@login_required
def editar_transacao(request, transacao_id):
    transacao = get_object_or_404(Transacao, id=transacao_id)
    permissoes = Permission.objects.all()

    if request.method == 'POST':
        form = TransacaoForm(request.POST, instance=transacao)
        if form.is_valid():
            transacao = form.save(commit=False)
            transacao.permissoes.set(form.cleaned_data['permissoes'])
            transacao.save()
            messages.success(request, 'Transação atualizada com sucesso.')
            return redirect('galeria:editar_transacao', transacao_id=transacao.id)
        else:
            messages.error(request, 'Nome já existente')

    else:
        form = TransacaoForm(instance=transacao)

    permissoes_formatadas = []
    for permissao in permissoes:
        checked = permissao in transacao.permissoes.all()
        permissoes_formatadas.append({
            'id': permissao.id,
            'name': permissao.name,
            'codename': permissao.codename,
            'checked': checked
        })

    return render(request, 'galeria/editar_transacao.html', {
        'form': form,
        'transacao': transacao,
        'permissoes': permissoes_formatadas,
    })



















# views.py
from django.shortcuts import render, redirect
from .models import Transacao

def excluir_transacao(request, pk):
    transacao = Transacao.objects.get(pk=pk)
    transacao.delete()
    # Redirecione para a página desejada após a exclusão
    return redirect('galeria:transacoes')






@login_required
def gestao_de_perfis(request):
    grupos = Group.objects.all()  # Buscar todos os grupos do banco de dados
    return render(request, 'galeria/gestao_de_perfis.html', {'grupos': grupos, 'teste': 'Olá, mundo!'})

@login_required
def excluir_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        usuario.delete()
        return redirect('galeria:gerenciar_usuarios')
    
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.db.models import Q

def buscar_grupos(request):
    query = request.GET.get('q', '')
    grupos = Group.objects.filter(Q(name__icontains=query))
    data = [{'id': grupo.id, 'name': grupo.name} for grupo in grupos]
    return JsonResponse(data, safe=False)






from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.forms import modelformset_factory




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import GroupForm  # Certifique-se de ter um formulário para grupos

@login_required
def criar_grupo(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil criado com sucesso!')
            form = GroupForm()  # Limpa o formulário
    else:
        form = GroupForm()

    return render(request, 'galeria/criar_grupo.html', {'form': form})



# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, Permission
from django.contrib import messages
from django.forms import modelformset_factory
from django import forms

@login_required
def editar_grupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    PermissionFormSet = modelformset_factory(Permission, fields=('id', 'name'), extra=0, widgets={'id': forms.CheckboxSelectMultiple})


    if request.method == 'POST':
        formset = PermissionFormSet(request.POST)
        if formset.is_valid():
            grupo.name = request.POST['nome']
            grupo.permissions.clear()
            for form in formset:
                if form.cleaned_data.get('id'):
                    grupo.permissions.add(form.cleaned_data['id'])
            grupo.save()
            messages.success(request, 'Perfil editado com sucesso!')
            return redirect('galeria:listar_grupos')
    else:
        initial_data = [{'id': perm.id} for perm in grupo.permissions.all()]
        formset = PermissionFormSet(queryset=Permission.objects.all(), initial=initial_data)

    return render(request, 'galeria/editar_grupo.html', {'formset': formset, 'grupo': grupo})



from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.models import Group

@login_required
def excluir_grupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk)

    if request.method == 'POST':
        grupo.delete()
        messages.success(request, 'Perfil excluído com sucesso!')
        return redirect('galeria:gestao_de_perfis')
    else:
        return render(request, 'galeria/confirmar_exclusao_grupo.html', {'grupo': grupo})
    








from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Modulo
from .forms import ModuloForm

@login_required
def listar_modulos(request):
    query = request.GET.get('q')
    if query:
        modulos = Modulo.objects.filter(Q(nome__icontains=query) | Q(descricao__icontains=query))
    else:
        modulos = Modulo.objects.all()
    return render(request, 'galeria/modulos.html', {'modulos': modulos})

from .models import Transacao, Modulo
from .forms import ModuloForm
from django.contrib import messages
from django.shortcuts import render, redirect

@login_required
def criar_modulo(request):
    if request.method == 'POST':
        form = ModuloForm(request.POST)
        if form.is_valid():
            modulo = form.save()
            transacoes_ids = request.POST.getlist('transacoes')
            for transacao_id in transacoes_ids:
                transacao = Transacao.objects.get(id=transacao_id)
                transacao.modulo = modulo
                transacao.save()
            messages.success(request, 'Módulo criado com sucesso!')
            form = ModuloForm()
    else:
        form = ModuloForm()
    
    transacoes = Transacao.objects.all()
    return render(request, 'galeria/criar_modulo.html', {'form': form, 'transacoes': transacoes})








from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Modulo, Transacao
from .forms import ModuloForm

@login_required
def editar_modulo(request, pk):
    modulo = get_object_or_404(Modulo, pk=pk)
    if request.method == 'POST':
        form = ModuloForm(request.POST, instance=modulo)
        if form.is_valid():
            modulo = form.save()
            transacoes_ids = request.POST.getlist('transacoes')
            modulo.transacoes.clear()  # Limpa todas as transações associadas
            for transacao_id in transacoes_ids:
                transacao = Transacao.objects.get(id=transacao_id)
                modulo.transacoes.add(transacao)  # Adiciona as novas transações
            messages.success(request, 'Módulo editado com sucesso!')
            return redirect('galeria:listar_modulos')
    else:
        form = ModuloForm(instance=modulo)
    
    transacoes = Transacao.objects.all()
    for transacao in transacoes:
        transacao.checked = transacao in modulo.transacoes.all()
    
    return render(request, 'galeria/editar_modulo.html', {'form': form, 'modulo': modulo, 'transacoes': transacoes})


@login_required
def excluir_modulo(request, pk):
    modulo = get_object_or_404(Modulo, pk=pk)
    if request.method == 'POST':
        modulo.delete()
        messages.success(request, 'Módulo excluído com sucesso!')
        return redirect('galeria:listar_modulos')
    return render(request, 'galeria/confirmar_exclusao_modulo.html', {'modulo': modulo})


