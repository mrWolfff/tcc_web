from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Demandas, Ofertas, Servicos
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Reset


class DemandasForm(forms.ModelForm):

	class Meta:
		model = Demandas
		fields = ('titulo_demanda', 'descricao_demanda', 'categoria', 'imagem_demanda', 'requisitos_demanda', 'anexo_demanda','usuario_demanda')
		widgets = {'usuario_demanda': forms.TextInput(attrs={'type': 'hidden',})}
		widgets = {'descricao_demanda': forms.Textarea(attrs={'rows': '4'})}

	def __init__(self, *args, **kwargs):
		super(DemandasForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
        	Row(
           		Column('titulo_demanda', css_class='form-group col-md-6 mb-0'),
           		Column('categoria', css_class='form-group col-md-6 mb-0'),
           		css_class='form-row'
        	),
        	Row(
           		Column('descricao_demanda', css_class='form-group col-md-8'),
           		Column('imagem_demanda', css_class='form-group col-md-3'),
        	),
        	Row(
           		Column('requisitos_demanda', css_class='form-group col-md-8'),
           		Column('anexo_demanda', css_class='form-group col-md-3'),
        	),
        )
		self.helper.add_input(Submit('submit', 'Cadastrar', css_class='mdl-button mdl-js-button mdl-button--raised mdl-button--colored mdl-js-ripple-effect'))
		self.helper.add_input(Reset('reset', 'Limpar', css_class='mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent'))



class OfertasForm(forms.ModelForm):
	class Meta:
		model = Ofertas
		fields = ('titulo_ofertas', 'descricao_ofertas', 'imagem_oferta', 'usuario_oferta')
		widgets = {'usuario_oferta': forms.TextInput(attrs={'type': 'hidden',})}
		widgets = {'descricao_ofertas': forms.Textarea(attrs={'rows': '4'})}

	def __init__(self, *args, **kwargs):
		super(OfertasForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_method = 'post'
		self.helper.layout = Layout(
        	Row(
           		Column('titulo_ofertas', css_class='form-group col-md-8 mb-0'),
           		Column('imagem_oferta', css_class='form-group col-md-4 mb-0'),
           		css_class='form-row'
        	),
        	Row(
           		Column('descricao_ofertas', css_class='form-group col-md-10'),
        	),
        )
		self.helper.add_input(Submit('submit', 'Cadastrar', css_class='mdl-button mdl-js-button mdl-button--raised mdl-button--colored mdl-js-ripple-effect'))
		self.helper.add_input(Reset('reset', 'Limpar', css_class='mdl-button mdl-js-button mdl-button--raised mdl-js-ripple-effect mdl-button--accent'))


