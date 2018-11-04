# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/11/3 11:27'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequireMixin():
    # 要求用户登录，用户如果未登录调整登录页面
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)