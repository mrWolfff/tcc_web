from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Servicos_Categoria
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset

class CustomUserCreationForm(UserCreationForm):
	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('username', 'email', 'categoria')
		widgets = {'email': forms.TextInput(attrs={'required': 'True',})}
		labels = {
            'username': 'Nome de Usuário',
             'email': 'Endereço de E-mail*',
             'categoria': 'Categoria de Usuário',
        }


	def __init__(self, *args, **kwargs):
		super(CustomUserCreationForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = 'post'
		self.fields['email'].help_text = "Por favor, preencha com um endereço de e-mail válido."
		self.fields['categoria'].help_text = "Selecione o tipo de usuário que você representará no sistema: <br/> - Prestador: usuário que tem a intenção de procurar demandas de serviços e presta-los.<br/>- Consumidor: usuário que necessita de uma realização de um serviço(demanda), e/ou está a procura de prestadores. "
		self.helper.add_input(Submit('submit', 'Pronto', css_class="mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--colored"))
		self.helper.add_input(Reset('reset', 'Limpar', css_class='mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent'))


class CustomUserChangeForm(UserChangeForm):
	class Meta:
		model = CustomUser
		fields = ('first_name', 'last_name', 'cpf_cnpj', 'sexo', 'data_nasc', 'telefone', 'celular', 'site', 'estado', 'cidade', 'endereço', 'descricao', 'imagem', 'categoria_servico',)
		widgets = {'descricao': forms.Textarea(attrs={'rows': '4'})}
		fieldsets = (
			('Informações Pessoais', {
				'fields': ('cpf_cnpj', 'sexo', 'data_nasc',)
				}),
			('Endereço', {
				'fields': ('telefone', 'celular', 'site',)
				}),
			)
		labels = {
            'cpf_cnpj': 'CPF/CNPJ*',
            'sexo': 'Sexo*',
            'data_nasc': 'Data de Nascimento*',
            'celular': 'Celular*',
            'site': 'Endereço Site',
            'estado': 'Estado*',
            'cidade': 'Cidade*',
            'descricao': 'Descrição',
            'imagem': 'Imagem de Perfil',
            'categoria_servico': 'Categoria de Serviço*',
        }

	def __init__(self, *args, **kwargs):
		super(CustomUserChangeForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = 'post'
		self.fields['cpf_cnpj'].help_text = "Por favor, preencha com um CPF ou CNPJ válido."
		self.fields['site'].help_text = "Por favor, preencha caso possua um site próprio."
		self.fields['descricao'].help_text = "Nesse campo, informe o tipo de trabalho que realiza ou realizou."
		self.fields['imagem'].help_text = "Essa será a sua imagem de perfil que aparecerá para todos os usuários."
		self.fields['categoria_servico'].help_text = "Escolha a categoria de serviço que você realiza."
		self.helper.layout = Layout(
			Row(
           		Column('first_name', css_class='form-group col-md-6 mb-0'),
           		Column('last_name', css_class='form-group col-md-6 mb-0'),
           		css_class='form-row'
        	),
        	Row(
           		Column('cpf_cnpj', css_class='form-group col-md-10 	'),

           		css_class='form-row'
        	),
        	Row(
           		Column('sexo', css_class='form-group col-md-6 mb-0'),
           		Column('data_nasc', css_class='form-group col-md-6 mb-0'),
           		css_class='form-row'
        	),
        	Row(
           		Column('telefone', css_class='form-group col-md-6'),
           		Column('celular', css_class='form-group col-md-6'),
           		css_class='form-row'	
        	),
        	Row(
        		Column('site', css_class='form-group col-md-10'),
        		css_class='form-row'
        	),
        	Row(
           		Column('estado', css_class='form-group col-md-6'),
           		Column('cidade', css_class='form-group col-md-6'),
           		css_class='form-row'		
        	),
        	Row(
        		Column('endereço', css_class='form-group col-md-10'),
        		css_class='form-row'
        	),
        	Row(
        		Column('descricao', css_class='form-group col-md-8'),
        		Column('imagem', css_class='form-group col-md-4'),
        		css_class='form-row'
        	),
        	Row(
        		Column('categoria_servico', css_class='form-group col-md-10')
        		)
        )
class TrocaCategoria(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('categoria',)

class ContaForm(UserChangeForm):
  class Meta:
    model=CustomUser
    fields=('first_name', 'last_name', 'cpf_cnpj', 'data_nasc', 'celular', 'imagem', 'email')

class SignupForm(UserCreationForm):
  email = forms.EmailField(max_length=200, help_text='Required')
  class Meta:
    model = CustomUser
    fields = ('first_name', 'last_name', 'username', 'email', 'sexo', 'data_nasc', 'categoria', 'celular', 'password1', 'password2')
    widgets = {'email': forms.TextInput(attrs={'required': 'True',}),
              'data_nasc': forms.DateInput(attrs={'type': 'date'}),
              'celular': forms.TextInput(attrs={'placeholder': 'Ex.: (00) 00000-0000'})}
    labels = {
      'username': 'Nome de Usuário',
      'email': 'Endereço de E-mail*',
      'categoria': 'Categoria de Usuário',
      'data_nasc': 'Data de Nascimento*',
      'celular': 'Celular',
    }
  def __init__(self, *args, **kwargs):
    super(SignupForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper(self)
    self.helper.form_method = 'post'
    self.fields['email'].help_text = "Por favor, preencha com um endereço de e-mail válido."
    self.fields['categoria'].help_text = "Selecione o tipo de usuário que você representará no sistema: <br/> - Prestador: usuário que tem a intenção de procurar demandas de serviços e presta-los.<br/>- Consumidor: usuário que necessita de uma realização de um serviço(demanda), e/ou está a procura de prestadores. "
    self.helper.layout = Layout(
      Row(
        Column('first_name', css_class='form-group col-md-6 mb-0'),
        Column('last_name', css_class='form-group col-md-6 mb-0'),
        css_class='form-row'
      ),
      Row(
        Column('username', css_class='form-group col-md-6  '),
        Column('email', css_class='form-group col-md-6  '),
        css_class='form-row'
      ),
      Row(
        Column('sexo', css_class='form-group col-md-6 mb-0'),
        Column('data_nasc', css_class='form-group col-md-6 mb-0'),
        css_class='form-row'
      ),
      Row(
        Column('categoria', css_class='form-group col-md-6'),
        Column('celular', css_class='form-group col-md-6 cel-sp-mask'),
        css_class='form-row'  
      ),
      Row(
        Column('password1', css_class='form-group col-md-6'),
        Column('password2', css_class='form-group col-md-6'),
        css_class='form-row'  
      ),
    )