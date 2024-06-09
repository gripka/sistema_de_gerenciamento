from django.urls import path
from . import views

app_name = 'galeria'

urlpatterns = [
    path('', views.index, name='index'), 
    path('meu-perfil/', views.meu_perfil, name='meu_perfil'),
    path('gerenciar-usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),

    path('gestao-de-perfis/', views.gestao_de_perfis, name='gestao_de_perfis'),
    path('cadastro/', views.UserCreateView.as_view(), name='cadastro'),
    path('editar-usuario/<int:pk>/', views.editar_usuario, name='editar_usuario_id'),  # Formulário preenchido com o ID do usuário
    path('buscar_grupos/', views.buscar_grupos, name='buscar_grupos'),

    # ... outras URLs ...
    path('gestao-de-perfis/criar/', views.criar_grupo, name='criar_grupo'),
    path('gestao-de-perfis/editar/<int:pk>/', views.editar_grupo, name='editar_grupo'),
    path('gestao-de-perfis/excluir/<int:pk>/', views.excluir_grupo, name='excluir_grupo'),

    # Corrigindo as rotas dos módulos
    path('modulos/', views.listar_modulos, name='listar_modulos'),
    path('modulos/criar/', views.criar_modulo, name='criar_modulo'),
    path('modulos/editar/<int:pk>/', views.editar_modulo, name='editar_modulo'),
    path('modulos/excluir/<int:pk>/', views.excluir_modulo, name='excluir_modulo'),
    
    path('transacoes/', views.transacoes, name='transacoes'),
    path('criar-transacao/', views.criar_transacao, name='criar_transacao'),

    path('excluir-transacao/<int:pk>/', views.excluir_transacao, name='excluir_transacao'),
    path('editar-transacao/<int:transacao_id>/', views.editar_transacao, name='editar_transacao'),
    

]