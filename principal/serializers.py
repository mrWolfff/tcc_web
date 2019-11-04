from .models import Demandas, Servicos, Message, Propostas, MessageSession
from accounts.models import CustomUser
from rest_framework import serializers

class DemandasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demandas
        fields = ('id', 'titulo', 'descricao', 'data', 'user_demanda', 'categoria')  
        
class ServicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicos
        fields = ('url', 'id', 'data_servico', 'status', 'proposta', 'user', 'justificativa', 'cancel_confirm', 'avaliacao', 'sugestao_critica')  
        
class PropostasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propostas
        fields = ('url', 'id', 'proposta', 'valor', 'data', 'data_inicio', 'data_fim', 'user_proposta', 'to_user_proposta', 'demanda')  
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('message', 'data', 'from_user', 'to_user', 'session')  
        
class MessageSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageSession
        fields = ('url', 'id', 'from_user', 'to_user')  
        
class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('url', 'id', 'first_name', 'last_name', 'email', 'cpf_cnpj', 'cpf_cnpj', 'sexo', 'nascimento', 'telefone', 'celular', 'estado', 'cidade', 'endereço', 'imagem', 'categoria_servico', 'categoria')  