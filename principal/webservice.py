import pdb
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import generics
from .serializers import DemandasSerializer, ServicosSerializer, PropostasSerializer, MessageSerializer, MessageSessionSerializer, UsersSerializer, Servicos_CategoriaSerializer
from rest_framework import viewsets
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import login, authenticate
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from .models import Demandas, Servicos, Message, MessageSession, Interesses, Propostas
from accounts.models import CustomUser, Servicos_Categoria
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

"""   Serializers Views   """


class Demandas_all(viewsets.ModelViewSet):
    queryset = Demandas.objects.all()
    serializer_class = DemandasSerializer


class Servicos_all(viewsets.ModelViewSet):
    queryset = Servicos.objects.all()
    serializer_class = ServicosSerializer


class Propostas_all(viewsets.ModelViewSet):
    queryset = Propostas.objects.all()
    serializer_class = PropostasSerializer


class Message_all(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class MessageSession_all(viewsets.ModelViewSet):
    queryset = MessageSession.objects.all()
    serializer_class = MessageSessionSerializer


class Users_all(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer

class Categorias(viewsets.ModelViewSet):
    queryset = Servicos_Categoria.objects.all()
    serializer_class = Servicos_CategoriaSerializer

"""  webservice VIEWS  """


def user_is_valid(token, id):
    user = CustomUser.objects.get(id=id)
    token_ = Token.objects.get_or_create(user=user)
    token_ = Token.objects.get(key=token_[0])
    if token == str(token_):
        return True
    return False


def get_new_token(request):
    if(request.method == 'GET' and request.GET.get('secret', False) == 'CHANGE_ME'):
        token = get_token(request)
        return JsonResponse({'token': token, 'success': 'true'})
    else:
        return JsonResponse({'error': 'true', 'msg': 'Invalid secret'})


@csrf_exempt
@api_view(["POST"])
def create_demanda(request):
    token = request.data.get('token')
    userid = request.data.get('id')
    titulo = request.data.get('titulo')
    descricao = request.data.get('descricao')
    data_categoria = request.data.get('categoria')
    if user_is_valid(token, userid):
        user = CustomUser.objects.get(id=userid)
        categoria = Servicos_Categoria.objects.get(categoria=data_categoria)
        Demandas.objects.create(titulo=titulo, descricao=descricao, categoria=categoria, user_demanda=user)
        return Response(status=HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["POST"])
def get_demandas(request):
    token = request.data.get('token')
    userid = request.data.get('id')
    if user_is_valid(token, userid):
        user = CustomUser.objects.get(id=userid)
        demandas = Demandas.objects.filter(user_demanda=user)
        serializer = DemandasSerializer(demandas, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(["POST"])
def index_mobile(request):
    token = request.data.get('token')
    userid = request.data.get('id')
    if user_is_valid(token, userid):
        user = CustomUser.objects.get(id=userid)
        if user.categoria == 'Prestador':
            demandas = Demandas.objects.filter(user_demanda=user)
            serializer = DemandasSerializer(demandas, many=True)
        if user.categoria == 'Consumidor': 
            categorias = Servicos_Categoria.objects.all()
            serializer = Servicos_CategoriaSerializer(categorias, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(["POST"])
def get_categorias(request):
    token = request.data.get('token')
    userid = request.data.get('id')
    aux = {}
    if user_is_valid(token, userid):
        categorias = Servicos_Categoria.objects.all()
        serializer = Servicos_CategoriaSerializer(categorias, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(["POST"])
def delete_demanda(request):
    token = request.data.get('token')
    userid = request.data.get('id')
    id_demanda = request.data.get('id_demanda')
    if user_is_valid(token, userid):
        demanda = Demandas.objects.get(id=id_demanda)
        demanda.delete()
    return Response(status=HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(["POST"])
def edit_demanda(request):
    token = request.data.get('token')
    userid = request.data.get('id')
    id_demanda = request.data.get('id_demanda')
    titulo = request.data.get('titulo')
    descricao = request.data.get('descricao')
    if user_is_valid(token, userid):
        demanda = Demandas.objects.get(id=id_demanda)
        demanda.setTitulo(titulo)
        demanda.setDescricao(descricao)
        demanda.save()
        return Response(status=HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(["POST"])
def get_user_categoria(request):
    token = request.data.get('token')
    userid = request.data.get('id')
    categ = request.data.get('categoria')
    categoria = Servicos_Categoria.objects.get(categoria=categ)
    if user_is_valid(token, userid):
        users = CustomUser.objects.filter(categoria_servico=categoria)
        serializer = UsersSerializer(users, many=True)
        return Response(serializer.data, status=HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)
        

























"""   users VIEWS   """ 


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register_user(request):
    request.data.get('first_name')
    request.data.get('last_name')
    request.data.get('username')
    request.data.get('email')
    request.data.get('categoria')
    request.data.get('celular')
    request.data.get('password')

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def get_info(request):
    token = request.data.get('token')
    userid = request.data.get('id')
    if user_is_valid(token, userid):
        user = CustomUser.objects.get(id=userid)
        if user.categoria != 'Consumidor':
            data = {
			    'first_name':user.first_name,
			    'last_name':user.last_name,
			    'username':user.username,
			    'email':user.email,
			    'categoria':user.categoria,
		    }
        else:
            data = {
			    'first_name':user.first_name,
			    'last_name':user.last_name,
			    'username':user.username,
			    'email':user.email,
			    'categoria':user.categoria,
                'categoria_servico':user.categoria_servico,
		    }
        return Response(data, status=HTTP_200_OK)
    return Response(status=HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    token = request.data.get('token')
    userid = request.data.get('id')
    if token:
        user = CustomUser.objects.get(id=userid)
        token_ = Token.objects.get_or_create(user=user)
        token_ = Token.objects.get(key=token_[0])
        if token == str(token_):
            return Response({'token': str(token_)}, status=HTTP_200_OK)
        else:
            return Response(status=HTTP_404_NOT_FOUND)
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)	
    token, _ = Token.objects.get_or_create(user=user)
    data = {
		'token':token.key,
		'id':user.id,
		'first_name':user.first_name,
		'last_name':user.last_name,
		'username':user.username,
		'email':user.email,
		'categoria_user':user.categoria,
  	}
    return Response(data, status=HTTP_200_OK)