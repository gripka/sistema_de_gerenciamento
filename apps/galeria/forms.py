from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group
from django.db import models
from django_select2.forms import ModelSelect2MultipleWidget

import django_filters
from django.contrib.auth.models import Group

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
    first_name = forms.CharField(  # Altere 'nome' para 'first_name'
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
    last_name = forms.CharField(   # Altere 'sobrenome' para 'last_name'
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
        fields = ('username', 'email', 'first_name', 'last_name')  # Use os nomes corretos

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
        label='Perfis'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'groups')


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Buscar por nome')

    class Meta:
        model = Group
        fields = ['name']

from django import forms
from django.contrib.auth.models import Group

from django import forms
from django.contrib.auth.models import Group, Permission

class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Permissões'
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']


from django import forms
from .models import Modulo, Transacao

class ModuloForm(forms.ModelForm):
    # Campo personalizado para selecionar transações
    transacoes = forms.ModelMultipleChoiceField(queryset=Transacao.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)

    class Meta:
        model = Modulo
        fields = ['nome', 'descricao', 'transacoes']

    def __init__(self, *args, **kwargs):
        super(ModuloForm, self).__init__(*args, **kwargs)
        # Se estiver editando um módulo existente, pré-selecione as transações associadas a ele
        if self.instance.pk:
            self.fields['transacoes'].initial = self.instance.transacoes.all()

    def save(self, commit=True):
        # Salvar o módulo e as transações associadas
        modulo = super(ModuloForm, self).save(commit=commit)
        if commit:
            modulo.transacoes.set(self.cleaned_data['transacoes'])
        return modulo

from django import forms
from django.core.exceptions import ValidationError
from .models import Transacao
from django.contrib.auth.models import Permission

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
        nome = self.cleaned_data['nome']
        if Transacao.objects.filter(nome__iexact=nome).exists():
            raise ValidationError('Já existe uma transação com este nome.')
        return nome.upper()

    def __init__(self, *args, **kwargs):
        super(TransacaoForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            permissoes_associadas = self.instance.permissoes.all()
            self.fields['permissoes'].initial = [permissao.pk for permissao in permissoes_associadas]

    def save(self, commit=True):
        transacao = super().save(commit=False)
        if commit:
            transacao.save()
            self.save_m2m()  # Salva as relações Many-to-Many
        return transacao



