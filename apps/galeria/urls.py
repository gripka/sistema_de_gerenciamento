from django.urls import path
from . import views

app_name = 'galeria'

urlpatterns = [
    path('', views.index, name='index'), 
    path('meu-perfil/', views.meu_perfil, name='meu_perfil'),
    path('gerenciar-usuarios/', views.gerenciar_usuarios, name='gerenciar_usuarios'),

    path('gestao-de-perfis/', views.gestao_de_perfis, name='gestao_de_perfis'),
    path('cadastro/', views.UserCreateView.as_view(), name='cadastro'),
    path('editar-usuario/<int:pk>/', views.editar_usuario, name='editar_usuario_id'),
    path('buscar_grupos/', views.buscar_grupos, name='buscar_grupos'),

    path('gestao-de-perfis/criar/', views.criar_grupo, name='criar_grupo'),
    path('gestao-de-perfis/editar/<int:grupo_id>/', views.editar_grupo, name='editar_grupo'),
    path('gestao-de-perfis/excluir/<int:pk>/', views.excluir_grupo, name='excluir_grupo'),

    path('modulos/', views.listar_modulos, name='listar_modulos'),
    path('modulos/criar/', views.criar_modulo, name='criar_modulo'),
    path('modulos/editar/<int:pk>/', views.editar_modulo, name='editar_modulo'),
    path('modulos/excluir/<int:pk>/', views.excluir_modulo, name='excluir_modulo'),
    
    path('transacoes/', views.transacoes, name='transacoes'),
    path('criar-transacao/', views.criar_transacao, name='criar_transacao'),
    path('excluir-transacao/<int:pk>/', views.excluir_transacao, name='excluir_transacao'),
    path('editar-transacao/<int:transacao_id>/', views.editar_transacao, name='editar_transacao'),
    
    path('funcoes/', views.listar_funcoes, name='listar_funcoes'),
    path('criar-funcao/', views.criar_funcao, name='criar_funcao'),
    path('editar-funcao/<int:pk>/', views.editar_funcao, name='editar_funcao'),
    path('excluir-funcao/<int:pk>/', views.excluir_funcao, name='excluir_funcao'),

    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/exportar/', views.exportar_relatorios, name='exportar_relatorios'),
    path('relatorios/usuarios_cadastrados/', views.usuarios_cadastrados, name='usuarios_cadastrados'),
    path('relatorios/perfis_usuarios/', views.perfis_usuarios, name='perfis_usuarios'),
    path('relatorios/lista_modulos/', views.lista_modulos, name='lista_modulos'),
    path('relatorios/lista_transacoes/', views.lista_transacoes, name='lista_transacoes'),
    path('relatorios/funcoes_cadastradas/', views.funcoes_cadastradas, name='funcoes_cadastradas'),
]