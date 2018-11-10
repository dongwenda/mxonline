# -*- coding: utf-8 -*-
__author__ = 'dongwenda'
__date__ = '2018/10/21 15:38'
from random import Random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from MxOnline.settings import DEFAULT_FROM_EMAIL

# 生成随机字符串
def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str

def send_email(email, send_type):
    # 发送之前先保存到数据库，到时候查询链接是否存在
    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机的code放入链接
    if send_type == 'update_mail':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    if send_type == "register":
        email_title = "慕课小站 注册激活链接"
        email_body = "欢迎注册慕课小站:  请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        #使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL, [email])

        # 如果发送成功
        if send_status:
            pass

    elif send_type == "forget":
        email_title = "慕课小站 重置密码链接"
        email_body = "欢迎注册慕课小站:  请点击下面的链接重置你的密码: http://127.0.0.1:8000/reset/{0}".format(
            code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL,
                                [email])

        # 如果发送成功
        if send_status:
            pass

    elif send_type == "update_mail":
        email_title = "慕课小站 修改邮箱链接"
        email_body = "您的邮箱验证码为:{} ".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，从哪里发，接受者list
        send_status = send_mail(email_title, email_body, DEFAULT_FROM_EMAIL,
                                [email])

        # 如果发送成功
        if send_status:
            pass