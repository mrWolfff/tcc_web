from django.urls import path
from  .import views

urlpatterns = [
path('', views.index, name='index'),
path('indexC/', views.indexC, name='indexC'),
path('indexP/', views.indexP, name='indexP'),

path('baselogin/', views.baseLogin, name='baselogin'),
path('base/', views.base, name='base'),

path('demanda/', views.demandaRender, name='demandas'),
path('cadastrodemanda/', views.cadastroDemanda, name='cadastro_demanda'),
path('deletardemanda/<int:id>/', views.deletarDemanda, name='deletar_demanda'),
path('editardemanda/<int:id>/', views.editarDemanda, name='editar_demanda'),
path('pesquisa/<int:id>/', views.pesquisa, name='pesquisa'),

path('ofertas/', views.ofertasRender, name='ofertas'),
path('cadastroofertas/', views.cadastroOfertas, name='cadastro_ofertas'),
path('deletarofertas/<int:id>/', views.deletarOfertas, name='deletar_oferta'),
path('editarofertas/<int:id>/', views.editarOfertas, name='editar_oferta'),


path('atualizar/', views.atualizarDados, name='atualizar_dados'),
path('servicos/', views.servicosRender, name='servicos'),
path('interesses/', views.interesses, name='interesses'),
path('novointeresse/<int:id>/', views.newInteresse, name='newInteresse'),
path('deletarinteresse/<int:id>/', views.deleteInteresse, name='delete_interesse'),

path('chat/', views.chat, name='chat'),
path('post/', views.post, name='chat'),

#path('messages/', views.messages, name='messages'),
path('box/', views.box_message, name='box_message'),
path('boxsend/', views.box_message_send, name='box_message_send'),
path('send/<int:id>/', views.send_message, name='send_message'),
path('messages/<int:id>/', views.messagesUser, name='messagesUser'),


path('deletepropostas/<int:id>/', views.deletePropostas, name='deletePropostas'),
path('createservico/<int:id>/', views.create_servico, name='create_servico'),
path('create_proposta/', views.create_proposta, name='create_proposta'),
]