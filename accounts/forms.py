from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset 

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
        fields = ('username', 'email',)

class TrocaCategoria(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('categoria',)