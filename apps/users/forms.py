# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/21 0:29'
from django import forms
from captcha.fields import CaptchaField # 做验证码

class LoginForm(forms.Form):
    username = forms.CharField(required=True) # required 必须填写
    password = forms.CharField(required=True, min_length=3) # username 这个名字，必须和html表单的name一致

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=3)
    captcha = CaptchaField(required=True, error_messages={"invalid": "验证码错误"}) # 验证码