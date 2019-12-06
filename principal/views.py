from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
import pdb
from django.views.generic import CreateView
from .models import Demandas, Servicos, Message, MessageSession, Propostas, Bug
from .forms import DemandasForm, MessageForm, DemandasFormEdit, PropostasForm
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser, Servicos_Categoria
from django.urls import reverse_lazy
from django.views import generic
from accounts.forms import CustomUserChangeForm, ContaForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import DeleteView
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.response import Response
from copy import deepcopy
from django.db.models import Q
from rest_framework import generics
from .serializers import DemandasSerializer, ServicosSerializer, PropostasSerializer, MessageSerializer, MessageSessionSerializer, UsersSerializer
from rest_framework import viewsets
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
import json
from datetime import datetime, timedelta
from rest_framework.renderers import JSONRenderer

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


"""  webservice  """
def get_new_token(request):
    if(request.method == 'GET' and request.GET.get('secret', False) == 'CHANGE_ME'):
        token = get_token(request)
        return JsonResponse({'token': token, 'success': 'true'})
    else:
        return JsonResponse({'error': 'true', 'msg': 'Invalid secret'})

@csrf_exempt
@api_view(["POST"])
def create_demanda(request):
    if request.POST:
        pdb.set_trace()


"""   Index and Base   """


def baseLogin(request):
    return render(request, 'registration/baselogin.html')

def bug(request):
    bugs = Bug.objects.filter(user=request.user)
    if request.POST:
        Bug.objects.create(texto=request.POST.get('texto'), user=request.user)
    #pdb.set_trace()
    return render(request, 'principal/bug.html', {'bugs':bugs})

@login_required
def index(request):
    categorias = Servicos_Categoria.objects.all()
    querys = ''
    if request.POST.get('message'):
        """ criar mensagens aqui """
        #pdb.set_trace()
        to_user = CustomUser.objects.get(id=request.POST.get('to_user'))
        from_user = CustomUser.objects.get(id=request.POST.get('from_user'))

        post = request.POST
        try:
            MessageSession.objects.get(from_user=from_user, to_user=to_user)
            created = MessageSession.objects.get(from_user=from_user, to_user=to_user)
            url = created.get_absolute_url()
            obj = Message.objects.create(
                message=request.POST.get('message'),
                data=timezone.now,
                from_user=from_user,
                to_user=to_user,
                session=created
            )
        except:
            try:
                MessageSession.objects.get(from_user=to_user, to_user=from_user)
                created = MessageSession.objects.get(from_user=to_user, to_user=from_user)
                url = created.get_absolute_url()
                copy = post.copy()
                copy.appendlist('session', created.id)
                form = MessageForm(copy)
                if form.is_valid():
                    form.save()
                    return redirect(url)
            except:
                MessageSession.objects.get_or_create(from_user=from_user, to_user=to_user)
                created = MessageSession.objects.get(from_user=from_user, to_user=to_user)
                url = created.get_absolute_url()
                copy = post.copy()
                copy.appendlist('session', created.id)
                form = MessageForm(copy)
                if form.is_valid():
                    form.save()
                    return redirect(url)
    if request.POST.get('busca'):
        busca = request.POST.get('pesquisa')
        querys = CustomUser.objects.filter(username__icontains=busca)
    userid = get_user_model()
    demandas = Demandas.objects.filter(status='Ativo')
    querys = demandas
    if request.POST.get('pesquisa'):
        busca = request.POST.get('pesquisa')
        querys = demandas.filter(Q(titulo__icontains=busca) | Q(descricao__icontains=busca))
    #else:
     #   querys = demandas.prefetch_related('categoria')
        # querys = demandas.filter(categoria_id__icontains=user.categoria_servico)
    context = {
        'querys': querys,
        'categorias': categorias,
    }
    return render(request, 'principal/index.html', context)


@login_required
def pesquisa(request, id):
    users = CustomUser.objects.all()
    results = users.filter(categoria_servico__id=id)
    return render(request, 'principal/pesquisa.html', {'results': results})


@login_required
def base(request):
    return render(request, 'principal/base.html')
#############################################################################
## DEMANDAS #################################################################
@login_required
def demandaRender(request):
    if request.POST:
        form = DemandasFormEdit(request.POST)
        if form.is_valid():
            form.save()
    demandas = Demandas.objects.filter(user_demanda=request.user, status='Ativo')
    demandas_inativas = Demandas.objects.filter(user_demanda=request.user, status='Inativo')
    context = {
        'demandas':demandas,
        'demandas_inativas': demandas_inativas, 
    }
    #pdb.set_trace()
    return render(request, 'principal/demandas.html', context)


def editar_demanda(request, id):
    demanda = Demandas.objects.get(id=id)
    form = DemandasFormEdit(request.POST, instance=demanda)
    if form.is_valid():
        form.save()
        return redirect('demandas')
    pdb.set_trace()


@login_required
def cadastroDemanda(request):
    usuarios = CustomUser.objects.all()
    user = request.user.id
    categorias = Servicos_Categoria.objects.all()
    
    if request.POST != None:
        form = DemandasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('demandas')
    context = {
        'form':form,
        'usuarios':usuarios,
        'categorias':categorias,
    }
    return render(request, 'principal/cadastro_demanda.html', context)


def deletar_demanda(request, id):
    if request.POST:
        demanda = Demandas.objects.get(id=id)
        demanda.delete()
        return redirect('demandas')


########################################################################
## SERVICOS ############################################################
def servicosRender(request):
    servicos = Servicos.objects.filter(user=request.user, status='Ativo')
    if not servicos:
        servicos = Servicos.objects.filter(user_prestador=request.user, status='Ativo')
    servicos_concluidos = Servicos.objects.filter(user=request.user, status='Concluído')
    if not servicos_concluidos:
        servicos_concluidos = Servicos.objects.filter(user_prestador=request.user, status='Concluído')
    servicos_cancelados = Servicos.objects.filter(user=request.user, status='Cancelado')
    if not servicos_cancelados:
        servicos_cancelados = Servicos.objects.filter(user_prestador=request.user, status='Cancelado')
    context = {
        'servicos_concluidos':servicos_concluidos,
        'servicos': servicos,
        'servicos_cancelados': servicos_cancelados,
    }
    #pdb.set_trace()
    return render(request, 'principal/servicos.html', context)


def create_servico(request, id):
    proposta = Propostas.objects.get(id=id)
    #pdb.set_trace()
    try:
        Servicos.objects.get(proposta=proposta, user=request.user, user_prestador=proposta.user_proposta, status='Ativo')
    except:
        Servicos.objects.create(proposta=proposta, user=request.user, user_prestador=proposta.user_proposta, status='Ativo')
    demanda = proposta.demanda
    #pdb.set_trace()
    demanda.status = 'Inativo'   
    demanda.save()
    proposta.set_ativo() 
    proposta.save()
    return redirect('servicos')


def servico_atual(request, id):
    servico = Servicos.objects.get(id=id)
    proposta = Propostas.objects.get(id=servico.proposta.id)
    demanda =  Demandas.objects.get(id=proposta.demanda.id)
    user = servico.user_prestador
    
    if request.POST.get('proposta'):
        pass
    if request.POST.get('justificativa'):
        justificativa = request.POST.get('justificativa')
        if servico.cancel_servico(justificativa):
            servico.save()
            redirect('servicos')
    if request.POST.get('avaliacao') and request.POST.get('sugestao_critica'):
        if request.user.categoria == 'Prestador':
            avaliacao = float(request.POST.get('avaliacao'))
            sugestao_critica = request.POST.get('sugestao_critica')
            if servico.finish_servico_prestador(avaliacao, sugestao_critica):
                demanda.set_status()
                servico.save()
                redirect('servicos')
        if request.user.categoria == 'Consumidor':
            avaliacao = float(request.POST.get('avaliacao'))
            sugestao_critica = request.POST.get('sugestao_critica')
            if servico.finish_servico(avaliacao, sugestao_critica):
                cont_servico = Servicos.objects.filter(user_prestador=user).count()
                user.avaliar(avaliacao, cont_servico)
                user.save()
                demanda.set_status()
                servico.save()
                redirect('servicos')
    context = {
        'servico': servico,
        'demanda':demanda,
        'proposta': proposta,
    }
    
    return render(request, 'principal/servico_atual.html', context)

def avaliar_servico(request):
    avaliacao = request.POST.get('avaliacao')
    avaliacao_do_prestador = request.POST.get('avaliacao_do_prestador')
    servico = Servicos.objects.get(id=request.POST.get('servico'))
    user = servico.user_prestador
    if avaliacao:
        avaliacao = float(request.POST.get('avaliacao'))
        cont_servico = Servicos.objects.filter(user_prestador=user).count()
        user.avaliar(avaliacao, cont_servico)
        user.save()
        servico.avaliacao = avaliacao
        servico.save()
        return redirect('servicos')
    if avaliacao_do_prestador:
        avaliacao_do_prestador = float(request.POST.get('avaliacao_do_prestador'))
        servico.avaliacao_do_prestador = avaliacao_do_prestador
        servico.save()
        return redirect('servicos')
        
    #pdb.set_trace()


def editarServicos(request, id):
    demandas = Demandas.objects.get(id=id)
    if request.POST != None:
        form = DemandasForm(request.POST or None, instance=demandas)
        if form.is_valid():
            form.save()
            return redirect('demanda')
    return render(request, 'principal/editardemanda.html', {'demandas': demandas})


def deletarServicos(request, id):
    demanda = Demandas.objects.get(id=id)
    if request.POST != None:
        demanda.delete()
        return redirect('index')
    return render(request, 'principal/deletardemanda.html', {'demanda': demanda})


###############################################################################
## ATUALIZAR DADOS USER #######################################################
@login_required
def atualizarDados(request):
    form = ''
    user = request.user
    if request.POST != None:
        form = CustomUserChangeForm(
            request.POST or None, request.FILES or None, instance=user)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'principal/atualizar_dados.html', {'form': form, 'user': user})

######################################################################################
##########################################################################


def box_message(request):
    search = MessageSession.objects.filter(
        to_user=request.user).exclude(from_user=request.user)
    cont = search.count()
    aux = True
    if not search:
        search = MessageSession.objects.filter(from_user=request.user)
        aux = False
    context = {
        'search': search,
        'aux': aux,
        'cont': cont,
    }
    return render(request, 'principal/boxmessage.html', context)


def create_proposta(request):
    response_data = {}
    if request.POST:
        user_proposta = request.POST.get('user_proposta')
        to_user_proposta = request.POST.get('to_user_proposta')
        proposta = request.POST.get('proposta')
        valor = request.POST.get('valor')
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        demanda = request.POST.get('demanda')
        response_data = {
            'proposta': proposta,
            'valor': valor, 
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'user_proposta': user_proposta,
            'to_user_proposta': to_user_proposta,
            'demanda': demanda,
        }
        user_proposta = CustomUser.objects.get(id=user_proposta)
        to_user_proposta = CustomUser.objects.get(id=to_user_proposta)
        demanda = Demandas.objects.get(id=request.POST.get('demanda'))
            # pdb.set_trace()
        Propostas.objects.create(
            proposta=proposta,
            valor=valor,
            data_inicio=data_inicio,
            data_fim=data_fim,
            user_proposta=user_proposta,
            to_user_proposta=to_user_proposta,
            demanda=demanda,    
        )
        return JsonResponse(response_data)
    return redirect('box_message')


def messagesUser(request, id):
    messages = Message.objects.filter(session=id)
    session = MessageSession.objects.get(id=id)
    form = MessageForm()
    post = request.POST
    from_user = request.POST.get('from_user')
    to_user = request.POST.get('to_user')
    propostas = ''
    try:
        propostas = Propostas.objects.filter(to_user_proposta=request.user, ativo=True).order_by('-id')[0]
    except Exception as exception:
        try:
            propostas = Propostas.objects.filter(user_proposta=request.user, ativo=True).order_by('-id')[0]
        except Exception as exception:
            print(exception)
    if post.get('proposta_valor') or post.get('proposta'):
        user_proposta = request.POST.get('user_proposta')
        to_user_proposta = request.POST.get('to_user_proposta')
        try:
            aux = Propostas.objects.get(user_proposta=user_proposta, to_user_proposta=to_user_proposta)
            aux.delete()
        except Exception as exception:
            print("Erro: {}", exception)
            obj = PropostasForm(request.POST)
            if obj.is_valid():
                obj.save()
                return redirect('box_message')
    if post.get('message'):
        try:
            from_user = CustomUser.objects.get(id=from_user)
            to_user = CustomUser(id=to_user)
            MessageSession.objects.get(from_user=from_user, to_user=to_user)
            created = MessageSession.objects.get(
                from_user=from_user, to_user=to_user)
            copy = post.copy()
            copy.appendlist('session', created.id)
            form = MessageForm(copy)
            if form.is_valid():
                form.save()
                return redirect(created.get_absolute_url())
        except Exception as exception:
            try:
                MessageSession.objects.get(
                    from_user=to_user, to_user=from_user)
                created = MessageSession.objects.get(
                    from_user=to_user, to_user=from_user)
                copy = post.copy()
                copy.appendlist('session', created.id)
                form = MessageForm(copy)
                if form.is_valid():
                    form.save()
                    return redirect(created.get_absolute_url())
            except Exception as exception:
                MessageSession.objects.get_or_create(
                    from_user=from_user, to_user=to_user)
                created = MessageSession.objects.get(
                    from_user=from_user, to_user=to_user)
                copy = post.copy()
                copy.appendlist('session', created.id)
                form = MessageForm(copy)
                if form.is_valid():
                    form.save()
                    return redirect(created.get_absolute_url())
    to_user = session.from_user
    from_user = request.user
    session_user = ''
    demandas = Demandas.objects.filter(user_demanda=to_user, status='Ativo')
    
    if to_user == from_user:
        session_user = session.to_user
    if not demandas:
        try:
            demandas = Demandas.objects.filter(user_demanda=session_user, status='Ativo')
        except:
            print('erro')
    #pdb.set_trace()
    context = {'to_user': to_user, 'messages': messages, 'from_user': from_user, 'session_user': session_user, 'propostas':propostas, 'demandas': demandas}
    return render(request, 'principal/messages.html', context)

def get_message_ajax(request):
    from_user = request.POST.get('from_user')
    to_user = request.POST.get('to_user')
    session_user = request.POST.get('session_user')
    try:
        from_user = CustomUser.objects.get(id=from_user)
        to_user = CustomUser.objects.get(id=to_user)
        session_user = CustomUser.objects.get(id=session_user)
    except Exception as e:
        pass
    #if session_user:
    #    to_user = session_user
    session = ''
    proposta = ''
    try:
        session = MessageSession.objects.get(from_user=from_user.id, to_user=to_user.id)
        proposta = Propostas.objects.get(user_proposta=from_user.id, to_user_proposta=to_user.id)
    except Exception as e:
        try:
            session = MessageSession.objects.get(from_user=from_user.id, to_user=session_user.id)
            proposta = Propostas.objects.get(user_proposta=from_user.id, to_user_proposta=session_user.id)
        except:
            try:
                session = MessageSession.objects.get(from_user=to_user.id, to_user=from_user.id)
                proposta = Propostas.objects.get(user_proposta=to_user.id, to_user_proposta=from_user.id)
            except:
                pass
    
    if request.POST:
        #now = datetime.now()
        #before = timedelta(seconds=24)
        #past_time = now - before
        #message = Message.objects.filter(data__gte=past_time).exclude(from_user=session.from_user.id)
        
        message = Message.objects.filter(session=session)
        serializer = MessageSerializer(message, many=True)
        #pdb.set_trace()
        return JsonResponse(serializer.data, safe=False)

def get_propostas_ajax(request):
    from_user = request.POST.get('from_user')
    to_user = request.POST.get('to_user')
    session_user = request.POST.get('session_user')
    try:
        from_user = CustomUser.objects.get(id=from_user)
        to_user = CustomUser.objects.get(id=to_user)
        session_user = CustomUser.objects.get(id=session_user)
    except Exception as e:
        pass
    proposta = ''
    try:
        proposta = Propostas.objects.get(user_proposta=from_user.id, to_user_proposta=to_user.id)
    except Exception as e:
        try:
            proposta = Propostas.objects.get(user_proposta=from_user.id, to_user_proposta=session_user.id)
        except:
            try:
                proposta = Propostas.objects.get(user_proposta=to_user.id, to_user_proposta=from_user.id)
            except:
                pass
    
    if request.POST:
        serial = {
            'id': proposta.id,
            'valor_proposta': proposta.valor,
            'proposta': proposta.proposta,
            'data': proposta.data.strftime("%Y-%m-%d %H:%M:%S"),
            'data_inicio': proposta.data_inicio.strftime("%Y-%m-%d %H:%M:%S"),
            'data_fim': proposta.data_fim.strftime("%Y-%m-%d %H:%M:%S"),
            'user_proposta': proposta.user_proposta.username,
            'to_user_proposta': proposta.to_user_proposta.username,
            'demanda': proposta.demanda.titulo,
        }
        return JsonResponse(serial, safe=False)

def message_ajax(request):
    message = request.POST.get('message')
    from_user = request.POST.get('from_user')
    to_user = request.POST.get('to_user')
    #pdb.set_trace()
    if message:
        try:
            from_user = CustomUser.objects.get(id=from_user)
            to_user = CustomUser(id=to_user)
            MessageSession.objects.get(from_user=from_user, to_user=to_user)
            created = MessageSession.objects.get(
                from_user=from_user, to_user=to_user)
            copy = request.POST.copy()
            copy.appendlist('session', created.id)
            form = MessageForm(copy)
            if form.is_valid():
                form.save()
                response_data = {
                        'message':message,	
		            }
                return JsonResponse(response_data)
        except Exception as exception:
            try:
                MessageSession.objects.get(
                    from_user=to_user, to_user=from_user)
                created = MessageSession.objects.get(
                    from_user=to_user, to_user=from_user)
                copy = request.POST.copy()
                copy.appendlist('session', created.id)
                form = MessageForm(copy)
                if form.is_valid():
                    form.save()
                    response_data = {
                        'message':message,	
		            }
                    return JsonResponse(response_data)
            except Exception as exception:
                MessageSession.objects.get_or_create(
                    from_user=from_user, to_user=to_user)
                created = MessageSession.objects.get(
                    from_user=from_user, to_user=to_user)
                copy = request.POST.copy()
                copy.appendlist('session', created.id)
                form = MessageForm(copy)
                if form.is_valid():
                    form.save()
                    response_data = {
                        'message':message,	
		            }
                    return JsonResponse(response_data)
    return Response(status=HTTP_404_NOT_FOUND)

def send_message(request, id):
    to_user = CustomUser.objects.get(id=id)
    from_user = request.user
    form = MessageForm()
    post = request.POST
    if post:
        try:
            MessageSession.objects.get(from_user=from_user, to_user=to_user)
            created = MessageSession.objects.get(
                from_user=from_user, to_user=to_user)
            copy = post.copy()
            copy.appendlist('session', created.id)
            form = MessageForm(copy)
            if form.is_valid():
                form.save()
                
                return redirect('box_message')
        except:
            try:
                MessageSession.objects.get(
                    from_user=to_user, to_user=from_user)
                created = MessageSession.objects.get(
                    from_user=to_user, to_user=from_user)
                copy = post.copy()
                copy.appendlist('session', created.id)
                form = MessageForm(copy)
                if form.is_valid():
                    form.save()
                    return redirect('box_message')
            except:
                MessageSession.objects.get_or_create(
                    from_user=from_user, to_user=to_user)
                created = MessageSession.objects.get(
                    from_user=from_user, to_user=to_user)
                copy = post.copy()
                copy.appendlist('session', created.id)
                form = MessageForm(copy)
                if form.is_valid():
                    form.save()
                    return redirect('box_message')
    return render(request, 'principal/sendmessage.html', {'to_user': to_user})


def rejeitar_proposta(request, id):
    proposta = Propostas.objects.get(id=id)
    from_user = request.POST.get('from_user')
    to_user = request.POST.get('to_user')
    session_user = request.POST.get('session_user')
    if to_user == from_user:
        to_user = session_user
    try:
        from_user = CustomUser.objects.get(id=from_user)
        to_user = CustomUser.objects.get(id=to_user)
    except:
        pass
    
    try:
        session = MessageSession.objects.get(from_user=from_user.id, to_user=to_user.id)
    except:
        session = MessageSession.objects.get(from_user=to_user.id, to_user=from_user.id)
    aux = 'Proposta: ' + proposta.proposta + ' Valor: ' + str(proposta.valor) + ' Datas: de ' + str(proposta.data_inicio) + ' até ' + str(proposta.data_fim) 
    message = Message.objects.create(message=aux, from_user=session.from_user, to_user=session.to_user, session=session)
    message.set_proposta(proposta)  
    proposta.set_ativo()
    message.save()
    proposta.save()
    #pdb.set_trace()
    response_data = {
        'message':message.message
    }
    return JsonResponse(response_data)
