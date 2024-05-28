from django.urls import path
from . import views

app_name = 'galeria'

urlpatterns = [
    path('', views.index, name='index'), 
    
    path('meu-perfil/', views.meu_perfil, name='meu_perfil'),
    path('gerenciar-usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('modulos/', views.modulos, name='modulos'),
    path('transacoes/', views.transacoes, name='transacoes'),
    path('gestao-de-perfis/', views.gestao_de_perfis, name='gestao_de_perfis'),
    
]
