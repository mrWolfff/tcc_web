from django.db import models
from django.utils import timezone
from django import forms
from accounts.models import Usuario_Categoria, CustomUser, Servicos_Categoria
from django.conf import settings

class Demandas(models.Model):
    titulo = models.TextField()
    descricao = models.TextField()
    data = models.DateTimeField(default=timezone.now)
    user_demanda = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Servicos_Categoria, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='Ativo')

    class Meta:
        ordering = ['data']

    def __str__(self):
        return self.titulo
    
    def setTitulo(self, titulo):
        self.titulo = titulo
    
    def setDescricao(self, descricao):
        self.descricao = descricao
    
    def set_status(self):
        self.status = 'Inativo'

class Interesses(models.Model):
    interesse = models.ForeignKey(Demandas, on_delete=models.CASCADE, blank=True)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, related_name='usuario')
    data = models.DateTimeField(default=timezone.now)
    user_interesse = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_interesse')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return self.titulo


class Comentarios(models.Model):
    comentario = models.TextField()
    data = models.DateTimeField(default=timezone.now)
    user_prestador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usuarios_prestador')
    user_comentario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='usuarios_comentario')

    class Meta:
        ordering = ['data']

    def __str__(self):
        return self.comentario

    def set_comentario(self, comentario):
        self.comentario = comentario

class MessageSession(models.Model):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='do_usuario')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='para_usuario')
    
    def get_absolute_url(self):
    	return "/messages/%i/" % self.id



class Propostas(models.Model):
    proposta = models.TextField()
    valor = models.FloatField(blank=True)
    data = models.DateTimeField(default=timezone.now)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    user_proposta = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_proposta')
    to_user_proposta = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user_proposta')
    demanda = models.ForeignKey(Demandas, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=True)
        
    def set_status(self):
        self.ativo = False

class Message(models.Model):
    message = models.TextField()
    data = models.DateTimeField(default=timezone.now)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='to_user')
    session = models.ForeignKey(MessageSession, on_delete=models.CASCADE)
    is_proposta = models.BooleanField(default=False)
    proposta = models.ForeignKey(Propostas, on_delete=models.CASCADE, null=True)
    
    def set_proposta(self, proposta):
        self.is_proposta = True
        self.proposta = proposta

    class Meta:
        ordering = ['data']

class Servicos(models.Model):
    data_servico = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=240, default='Ativo')
    proposta = models.ForeignKey(Propostas, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_prestador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_prestador')
    justificativa = models.TextField(blank=True, default='')
    cancel_confirm = models.BooleanField(default=False)
    avaliacao = models.FloatField(blank=True, default=0)
    sugestao_critica = models.TextField(blank=True, default='')
    
    
    def get_absolute_url(self):
    	return "/servico/%i/" % self.id

    def finish_servico(self, avaliacao, sugestao_critica):
        if self.status == 'Ativo':
            self.avaliacao = avaliacao
            self.sugestao_critica = sugestao_critica
            self.status = 'Concluído'
            return True
        return False

    def cancel_servico(self, justificativa):
        if self.status == 'Ativo':
            self.justificativa = justificativa
            self.status = 'Cancelado sem Confirmação'
            return True
        if self.cancel_confirm == False:
            self.status = 'Cancelado'
            self.cancel_confirm = True
            return True
        return False