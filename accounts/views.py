from django.shortcuts import render, redirect
from django.views import generic
from . forms import CustomUserCreationForm, CustomUserChangeForm, CustomUser, ContaForm, SignupForm
from .models import CustomUser
from django.contrib.auth.models import User
from django.utils import timezone
import pdb
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model


# class SignUp(generic.CreateView):
#	form_class = CustomUserCreationForm
#	success_url = reverse_lazy('login')
#	template_name = 'signup.html'

def minhaConta(request, id):
	user = CustomUser.objects.get(id=id)
	form = ''
	if request.POST != None:
		form = ContaForm(request.POST or None, request.FILES or None, instance=user)
		if form.is_valid():
			form.save()
			redirect('index')
	return render(request, 'principal/conta.html', {'user': user, 'form': form})


def editar_conta(request):
	return render(request, 'principal/editar_conta.html')


def signup(request):
	# User = get_user_model()
	if request.method == 'POST':
		# pdb.set_trace()
		form = SignupForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			# current_site = get_current_site(request)
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
			email.send()
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
