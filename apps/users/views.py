from django.shortcuts import render
from django.contrib.auth import authenticate, login # authenticate用来用户验证,login用来登录
from django.contrib.auth.backends import ModelBackend # 认证方法的类
from django.db.models import Q # 用来查并集
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password # 注册密码

from .models import UserProfile
from .forms import LoginForm, RegisterForm
from utlis.email_send import send_register_email

# Create your views here.
class CustomBackend(ModelBackend): #重写认证方法
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)) # |或  ,和
            if user.check_password(password):   # 不能直接从库里验证密码，库密码被加密了的
                return user
        except Exception as e:
            return None

class LoginView(View):  # 用类来写view，代替之前的函数，这个会更灵活
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST) # request.POST 里面的字典参数会自动去校验
        if login_form.is_valid(): # 判断是否符合，设置的form规则
            username = request.POST.get('username', '')  # 获取username的值，没有就""
            password = request.POST.get('password', '')
            user = authenticate(username=username,
                                password=password)  # 无效就返回None，有效就返回这个用户
            if user is not None:
                login(request, user)  # 登录
                return render(request, "index.html")
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误!"})
        else:
            return render(request, 'login.html', {"login_form": login_form})

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.email = email
            user_profile.password = make_password(password)
            user_profile.save()
            send_register_email(email, 'register')
        else:
            return render(request, 'register.html', locals())


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '') # 获取username的值，没有就""
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password) # 无效就返回None，有效就返回这个用户
        if user is not None:
            login(request, user)    # 登录
            return render(request, "index.html")
        else:
            return render(request, 'login.html', {"msg": "用户名或密码错误!"})

    elif request.method == 'GET':
        return render(request, 'login.html', {})