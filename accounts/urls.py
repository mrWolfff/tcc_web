from django.urls import path
from django.conf.urls import url
from . import views
from principal import webservice
urlpatterns = [
	#path('signup/', views.SignUp.as_view(template_name='signup.html'), name='signup.html'),
	path('conta/<int:id>', views.minhaConta, name='conta'),
	path('editar_conta/', views.editar_conta, name='editar_conta'),
	path('configuracao/<int:id>/', views.config, name='config'),
	path('config_add/', views.config_json, name='config_json'),
	url('signup/', views.signup, name='signup'),
    url('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('api/login', webservice.login),
    path('api/get_info', webservice.get_info),
    path('api/register_user', webservice.register_user),
]