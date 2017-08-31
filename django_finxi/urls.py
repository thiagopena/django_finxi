# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from django.conf.urls.static import static
from .settings import DEBUG, MEDIA_ROOT, MEDIA_URL


urlpatterns = [
    url(r'^admin/', include('django_finxi.apps.cms.urls')),
    url(r'^', include('django_finxi.apps.main.urls')),
]

if DEBUG is True and MEDIA_URL == 'media/':
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)