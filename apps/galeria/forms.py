import django_filters

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from django_select2.forms import ModelSelect2MultipleWidget

from .models import Modulo, Transacao


class LoginForm(forms.Form):
    username = forms.CharField(
        label="",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nome de usuário",
            }
        )
    )

    password = forms.CharField(
        label="",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Digite sua senha",
            }
        )
    )


class CadastroForm(UserCreationForm):
    email = forms.EmailField(
        label="E-mail",
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: luiz@luiz.com",
            }
        )
    )
    first_name = forms.CharField( 
        label="Nome",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Seu nome",
            }
        )
    )
    last_name = forms.CharField(
        label="Sobrenome",
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Seu sobrenome",
            }
        )
    )


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name') 

    def clean_username(self):
        nome = self.cleaned_data.get("username")

        if nome:
            nome = nome.strip()
            if " " in nome:
                raise forms.ValidationError("Caractere inválido")
            else:
                return nome

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email


class EditarUsuarioForm(forms.ModelForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Perfis',
        required=False
    )
    is_active = forms.BooleanField(
        label='Ativo',
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
            }
        )
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'groups', 'is_active')


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Buscar por nome')

    class Meta:
        model = Group
        fields = ['name']

class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Permissões'
    )
    modulos = forms.ModelMultipleChoiceField(
        queryset=Modulo.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Módulos'
    )
    transacoes = forms.ModelMultipleChoiceField(
        queryset=Transacao.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Transações'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions', 'modulos', 'transacoes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['permissions'].choices = [
                (perm.pk, f"{perm.name} - {perm.codename}") 
                for perm in Permission.objects.all().order_by('content_type_id')
            ]
            self.fields['modulos'].initial = self.instance.modulos.all()
            self.fields['transacoes'].initial = self.instance.transacoes.all()

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()

        instance.permissions.set(self.cleaned_data['permissions'])
        instance.modulos.set(self.cleaned_data['modulos'])
        instance.transacoes.set(self.cleaned_data['transacoes'])

        if commit:
            instance.save()
            self._propagate_module_permissions(instance)

        return instance

    def _propagate_module_permissions(self, group):
        """
        Propaga as permissões dos módulos para o grupo.
        """
        group_permissions = set()
        
        for modulo in group.modulos.all():
            group_permissions.update(modulo.permissions.all())

        current_module_permissions = set(group.permissions.all())
        for permission in current_module_permissions:
            if permission not in group_permissions:
                group.permissions.remove(permission)


class ModuloForm(forms.ModelForm):
    transacoes = forms.ModelMultipleChoiceField(queryset=Transacao.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Modulo
        fields = ['nome', 'descricao', 'transacoes', 'permissions']
    
    def clean_nome(self):
        nome = self.cleaned_data['nome']
        
        if Modulo.objects.filter(nome__iexact=nome).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError('Já existe um módulo com este nome.')
        
        return nome

    def __init__(self, *args, **kwargs):
        super(ModuloForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['transacoes'].initial = self.instance.transacoes.all()

    def save(self, commit=True):
        modulo = super(ModuloForm, self).save(commit=commit)
        if commit:
            modulo.transacoes.set(self.cleaned_data['transacoes'])
        return modulo


class TransacaoForm(forms.ModelForm):
    permissoes = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Funções (Permissões)"
    )

    class Meta:
        model = Transacao
        fields = ['nome', 'descricao', 'permissoes']

    def clean_nome(self):
        nome = self.cleaned_data['nome'].upper()
        transacao_id = self.instance.pk

        if Transacao.objects.filter(nome=nome).exclude(pk=transacao_id).exists():
            raise ValidationError('Já existe uma transação com este nome.')
        return nome

    def __init__(self, *args, **kwargs):
        super(TransacaoForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            permissoes_associadas = self.instance.permissoes.all()
            self.fields['permissoes'].initial = [permissao.pk for permissao in permissoes_associadas]

    def save(self, commit=True):
        transacao = super().save(commit=False)
        if commit:
            transacao.save()
            self.save_m2m()  
        return transacao


class FuncaoForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name', 'codename']  


    def __init__(self, *args, **kwargs):
        super(FuncaoForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Nome'
        self.fields['codename'].label = 'Descrição'

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')

        if name:
            content_type = ContentType.objects.get(app_label='auth', model='permission')
            existing_permission = Permission.objects.filter(
                name=name,
                content_type=content_type
            ).exclude(id=self.instance.id if self.instance else None).exists() 

            if existing_permission:
                raise ValidationError(
                    'Já existe uma permissão com este nome para este tipo de conteúdo.'
                )
        return cleaned_data