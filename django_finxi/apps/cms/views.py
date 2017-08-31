# -*- coding: utf-8 -*-

from django.views.generic import View
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from django_finxi.apps.cms.forms import UserLoginForm
from django_finxi.apps.main.models import Imovel


class UserFormView(View):
    form_class = UserLoginForm
    template_name = 'cms/login.html'

    def get(self, request):
        form = self.form_class(None)

        if request.user.is_authenticated():
            return redirect('cms:adminindexview')
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
        if request.POST and form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = form.authenticate_user(username=username, password=password)
            if user:
                login(request, user)
                return redirect('cms:adminindexview')

        return render(request, self.template_name, {'form': form})


class UserLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('main:indexview')


class CmsIndexView(ListView):
    model = Imovel
    template_name = 'cms/cms_index.html'
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
