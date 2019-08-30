from django.shortcuts import render
from django.utils import timezone
from django.shortcuts import redirect
import pdb
from django.views.generic import CreateView
from .models import Demandas, Servicos, Ofertas
from .forms import DemandasForm, OfertasForm
from django.contrib.auth.decorators import login_required
from accounts.forms import TrocaCategoria
from accounts.models import CustomUser
from django.urls import reverse_lazy
from django.views import generic


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
	querys =''
	if request.POST != None:
		busca = request.POST.get('pesquisa')
		if busca:
			ofertas = ofertas.filter(titulo_ofertas__icontains=busca)
			querys = CustomUser.objects.filter(username__icontains=busca)
	return render(request, 'principal/indexC.html', {'querys': querys, 'ofertas':ofertas})

@login_required
def indexP(request):
	demandas = Demandas.objects.all()
	querys =''
	if request.POST != None:
		busca = request.POST.get('pesquisa')
		if busca:
			querys = demandas.filter(titulo_demanda__icontains=busca)
	return render(request, 'principal/indexP.html', {'querys': querys})

@login_required
def base(request):
	return render(request, 'principal/base.html')

@login_required
def demandaRender(request):
	usuarios = CustomUser.objects.all()
	demanda = Demandas.objects.all()
	querys = demanda.filter(usuario_demanda=request.user)
	#querys = demanda.select_related('usuario_demanda').get(id=1)
	return render(request, 'principal/demandas.html', {'querys':querys, 'usuarios':usuarios})


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
			form.save()
			return redirect('demandas')

	return render(request, 'principal/cadastro_demanda.html', {'form':form, 'usuarios':usuarios})

def editarDemanda(request, id):
	demandas = Demandas.objects.get(id=id)
	if request.POST != None:
		form = DemandasForm(request.POST or None, instance=demandas)
		if form.is_valid():
			form.save()
			return redirect('demanda')	
	return render(request, 'principal/editardemanda.html', {'demandas': demandas})

def deletarDemanda(request, id):
	demanda = Demandas.objects.get(id=id)
	if request.POST != None:
		demanda.delete()
		return redirect('index')
	return render(request, 'principal/deletardemanda.html', {'demanda': demanda})




def ofertasRender(request):
	ofertas = Ofertas.objects.all()
	querys = ofertas.filter(usuario_oferta=request.user)
	usuarios = CustomUser.objects.all()	
	return render(request, 'principal/ofertas.html', {'querys':querys, 'usuarios':usuarios})

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

	return render(request, 'principal/cadastro_oferta.html', {'form':form, 'usuarios':usuarios})

def editarOfertas(request, id):
	demandas = Demandas.objects.get(id=id)
	if request.POST != None:
		form = DemandasForm(request.POST or None, instance=demandas)
		if form.is_valid():
			form.save()
			return redirect('demanda')	
	return render(request, 'principal/editar_oferta.html', {'demandas': demandas})

def deletarOfertas(request, id):
	demanda = Demandas.objects.get(id=id)
	if request.POST != None:
		demanda.delete()
		return redirect('index')
	return render(request, 'principal/deletar_oferta.html', {'demanda': demanda})


def servicosRender(request):
	form = Demandas.objects.all()
	usuarios = CustomUser.objects.all()	
	return render(request, 'principal/servicos.html', {'form':form, 'usuarios':usuarios})

def cadastroServicos(request):
	form = Demandas.objects.all()
	usuarios = CustomUser.objects.all()	
	if request.POST != None:
		form = DemandasForm(request.POST)	
		if form.is_valid():
			form.save()
			return redirect('demanda')

	return render(request, 'principal/cadastrodemanda.html', {'form':form, 'usuarios':usuarios})

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


def detalhes_demanda(request, id):
	demanda = Demandas.objects.get(id=id)
	return render(request, 'principal/detalhes_demandas.html', {'demanda', demanda})

def detalhes_oferta(request, id):
	oferta = Ofertas.objects.get(id=id)
	return render(request, 'principal/detalhes_oferta.html', {'oferta', oferta})