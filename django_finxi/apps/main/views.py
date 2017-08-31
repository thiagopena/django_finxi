# -*- coding: utf-8 -*-

from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.db.models import Q
from django.http import HttpResponse

from django_finxi.apps.main.forms import ImovelForm
from django_finxi.apps.main.models import Imovel

import json


class IndexView(ListView):
    model = Imovel
    template_name = 'main/index.html'
    context_object_name = 'all_imoveis'
    success_url = reverse_lazy('main:indexview')

    def get_queryset(self):
        all_imoveis = Imovel.objects.all()
        return all_imoveis

    def post(self, request, *args, **kwargs):
        if 'deletar_imovel' in request.POST:
            instance = self.model.objects.get(
                id=request.POST['deletar_imovel'])
            instance.delete()
        return redirect(self.success_url)


class BuscaImovelView(ListView):
    model = Imovel
    template_name = 'main/search_imovel.html'
    context_object_name = 'imoveis_encontrados'
    success_url = reverse_lazy('main:indexview')

    def get_queryset(self):
        tipo_imovel = self.request.GET.get('tipo_imovel')
        endereco_imovel = self.request.GET.get('endereco_imovel')
        if tipo_imovel == 'todos':
            tipo_imovel = ''
        elif tipo_imovel == 'residencial':
            tipo_imovel = 'R'
        elif tipo_imovel == 'comercial':
            tipo_imovel = 'C'
        elif tipo_imovel == 'rural':
            tipo_imovel = 'U'
        elif tipo_imovel == 'outros':
            tipo_imovel = 'O'

        if endereco_imovel and tipo_imovel:
            imoveis_encontrados = Imovel.objects.filter(Q(tipo=tipo_imovel) & (Q(bairro__icontains=endereco_imovel) | Q(
                municipio__icontains=endereco_imovel) | Q(regiao__icontains=endereco_imovel)))
        elif endereco_imovel:
            imoveis_encontrados = Imovel.objects.filter(Q(bairro__icontains=endereco_imovel) | Q(
                municipio__icontains=endereco_imovel) | Q(regiao__icontains=endereco_imovel))
        else:
            imoveis_encontrados = None

        return imoveis_encontrados


class BuscaAutocompleteView(View):

    def post(self, request, *args, **kwargs):
        endereco = request.POST['enderecoBusca']
        data = {}
        bairros = []
        cidades = []
        regioes = []

        imoveis_encontrados = Imovel.objects.filter(bairro__icontains=endereco)
        for im in imoveis_encontrados:
            bairros.append(im.bairro.upper())

        imoveis_encontrados = Imovel.objects.filter(
            municipio__icontains=endereco)
        for im in imoveis_encontrados:
            cidades.append(im.municipio.upper())

        imoveis_encontrados = Imovel.objects.filter(regiao__icontains=endereco)
        for im in imoveis_encontrados:
            regioes.append(im.regiao.upper())

        data['bairros'] = bairros
        data['cidades'] = cidades
        data['regioes'] = regioes
        return HttpResponse(json.dumps(data), content_type='application/json')


class AdicionarImovelView(CreateView):
    form_class = ImovelForm
    template_name = "main/add_imovel.html"
    success_url = reverse_lazy('cms:adminindexview')
    success_message = "Imóvel adicionado com sucesso."

    def post(self, request, *args, **kwargs):
        req_post = request.POST.copy()
        if 'valor' in req_post:
            req_post['valor'] = req_post['valor'].replace('.', '')
        request.POST = req_post
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.object = form.save(commit=False)
            if 'foto' in request.FILES:
                self.object.foto = request.FILES['foto']
            self.object.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class DetalharImovelView(DetailView):
    template_name = "main/det_imovel.html"
    queryset = Imovel.objects.all()

    def get_context_data(self, **kwargs):
        context = super(DetalharImovelView, self).get_context_data(**kwargs)
        info_gerais = {}
        localizacao = {}
        info_gerais['Á partir de'] = self.object.valor
        info_gerais['Área'] = self.object.area
        info_gerais['Região'] = self.object.regiao
        info_gerais['Imobiliária'] = self.object.imobiliaria
        localizacao['País'] = self.object.pais
        localizacao['Estado'] = self.object.uf
        localizacao['CEP'] = self.object.cep
        localizacao['Rua'] = self.object.rua
        localizacao['Bairro'] = self.object.bairro
        localizacao['Número'] = self.object.numero
        localizacao['Complemento'] = self.object.complemento
        localizacao['Município'] = self.object.municipio
        context['info_gerais'] = info_gerais
        context['localizacao'] = localizacao
        return context


class EditarImovelView(UpdateView):
    form_class = ImovelForm
    model = Imovel
    template_name = "main/edit_imovel.html"
    success_url = reverse_lazy('cms:adminindexview')
    success_message = "Imóvel editado com sucesso."

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        req_post = request.POST.copy()
        if 'valor' in req_post:
            req_post['valor'] = req_post['valor'].replace('.', '')
        request.POST = req_post
        form = form_class(request.POST, request.FILES, instance=self.object)
        if form.is_valid():
            self.object = form.save(commit=False)
            if 'foto' in request.FILES:
                self.object.foto = request.FILES['foto']
            self.object.save()
            return self.form_valid(form)
        return self.form_invalid(form)
