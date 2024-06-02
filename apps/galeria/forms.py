from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django_select2.forms import ModelSelect2MultipleWidget
from dal import autocomplete

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

class EditarUsuarioForm(UserChangeForm):
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Perfis'
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'groups')