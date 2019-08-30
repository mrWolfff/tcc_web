from django.shortcuts import render
from django.views import generic
from . forms import CustomUserCreationForm, CustomUserChangeForm, CustomUser
from .models import CustomUser
from django.utils import timezone
from django.shortcuts import redirect
import pdb
from django.urls import reverse_lazy


class SignUp(generic.CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('login')
	template_name = 'signup.html'		

def minhaConta(request, id):
	usuarios = CustomUser.objects.get(id=id)
	return render(request, 'principal/conta.html', {'usuarios':usuarios})
