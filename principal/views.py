from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
import pdb
from django.views.generic import CreateView
from .models import Demandas, Servicos, Message, MessageSession, Interesses, Propostas
from .forms import DemandasForm, MessageForm, DemandasFormEdit, PropostasForm
from django.contrib.auth.decorators import login_required
from accounts.forms import TrocaCategoria
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
from copy import deepcopy

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
    demandas = Demandas.objects.all()
    querys = demandas
    if request.POST.get('pesquisa'):
        busca = request.POST.get('pesquisa')
        querys = demandas.filter(titulo__icontains=busca)
    else:
        querys = demandas.prefetch_related('categoria')
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
    querys = Demandas.objects.filter(user_demanda=request.user)
    return render(request, 'principal/demandas.html', {'querys': querys})


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
    servicos = Servicos.objects.filter(user=request.user)
    if not servicos:
        servicos = Servicos.objects.filter(user_prestador=request.user)
    #pdb.set_trace()
    return render(request, 'principal/servicos.html', {'servicos': servicos})


def create_servico(request, id):
    proposta = Propostas.objects.get(id=id)
    #pdb.set_trace()
    try:
        Servicos.objects.get(proposta=proposta, user=request.user, user_prestador=proposta.user_proposta, status='Ativo')
    except:
        Servicos.objects.create(proposta=proposta, user=request.user, user_prestador=proposta.user_proposta)
    return redirect('servicos')


def servico_atual(request, id):
    servico = Servicos.objects.get(id=id)
    proposta = Propostas.objects.get(id=servico.proposta.id)
    demanda =  Demandas.objects.get(id=proposta.demanda.id)
    if request.POST.get('proposta'):
        pass
    if request.POST.get('justificativa'):
        justificativa = request.POST.get('justificativa')
        if servico.cancel_servico(justificativa):
            servico.save()
            redirect('servicos')
    if request.POST.get('avaliacao') and request.POST.get('sugestao_critica'):
        avaliacao = request.POST.get('avaliacao')
        sugestao_critica = request.POST.get('sugestao_critica')
        if servico.finish_servico(avaliacao, sugestao_critica):
            servico.save()
            redirect('servicos')
    context = {
        'servico': servico,
        'demanda':demanda,
        'proposta': proposta,
    }
    return render(request, 'principal/servico_atual.html', context)


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


def interesses(request):
    interesses = Interesses.objects.filter(user=request.user)
    return render(request, 'principal/interesses.html', {'interesses': interesses})


def newInteresse(request, id):
    user = CustomUser.objects.get(id=id)
    demanda = Demandas.objects.get(id=id)
    if request.user.categoria == 'Prestador':
        try:
            Interesses.objects.get(interesse=demanda, user=request.user)
            # GERAR MENSAGEM QUE INTERESSE JA ESTA CADASTRADO!
        except:
            Interesses.objects.create(user=request.user, interesse=demanda)
            return redirect('interesses')
    else:
        try:
            Interesses.objects.get(usuario_interesse=user, user=request.user)
            # GERAR MENSAGEM QUE INTERESSE JA ESTA CADASTRADO!
        except:
            Interesses.objects.created(usuario_interesse=user, user=request.user)
    return HttpResponse("Interesse já cadastrado ou Erro ao cadastrar!")


def deleteInteresse(request, id):
    if Interesses.objects.get(id=id).delete():
        return redirect('interesses')
    return HttpResponse('Erro ao deletar!')

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
            form.save(commit=False)
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
        try:
            aux = Propostas.objects.get(user_proposta=user_proposta, to_user_proposta=to_user_proposta)
            # aux.delete()
        except Exception as exception:
            print("Erro: {}", exception)
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
    return HttpResponse("error")


def messagesUser(request, id):
    messages = Message.objects.filter(session=id)
    session = MessageSession.objects.get(id=id)
    form = MessageForm()
    post = request.POST
    from_user = request.POST.get('from_user')
    to_user = request.POST.get('to_user')
    propostas = ''
    try:
        propostas = Propostas.objects.filter(to_user_proposta=request.user).order_by('-id')[0]
    except Exception as exception:
        try:
            propostas = Propostas.objects.filter(user_proposta=request.user).order_by('-id')[0]
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
                return redirect('box_message')
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
                    return redirect('box_message')
            except Exception as exception:
               # pdb.set_trace()
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
    to_user = session.from_user
    from_user = request.user
    session_user = ''
    demandas = Demandas.objects.filter(user_demanda=to_user)
    
    if to_user == from_user:
        session_user = session.to_user
    if not demandas:
        try:
            demandas = Demandas.objects.filter(user_demanda=session_user)
        except:
            print('erro')
    #pdb.set_trace()
    context = {'to_user': to_user, 'messages': messages, 'from_user': from_user, 'session_user': session_user, 'propostas':propostas, 'demandas': demandas}
    return render(request, 'principal/messages.html', context)



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


def deletePropostas(request, id):
    proposta = Propostas.objects.get(id=id)
    proposta.delete()
    return redirect('box_message')


