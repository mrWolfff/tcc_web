from django.db import models
from django.utils import timezone
from django import forms
from accounts.models import Usuario_Categoria, CustomUser, Servicos_Categoria
from django.conf import settings



class Chat(models.Model):
	message = models.CharField(max_length=254)
	date = models.DateTimeField(auto_now=True)
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

	def __str__(self):
		return self.message

class Demandas(models.Model):

	STATUS_DEMANDAS = [
        ("E", "ESPERA"), ("", ""), ("", "")]

	titulo_demanda = models.CharField(max_length=50)
	descricao_demanda = models.CharField(max_length=250)
	data_demanda = models.DateTimeField(default=timezone.now)
	requisitos_demanda = models.CharField(max_length=150)
	anexo_demanda = models.FileField(upload_to='../media', max_length=250, null=True)
	imagem_demanda = models.ImageField(upload_to='../media', max_length=250, null=True)
	usuario_demanda = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='usuarios_servicos')
	usuario_prestador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
	avaliacao_demanda = models.CharField(max_length=10)
	status_demanda = models.CharField(max_length=20, choices=STATUS_DEMANDAS, default="ESPERA")
	categoria = models.ForeignKey(Servicos_Categoria, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.titulo_demanda

class Servicos(models.Model):
	titulo_servico = models.CharField(max_length=50)
	descricao_servico = models.CharField(max_length=250)
	data_servico = models.DateTimeField(default=timezone.now)
	requisitos_servico = models.CharField(max_length=150)

		


class Ofertas(models.Model):
	titulo_ofertas = models.CharField(max_length=50)
	descricao_ofertas = models.CharField(max_length=250)
	data_oferta = models.DateTimeField(default=timezone.now)
	imagem_oferta = models.ImageField(upload_to='../media', null=True)
	usuario_oferta = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usuarios_oferta')

	def __str__(self):
		return self.usuario_oferta


class Interesses(models.Model):
	interesse = models.ForeignKey(Demandas, on_delete=models.CASCADE, null=True, blank=True)
	data_interesse = models.DateTimeField(default=timezone.now)
	#interesse_servico = models.ForeignKey(Servicos, on_delete=models.CASCADE, related_name='INTERESSE_SERVICO')
	usuario_interesse = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usuarios_interesse')
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')

	class Meta:
	 	ordering = ['-data_interesse']

class Comentarios_Perfil(models.Model):
	comentario = models.CharField(max_length=100)
	data_comentario = models.DateTimeField(default=timezone.now)
	hora_comentario = models.DateTimeField(default=timezone.now)
	usuario_prestador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usuarios_prestador')
	usuario_comentario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usuarios_comentario')

	class Meta:
		ordering = ['hora_comentario']

class MessageSession(models.Model):
	from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_1')
	to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_2')

class Message(models.Model):
	message = models.CharField(max_length=254)
	time_message = models.DateTimeField(default=timezone.now)
	from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
	to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
	session = models.ForeignKey(MessageSession, on_delete=models.CASCADE)