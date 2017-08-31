# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='indexview'),
    url(r'^imovel/cadastrar/$', views.AdicionarImovelView.as_view(),
        name='adicionaimovelview'),
    url(r'^imovel/detalhar/(?P<pk>[0-9]+)/$',
        views.DetalharImovelView.as_view(), name='detalharimovelview'),
    url(r'^imovel/editar/(?P<pk>[0-9]+)/$',
        views.EditarImovelView.as_view(), name='editarimovelview'),
    url(r'^imovel/buscar/$', views.BuscaImovelView.as_view(), name='buscarimovelview'),
    url(r'buscaautocomplete/$', views.BuscaAutocompleteView.as_view(),
        name='buscaautocompleteview'),
]
