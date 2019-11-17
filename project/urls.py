"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from principal import views, webservice

router = routers.DefaultRouter()
router.register('api/demandas', webservice.Demandas_all)
router.register('api/servicos', webservice.Servicos_all)
router.register('api/propostas', webservice.Propostas_all)
router.register('api/message', webservice.Message_all)
router.register('api/messagesession', webservice.MessageSession_all)
router.register('api/users', webservice.Users_all)
admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('principal.urls')), 
    path('', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  
    path('', LoginView.as_view(template_name='login.html'), name="login"),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework') ),
    
    #path('auth/', include('djoser.urls')),
    #path('auth/', include('djoser.urls.authtoken')),
    #path('', include('chat.urls')),
    
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)