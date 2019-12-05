from django.urls import path
from .import views
from .import webservice
from django.conf.urls.static import static
from django.conf import settings
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

    path('box/', views.box_message, name='box_message'),
    path('send/<int:id>/', views.send_message, name='send_message'),
    path('messages/<int:id>/', views.messagesUser, name='messagesUser'),
    path('message_ajax/', views.message_ajax, name="message_ajax"),
    path('get_message_ajax/', views.get_message_ajax, name="get_message_ajax"),
    

    path('get_propostas_ajax/', views.get_propostas_ajax, name="get_propostas_ajax"),
    path('rejeitar_proposta/<int:id>/', views.rejeitar_proposta, name='rejeitar_proposta'),
    path('createservico/<int:id>/', views.create_servico, name='create_servico'),
    path('create_proposta/', views.create_proposta, name='create_proposta'),
    path('servico/<int:id>/', views.servico_atual, name='servico_atual'),
    path('avaliar_servico/', views.avaliar_servico, name='avaliar_servico'),
    
    
    # """  urls webservice  """
    path('get_token', webservice.get_new_token),
    path('create_demanda', webservice.create_demanda),
    path('get_demandas', webservice.get_demandas),
    path('delete_demanda', webservice.delete_demanda),
    path('edit_demanda', webservice.edit_demanda),
    path('get_categorias', webservice.get_categorias),
    path('index_mobile', webservice.index_mobile),
    path('get_user_categoria', webservice.get_user_categoria),
    path('get_message_session', webservice.get_message_session, name='get_message_session'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
