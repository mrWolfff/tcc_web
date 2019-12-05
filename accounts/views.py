from django.shortcuts import render, redirect
from django.views import generic
from . forms import CustomUserCreationForm, CustomUserChangeForm, CustomUser, ContaForm, SignupForm
from .models import CustomUser, Informacoes
from principal.models import Comentarios
from django.contrib.auth.models import User
from django.utils import timezone
import pdb
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse, request
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.core.mail import send_mail


from django.conf import settings
settings.SENDGRID_SANDBOX_MODE_IN_DEBUG=False



# class SignUp(generic.CreateView):
#	form_class = CustomUserCreationForm
#	success_url = reverse_lazy('login')
#	template_name = 'signup.html'

def minhaConta(request, id):
	user = CustomUser.objects.get(id=id)
	form = ''
	comentarios = Comentarios.objects.filter(user=user)
	if request.user != user:
		redirect('index')
	if request.POST != None:
		form = ContaForm(request.POST or None, request.FILES or None, instance=user)
		if form.is_valid():
			form.save()
			redirect('index')
	informacoes = Informacoes.objects.filter(user=user)
	context = {
		'informacoes':informacoes,
		'user':user,
		'form':form,
		'comentarios':comentarios,
  		'media_root': settings.MEDIA_ROOT,
	}
	return render(request, 'principal/conta.html', context)

def config(request, id):
    user = CustomUser.objects.get(id=id)
    if user.categoria == 'Consumidor':
        return redirect('index')
    informacoes = Informacoes.objects.filter(user=request.user)
    return render(request, 'principal/config.html', {'user':user, 'informacoes':informacoes})

def comment_user(request):
    user = CustomUser.objects.get(id=request.POST.get('user'))
    comentario = request.POST.get('comentario')
    #pdb.set_trace()
    if request.POST:
        #pdb.set_trace()
        comment = Comentarios.objects.create(comentario=comentario, user=user, user_comentario=request.user)
        if comment:
            #pdb.set_trace()
            return redirect("/conta/%i" % user.id)
        return redirect(user.get_absolute_url)

def delete_info(request):
    id = request.POST.get('delete')
    info = Informacoes.objects.get(id=id)
    #pdb.set_trace()
    info.delete()	
    response_data = {
            'user':request.user.id,	
		}
    return JsonResponse(response_data)
    
def config_json(request):
    response_data = {}
    if request.GET:
        pdb.set_trace()
        info = Informacoes.objects.all()
        response_data['info'] = info
        return JsonResponse(response_data)
    if request.POST:
        user = CustomUser.objects.get(id=request.user.id)
        informacao = request.POST.get('informacao')
        #pdb.set_trace()
        if informacao != '':
            response_data = {
            	'informacao':informacao,
            	'user':request.user.id,	
            }
            Informacoes.objects.create(informacao=informacao, user=request.user)
            return JsonResponse(response_data)



def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			mail_subject = 'Ative seu E-mail no Sistema.'
			message = render_to_string('acc_active_email.html', {
				'user': user,
				'domain': '127.0.0.1:8000', 
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
						mail_subject, message, to=[to_email]
			)
			send_mail(mail_subject , message, 'lucasewolflew@gmail.com', [to_email], fail_silently=False)
			#email.send()
   			
			return HttpResponse('Please confirm your email address to complete the registration')
		else:
			HttpResponse('errou')
	else:
		form = SignupForm()
	return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = CustomUser.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, user.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		if user.categoria == 'Consumidor':
			return redirect('index')
		else:
			login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		return redirect('atualizar_dados')
	else:
		return HttpResponse('Activation link is invalid!')
