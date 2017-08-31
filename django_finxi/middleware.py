# -*- coding: utf-8 -*-

import re
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from .settings import LOGIN_REQUIRED


class LoginRequiredMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None, *args, **kwargs):
        self.required_urls = tuple(re.compile(url) for url in LOGIN_REQUIRED)
        self.get_response = get_response

        return super(LoginRequiredMiddleware, self).__init__(get_response, *args, **kwargs)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated():
            for url in self.required_urls:
                if url.match(request.path):
                    return redirect('cms:loginview')
            return None

        return None