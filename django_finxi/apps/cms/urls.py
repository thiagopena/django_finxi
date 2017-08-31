# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name = 'cms'
urlpatterns = [
    url(r'^$', views.UserFormView.as_view(), name='loginview'),
    url(r'^logout/$', views.UserLogoutView.as_view(), name='logoutview'),
    url(r'^index/$', views.CmsIndexView.as_view(), name='adminindexview'),
]
