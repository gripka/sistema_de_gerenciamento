from django.urls import path, include
from . import views

app_name = 'galeria'

urlpatterns = [
    path('', views.index, name='index'), 
    
    path('meu-perfil/', views.meu_perfil, name='meu_perfil'),
    path('gerenciar-usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),
    path('modulos/', views.modulos, name='modulos'),
    path('transacoes/', views.transacoes, name='transacoes'),
    path('gestao-de-perfis/', views.gestao_de_perfis, name='gestao_de_perfis'),
    path('cadastro/', views.UserCreateView.as_view(), name='cadastro'),
    path('editar-usuario/<int:pk>/', views.editar_usuario, name='editar_usuario_id'),  # Formulário preenchido com o ID do usuário
    path('buscar_grupos/', views.buscar_grupos, name='buscar_grupos'),

    # ... outras URLs ...
    path('gestao-de-perfis/criar/', views.criar_grupo, name='criar_grupo'),
    path('gestao-de-perfis/editar/<int:pk>/', views.editar_grupo, name='editar_grupo'),
    path('gestao-de-perfis/excluir/<int:pk>/', views.excluir_grupo, name='excluir_grupo'),
    # ...
]

