import re

from django import forms
from django.contrib.auth.hashers import check_password

from user.models import User


class RegisterForm(forms.Form):

    user_name = forms.CharField(max_length=20, min_length=5, required=True, error_messages={
        'required': '用户名必填',
        'max_length': '用户名不能超过20字符',
        'min_length': '用户名不能少于5字符'
    })
    pwd = forms.CharField(max_length=20, min_length=8, required=True, error_messages={
        'required': '密码必填',
        'max_length': '密码不能超过20字符',
        'min_length': '密码不能少于8字符'
    })
    cpwd = forms.CharField(max_length=20, min_length=8, required=True, error_messages={
        'required': '密码必填',
        'max_length': '密码不能超过20字符',
        'min_length': '密码不能少于8字符'
    })
    email = forms.CharField(required=True, error_messages={
        'required': '邮箱必填'
    })
    allow = forms.BooleanField(required=True, error_messages={
        'required': '须同意协议才能注册'
    })

    def clean(self):
        # 校验注册账号是否已存在
        username = self.cleaned_data.get('user_name')
        user = User.objects.filter(username=username).first()
        if user:
            raise forms.ValidationError('该账号已存在，请重新注册')
        # 校验密码
        pwd = self.cleaned_data.get('pwd')
        cpwd = self.cleaned_data.get('cpwd')
        if pwd != cpwd:
            raise forms.ValidationError({'cpwd': '两次密码不一致'})
        # 校验邮箱
        email_reg = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'
        email = self.cleaned_data.get('email')
        if email:
            if not re.match(email_reg, email):
                raise forms.ValidationError('邮箱格式错误')

        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20, min_length=5, required=True, error_messages={
        'required': '用户名必填',
        'max_length': '用户名不能超过20字符',
        'min_length': '用户名不能少于5字符'
    })
    pwd = forms.CharField(max_length=20, min_length=8, required=True, error_messages={
        'required': '密码必填',
        'max_length': '密码不能超过20字符',
        'min_length': '密码不能少于8字符'
    })

    def clean(self):
        # 校验用户名是否已注册
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if not user:
            raise forms.ValidationError({'username': '该账号没有被注册'})
        password = self.cleaned_data['pwd']
        if not check_password(password, user.password):
            raise forms.ValidationError({'pwd': '密码错误'})
        return self.cleaned_data


class AddressForm(forms.Form):
    username = forms.CharField(max_length=5, required=True,
                               error_messages={
                                   'required': '收件人必填',
                                   'max_length': '收件人姓名不能超过5个字符'
                               })
    address = forms.CharField(required=True,
                              error_messages={
                                  'required': '收货地址必填'
                              })
    postcode = forms.CharField(required=True,
                               error_messages={
                                  'required': '邮编必填'
                              })
    mobile = forms.CharField(required=True,
                             error_messages={
                                  'required': '手机号必填'
                              })

    def clean(self):
        pass
