from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Demandas, Servicos, Message, Propostas
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset


class DemandasForm(forms.ModelForm):
    class Meta:
        model = Demandas
        fields = ('titulo', 'descricao', 'categoria', 'user_demanda')
        widgets = {'user_demanda': forms.TextInput(attrs={'type': 'hidden'})}
        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'materialize-textarea', 'data-length':'500'}),
            'titulo': forms.TextInput(attrs={'type':'text', 'class': 'validate'}),
            'categoria': forms.Select(attrs={'id': 'select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(DemandasForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
        	Row(
        		Column('titulo', css_class="col-md-6"),
           		Column('categoria', css_class='col-md-6'),
        	),
        	Row(
           		Column('descricao', css_class='col-md-12'),  		
        	),
        )
        self.helper.add_input(Submit('submit', 'Cadastrar', css_class='btn waves-effect waves-light '))

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ('message', 'from_user', 'to_user', 'session')

class DemandasFormEdit(forms.ModelForm):
	class Meta:
		model = Demandas
		fields = ( 'titulo', 'descricao')
  
class PropostasForm(forms.ModelForm):
    class Meta:
        model = Propostas
        fields = ('proposta', 'valor', 'data', 'data_inicio', 'data_fim', 'user_proposta', 'to_user_proposta', 'demanda')
        widgets = { 'proposta': forms.Textarea(attrs={'class': 'materialize-textarea'}), 
                   'valor': forms.TextInput(attrs={'type': 'number'}),
                   }
        labels = {
            'proposta': 'Proposta: ',
            'valor': 'Valor da Proposta: *',
            'data_inicio': 'Data Inicio Serviço: ',
            'data_fim': 'Data Fim Serviço: ',
            'demanda': 'Demanda: ',
        }
 
