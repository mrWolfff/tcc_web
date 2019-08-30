from django.urls import path
from . import views

urlpatterns = [
	path('signup/', views.SignUp.as_view(template_name='signup.html'), name='signup.html'),
	path('conta/<int:id>', views.minhaConta, name='conta'),
]