from django.urls import path
from  .import views

urlpatterns = [
path('', views.index, name='index'),
path('indexC/', views.indexC, name='indexC'),
path('indexP/', views.indexP, name='indexP'),
path('base/', views.base, name='base'),

path('demanda/', views.demandaRender, name='demandas'),
path('cadastrodemanda/', views.cadastroDemanda, name='cadastro_demanda'),
path('deletardemanda/<int:id>/', views.deletarDemanda, name='deletar_demanda'),
path('editardemanda/<int:id>/', views.editarDemanda, name='editar_demanda'),

path('ofertas/', views.ofertasRender, name='ofertas'),
path('cadastroofertas/', views.cadastroOfertas, name='cadastro_ofertas'),
path('deletarofertas/<int:id>/', views.deletarOfertas, name='deletar_ofertas'),
path('editarofertas/<int:id>/', views.editarOfertas, name='editar_ofertas'),



path('servicos/', views.servicosRender, name='servicos'),


]