from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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


class CadastroForm(UserCreationForm):  # Herda de UserCreationForm
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

    class Meta:
        model = User
        fields = ('username', 'email')

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

