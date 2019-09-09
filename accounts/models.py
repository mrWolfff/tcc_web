from django.db import models
from django.contrib.auth.models import AbstractUser

class Servicos_Categoria(models.Model):
	categoria_servico = models.CharField(max_length=50)
	def __str__(self):
		return self.categoria_servico

class Usuario_Categoria(models.Model):
	categoria_usuario = models.CharField(max_length=30),

	def __str__(self):
		return self.categoria_categoria


class CustomUser(AbstractUser):
	CATEGORIAS = [('Prestador', 'Prestador'), ('Consumidor', 'Consumidor')]
	SEXOS = [('MAS', 'Masculino'), ('FEM', 'Feminino')]
	ESTADOS = [('PARANÁ', 'PR'), ('RIO GRANDE DO SUL', 'RS'), ('São Paulo', 'SP'), ('Santa Catarina', 'SC')]
	categoria = models.CharField(max_length=20, null=True, choices=CATEGORIAS)
	#
	cpf_cnpj= models.CharField(max_length=15, null=True, blank=True)
	sexo=models.CharField(max_length=11, null=True, blank=True, choices=SEXOS)
	data_nasc = models.DateTimeField(null=True, blank=True)
	#Contato
	telefone = models.CharField(max_length=20, null=True, blank=True)
	celular = models.CharField(max_length=20, null=True, blank=True)
	site = models.CharField(max_length=100, null=True, blank=True)
	#Localização
	estado = models.CharField(max_length=50, null=True, blank=True, choices=ESTADOS)
	cidade = models.CharField(max_length=50, null=True, blank=True,)
	endereço = models.CharField(max_length=150, null=True, blank=True,)
	#trabalho realizado
	descricao = models.CharField(max_length=150, null=True, blank=True,)
	imagem = models.ImageField(null=True, blank=True, upload_to='../media', default="https://miro.medium.com/max/3200/1*g09N-jl7JtVjVZGcd-vL2g.jpeg")
	categoria_servico = models.ForeignKey(Servicos_Categoria, on_delete=models.CASCADE, null=True, blank=True)

