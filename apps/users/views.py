import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login # authenticate用来用户验证,login用来登录
from django.contrib.auth.backends import ModelBackend # 认证方法的类
from django.db.models import Q # 用来查并集
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password # 注册密码
from django.http import HttpResponse # 指明返回给用户的是什么类型的数据

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from utlis.email_send import send_register_email
from utlis.mixin_utils import LoginRequireMixin


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
                if user.is_active:
                    login(request, user)  # 登录
                    return render(request, "index.html")
                else:
                    return render(request, 'login.html', {"msg": "请通过邮箱激活该账号!"})
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
            if UserProfile.objects.filter(username=email):
                return render(request, 'register.html', {'msg':'该用户已存在！', 'register_form': register_form})
            password = request.POST.get('password', '')
            user_profile = UserProfile()
            user_profile.username = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(email, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', locals())


class ActiveUserVIew(View):
    def get(self, request, active_code):
        try:
            code = EmailVerifyRecord.objects.get(code=active_code)
            email = code.email
            user = UserProfile.objects.get(username=email)
            user.is_active = True
            user.save()
            code.delete()
            return render(request, 'login.html')
        except:
            return render(request, 'active_fail.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', locals())

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            try:
                UserProfile.objects.get(username=email)
                send_register_email(email, 'forget')
                return render(request, 'send_success.html')
            except:
                return render(request, 'forgetpwd.html', {'forget_form': forget_form, 'msg':'没有此用户！'})
        else:
            return render(request, 'forgetpwd.html', locals())


class ResetVIew(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html',{'email':email})
        else:
            return render(request, 'active_fail.html')


class ModifyPwdView(View):
    """
    修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():      # 这里有漏洞，只要能进到这个修改密码页面，可以修改任意用户的密码
            pwd1 = request.POST.get('password1', '')    #这里要做，active_code和邮箱匹配的校验
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': "密码不一致！"})
            user = UserProfile.objects.get(username=email)
            user.password = make_password(pwd2)
            user.save()
            #EmailVerifyRecord.objects.get(email=email).delete() # 设置完之后，删除code
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html',
                          {'email': email, 'modify_form': modify_form})

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


class UserinfoView(LoginRequireMixin, View):
    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})


class UploadImageView(LoginRequireMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        # image_form = UploadImageForm(request.POST, request.FILES)   # 上传的文件都会在FILES内
        # if image_form.is_valid():
        #     image = image_form.cleaned_data['image']    # form 验证通过的数据都会在cleaned_data内
        #     request.user.image = image
        #     request.user.save()
        #     return HttpResponse('{"status":"success"}',
        #                         content_type='application/json')

        image_form = UploadImageForm(request.POST,
                                     request.FILES, # 上传的文件都会在FILES内
                                     instance=request.user)  # instance ，可以直接保存form
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}',
                                content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}',
                                content_type='application/json')


class UpdatePwdView(LoginRequireMixin,View):
    """
    个人中心修改用户密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail", "msg":"密码不一致"}',
                                    content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success"}',
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors),
                                content_type='application/json')