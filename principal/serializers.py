from .models import Demandas, Servicos, Message, Propostas, MessageSession, Propostas
from accounts.models import CustomUser, Servicos_Categoria
from rest_framework import serializers

class DemandasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandas
        fields = ('id', 'titulo', 'descricao', 'data', 'user_demanda', 'categoria')  
        
class ServicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicos
        fields = ('url', 'id', 'data_servico', 'status', 'proposta', 'user', 'justificativa', 'cancel_confirm', 'avaliacao', 'sugestao_critica')  
         
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message', 'data', 'from_user', 'to_user', 'session', 'is_proposta')  
        
class MessageSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageSession
        fields = ('url', 'id', 'from_user', 'to_user')  
        
class Servicos_CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicos_Categoria
        fields = ('__all__')
        
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('__all__')  
        
class PropostasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propostas
        fields = ('__all__')  