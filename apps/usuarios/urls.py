from django.urls import path
from . import views


app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('recuperar-senha/', views.recuperar_senha, name='recuperar_senha'),
    path('redefinir-senha/<uidb64>/<token>/', views.redefinir_senha, name='redefinir_senha'),
]