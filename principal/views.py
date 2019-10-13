from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
import pdb
from django.views.generic import CreateView
from .models import Demandas, Servicos, Ofertas, Chat, Message, MessageSession, Interesses
from .forms import DemandasForm, OfertasForm, OfertasFormEdit, MessageForm, DemandasFormEdit
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
##############################################################################
## INDEX E BASE ##############################################################
def baseLogin(request):
    return render(request, 'registration/baselogin.html')
@login_required
def index(request):
    if request.POST.get('troca_user_P'):
        token = request.GET.get('csrfmiddlewaretoken')
        string = {'csrfmiddlewaretoken': token, 'categoria': 'Consumidor'}
        form = TrocaCategoria(string or None, instance=request.user)
        if form.is_valid():
            form.save()
    if request.POST.get('troca_user_C'):
        token = request.GET.get('csrfmiddlewaretoken')
        string = {'csrfmiddlewaretoken': token, 'categoria': 'Prestador'}
        form = TrocaCategoria(string or None, instance=request.user)
        if form.is_valid():
            form.save()
    return render(request, 'principal/index.html')
@login_required
def indexC(request):
    ofertas = Ofertas.objects.all()
    categorias = Servicos_Categoria.objects.all()
    querys = ''
    if request.POST != None:
        busca = request.POST.get('pesquisa')
        if busca:
            ofertas = ofertas.filter(titulo_ofertas__icontains=busca)
            querys = CustomUser.objects.filter(username__icontains=busca)
    return render(request, 'principal/indexC.html', {'querys': querys, 'ofertas': ofertas, 'categorias': categorias})
@login_required
def indexP(request):
    messages.success(request, 'Your password was updated successfully!', extra_tags='alert')
    userid = get_user_model()
    demandas = Demandas.objects.all()
    querys = demandas
    if request.POST:
        busca = request.POST.get('pesquisa')
        if busca:
            querys = demandas.filter(titulo_demanda__icontains=busca)
    else:
        querys = demandas.prefetch_related('categoria')
        #querys = demandas.filter(categoria_id__icontains=user.categoria_servico)
    return render(request, 'principal/indexP.html', {'querys': querys, 'userid': userid})
@login_required
def pesquisa(request, id):
    users = CustomUser.objects.all()
    results = users.filter(categoria_servico__id=id)
    querys = Ofertas.objects.all()
    return render(request, 'principal/pesquisa.html', {'results': results})
@login_required
def base(request):
    return render(request, 'principal/base.html')
#############################################################################
## DEMANDAS #################################################################
@login_required
def demandaRender(request):
    usuarios = CustomUser.objects.all()
    demanda = Demandas.objects.all()
    querys = demanda.filter(usuario_demanda=request.user)
    #querys = demanda.select_related('usuario_demanda').get(id=1)
    return render(request, 'principal/demandas.html', {'querys': querys, 'usuarios': usuarios})


@login_required
def cadastroDemanda(request):
    form = Demandas.objects.all()
    usuarios = CustomUser.objects.all()
    user = request.user.id
    if request.POST != None:
        form = request.POST
        f = form.copy()
        f.appendlist('usuario_demanda', user)
        form = DemandasForm(f, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Post editado com sucesso')
                return redirect('demandas')
            except:
                return HttpResponse("Não foi possivel cadastrar")
    return render(request, 'principal/cadastro_demanda.html', {'form': form, 'usuarios': usuarios})


def editarDemanda(request, id):
    demandas = Demandas.objects.get(id=id)
    form = ''
    if request.POST != None:
        form = DemandasFormEdit(request.POST or None, instance=demandas)
        if form.is_valid():
            form.save()
            return redirect('demandas')
    return render(request, 'principal/editar_demanda.html', {'demandas': demandas, 'form': form})


def deletarDemanda(request, id):
    demanda = Demandas.objects.get(id=id)
    if request.POST != None:
        demanda.delete()
        return redirect('demandas')
    return render(request, 'principal/deletardemanda.html', {'demanda': demanda})


###############################################################################
## OFERTAS ####################################################################
def ofertasRender(request):
    ofertas = Ofertas.objects.all()
    querys = ofertas.filter(usuario_oferta=request.user)
    usuarios = CustomUser.objects.all()
    return render(request, 'principal/ofertas.html', {'querys': querys, 'usuarios': usuarios})
def cadastroOfertas(request):
    user = request.user.id
    form = Ofertas.objects.all()
    usuarios = CustomUser.objects.all()
    if request.POST != None:
        form = request.POST
        f = form.copy()
        f.appendlist('usuario_oferta', user)
        form = OfertasForm(f, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ofertas')

    return render(request, 'principal/cadastro_oferta.html', {'form': form, 'usuarios': usuarios})
def editarOfertas(request, id):
    oferta = Ofertas.objects.get(id=id)
    form = OfertasFormEdit(instance=oferta)
    if request.POST:
        form = OfertasFormEdit(request.POST or None, instance=oferta)
        if form.is_valid():
            form.save()
            return redirect('ofertas')
    return render(request, 'principal/editar_oferta.html', {'oferta': oferta, 'form':form})
def deletarOfertas(request, id):
    oferta = Ofertas.objects.get(id=id)
    if request.POST != None:
        oferta.delete()
        return redirect('ofertas')
    return render(request, 'principal/deletar_oferta.html', {'oferta': oferta})
########################################################################
## SERVICOS ############################################################
def servicosRender(request):
    form = Demandas.objects.all()
    usuarios = CustomUser.objects.all()
    return render(request, 'principal/servicos.html', {'form': form, 'usuarios': usuarios})

def cadastroServicos(request):
    form = Demandas.objects.all()
    usuarios = CustomUser.objects.all()
    if request.POST != None:
        form = DemandasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('demanda')

    return render(request, 'principal/cadastrodemanda.html', {'form': form, 'usuarios': usuarios})

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

def interesses(request, id):
    interesses = Interesses.objects.filter(user=request.user)
    return render(request, 'principal/interesses.html', {'interesses':interesses})
    
def newInteresse(request, id):
    user = CustomUser.objects.get(id=id)
    try:
        Interesses.objects.get(usuario_interesse=user)
        #GERAR MENSAGEM QUE INTERESSE JA ESTA CADASTRADO!
    except:
        obj = Intesses.objects.created(usuario_interesse=user, user=request.user)
    return render(request, 'principal/interesses.html', {'interesses':interesses})

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
            return redirect('indexP')
    return render(request, 'principal/atualizar_dados.html', {'form': form, 'user': user})

######################################################################################
# CHAT ###############################################################################
@login_required
def chat(request):
    c = Chat.objects.all()
    return render(request, "chat/chat.html", {'home': 'active', 'chat': c})

def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(user=request.user, message=msg)
        msg = c.user.username+": "+msg
        c = Chat(user=request.user, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': c.user.username})
    else:
        return HttpResponse('Request must be POST.')

def messages(request):
    c = Chat.objects.all()
    return render(request, 'chat/messages.html', {'chat': c})
##########################################################################
def box_message(request):
    search = MessageSession.objects.filter(
        to_user=request.user).exclude(from_user=request.user)
    aux = True
    if not search:
        search = MessageSession.objects.filter(from_user=request.user)
        aux = False
    # pdb.set_trace()
    return render(request, 'principal/boxmessage.html', {'search': search, 'aux': aux})
def messagesUser(request, id):
    messages = Message.objects.filter(session=id)
    #pdb.set_trace()
    session = MessageSession.objects.get(id=id)
    form = MessageForm()
    post = request.POST
    from_user = request.POST.get('from_user')
    to_user = request.POST.get('to_user')
    if post:
        message = request.POST.get('message')
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
    to_user = session.from_user
    from_user = request.user
    session_user = ''
    if to_user == from_user:
        session_user = session.to_user
    
    return render(request, 'principal/messages.html', {'to_user': to_user, 'messages': messages, 'from_user': from_user, 'session_user': session_user})


def box_message_send(request):
    search = MessageSession.objects.filter(from_user=request.user)
    return render(request, 'principal/boxmessagesend.html', {'search': search})


def send_message(request, id):
    to_user = CustomUser.objects.get(id=id)
    from_user = request.user
    form = MessageForm()
    post = request.POST
    if post:
        message = request.POST.get('message')
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
