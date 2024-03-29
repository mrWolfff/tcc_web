from django.db import models
from django.contrib.auth.models import AbstractUser

class Servicos_Categoria(models.Model):
    categoria = models.TextField()
    imagem = models.ImageField(upload_to='')

    def __str__(self):
        return self.categoria


class Usuario_Categoria(models.Model):
    categoria = models.CharField(max_length=30)

    def __str__(self):
        return self.categoria_categoria


class CustomUser(AbstractUser):
    CATEGORIAS = [
        ('Prestador', 'Prestador'),
        ('Consumidor', 'Consumidor')
    ]
    SEXOS = [
        ('Masculino', 'MAS'),
        ('Feminino', 'FEM'),
        ('Prefiro não colocar', 'NENHUM')
    ]
    ESTADOS = [
        ('Acre', 'AC'),
        ('Alagoas', 'AL'),
        ('Amapá', 'AP'),
        ('Amazonas', 'AM'),
        ('Bahia', 'BA'),
        ('Ceará', 'CE'),
        ('Distrito Federal', 'DF'),
        ('Espírito Santo', 'ES'),
        ('Goiás', 'GO'),
        ('Maranhão', 'MA'),
        ('Mato Grosso', 'MT'),
        ('Mato Grosso do Sul', 'MS'),
        ('Minas Gerais', 'MG'),
        ('Pará', 'PA'),
        ('Paraíba', 'PB'),
        ('Paraná', 'PR'),
        ('Pernambuco', 'PE'),
        ('Piauí', 'PI'),
        ('Rio de Janeiro', 'RJ'),
        ('Rio Grande do Norte', 'RN'),
        ('Rio Grande do Sul', 'RS'),
        ('Rondônia', 'RO'),
        ('Roraima', 'RR'),
        ('Santa Catarina', 'SC'),
        ('São Paulo', 'SP'),
        ('Sergipe', 'SE'),
        ('Tocantins', 'TO'),
    ]
    categoria = models.CharField(max_length=20, choices=CATEGORIAS,null=True)
    cpf_cnpj = models.CharField(max_length=15, blank=True, null=True)
    sexo = models.CharField(max_length=11, blank=True, choices=SEXOS, null=True)
    nascimento = models.DateField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, choices=ESTADOS, null=True)
    cidade = models.CharField(max_length=50, blank=True, null=True)
    endereço = models.CharField(max_length=150, blank=True, null=True)
    informacao = models.TextField(blank=True, null=True)
    imagem = models.ImageField(blank=True, upload_to='user_images/',
                               default="perfil_default.jpeg", null=True)
    categoria_servico = models.ForeignKey(Servicos_Categoria, on_delete=models.CASCADE, blank=True, null=True)
    avaliacao = models.FloatField(default=0.0)

    def set_informacao(self, informacao):
        self.informacao = informacao
    
    def get_absolute_url(self):
    	return "/conta/%i/" % self.id
 
    def get_full_address(self):
        return '%s, %s, %s' % (self.endereço, self.cidade, self.estado)
    
    def avaliar(self, avaliacao, cont_servicos):
        self.avaliacao = (self.avaliacao + avaliacao) / cont_servicos
    
class Informacoes(models.Model):
    informacao = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    #perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.informacao
       


