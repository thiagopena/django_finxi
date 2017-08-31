# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from django_finxi.apps.main.models import Imovel


class ImovelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImovelForm, self).__init__(*args, **kwargs)
        self.fields['valor'].localize = True

    class Meta:
        model = Imovel
        fields = ('tipo', 'descricao_curta', 'descricao', 'imobiliaria', 'valor', 'area', 'rua',
                  'numero', 'bairro', 'regiao', 'complemento', 'pais', 'municipio', 'cep', 'uf', 'foto',)

        widgets = {
            'descricao_curta': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'imobiliaria': forms.TextInput(attrs={'class': 'form-control'}),
            'foto': forms. FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'valor': forms.TextInput(attrs={'class': 'form-control decimal-mask'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'regiao': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'uf': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'descricao_curta': _('Descrição curta'),
            'descricao': _('Descrição'),
            'imobiliaria': _('Imobiliária'),
            'tipo': _('Tipo'),
            'foto': _('Foto'),
            'valor': _('Valor de venda'),
            'area': _('Área'),
            'rua': _('Rua'),
            'numero': _('Número'),
            'bairro': _('Bairro'),
            'regiao': _('Região'),
            'complemento': _('Complemento'),
            'pais': _('País'),
            'municipio': _('Município'),
            'cep': _('CEP'),
            'uf': _('Estado'),
        }
