from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
	#path('signup/', views.SignUp.as_view(template_name='signup.html'), name='signup.html'),
	path('conta/<int:id>', views.minhaConta, name='conta'),
	path('editar_conta/', views.editar_conta, name='editar_conta'), 
	url('signup/', views.signup, name='signup'),
    url('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
]