from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario_Categoria(models.Model):
	categoria_categoria = models.CharField(max_length=30)

	def __str__(self):
		return self.categoria_categoria


class CustomUser(AbstractUser):
	CATEGORIAS = [('Prestador', 'Prestador'), ('Consumidor', 'Consumidor')]
	categoria = models.CharField(max_length=20, null=True, choices=CATEGORIAS)

