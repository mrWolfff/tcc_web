from django.urls import path
from .import views
urlpatterns = [
    
    
    path('', views.index, name='index'),

    path('baselogin/', views.baseLogin, name='baselogin'),
    path('base/', views.base, name='base'),

    path('demanda/', views.demandaRender, name='demandas'),
    path('cadastrodemanda/', views.cadastroDemanda, name='cadastro_demanda'),
    path('editardemanda/<int:id>/', views.editar_demanda, name='editar_demanda'),
    path('deletardemanda/<int:id>/', views.deletar_demanda, name='deletar_demanda'),
    path('pesquisa/<int:id>/', views.pesquisa, name='pesquisa'),

    path('atualizar/', views.atualizarDados, name='atualizar_dados'),
    path('servicos/', views.servicosRender, name='servicos'),
    path('interesses/', views.interesses, name='interesses'),
    path('novointeresse/<int:id>/', views.newInteresse, name='newInteresse'),
    path('deletarinteresse/<int:id>/', views.deleteInteresse, name='delete_interesse'),

    path('box/', views.box_message, name='box_message'),
    path('send/<int:id>/', views.send_message, name='send_message'),
    path('messages/<int:id>/', views.messagesUser, name='messagesUser'),


    path('deletepropostas/<int:id>/', views.deletePropostas, name='deletePropostas'),
    path('createservico/<int:id>/', views.create_servico, name='create_servico'),
    path('create_proposta/', views.create_proposta, name='create_proposta'),
    path('servico/<int:id>/', views.servico_atual, name='servico_atual'),
]
