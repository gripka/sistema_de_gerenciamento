from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm, CadastroForm
from django.urls import reverse



def login_view(request): 
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['username']
            senha = form.cleaned_data['password']

            usuario = authenticate(request, username=nome, password=senha)
            if usuario is not None:
                login(request, usuario) 
                messages.success(request, f"{nome} logado com sucesso!")
                return redirect(reverse('galeria:index'))
            else:
                messages.error(request, "Nome de usuário ou senha incorretos.")
    return render(request, 'usuarios/login.html', {'form': form})


def logout_view(request): 
    logout(request)
    messages.success(request, "Logout efetuado com sucesso!")
    return redirect('usuarios:login') 

def recuperar_senha(request):
    return render(request, 'usuarios/recuperar_senha.html')

