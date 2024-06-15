from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from ..galeria.forms import LoginForm
from .forms import RedefinirSenhaForm


def login_view(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data["username"]
            senha = form.cleaned_data["password"]

            usuario = authenticate(request, username=nome, password=senha)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, f"{nome} logado com sucesso!")
                return redirect(reverse("galeria:gerenciar_usuarios"))
            else:
                messages.error(request, "Nome de usuário ou senha incorretos.")
    return render(request, "usuarios/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "Logout efetuado com sucesso!")
    return redirect("usuarios:login")


def recuperar_senha(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_url = (
                f"{settings.SITE_URL}/usuarios/redefinir-senha/{uidb64}/{token}/"
            )

            subject = "Recuperação de senha"
            message = f"Clique no link para redefinir sua senha: {reset_url}"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, "Email de recuperação enviado com sucesso!")
            return redirect("usuarios:login") 

        else:
            messages.error(request, "Email não cadastrado.")

    return render(request, "usuarios/recuperar_senha.html")


def redefinir_senha(request, uidb64, token):
    print("View redefinir_senha chamada")
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = RedefinirSenhaForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data["new_password"]
                user.set_password(new_password)
                user.save()
                messages.success(request, "Sua senha foi alterada com sucesso!")
                return redirect("usuarios:login")
        else:
            form = RedefinirSenhaForm()
        return render(
            request, "usuarios/redefinir_senha.html", {"form": form}
        ) 
    else:
        messages.error(request, "Link de redefinição de senha inválido ou expirado.")
        return redirect("usuarios:recuperar_senha")