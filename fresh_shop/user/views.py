from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render

from goods.models import Goods
from user.forms import RegisterForm, LoginForm, AddressForm
from user.models import User, UserAddress


def register(req):
    if req.method == 'GET':
        return render(req, 'register.html')
    else:
        # 使用form表单作校验
        form = RegisterForm(req.POST)
        if form.is_valid():
            # 账号不存在于数据库，两次输入密码一致，邮箱格式正确
            username = form.cleaned_data['user_name']
            password = make_password(form.cleaned_data['pwd'])
            email = form.cleaned_data['email']
            User.objects.create(
                username=username,
                password=password,
                email=email
            )
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # 获取表单验证不通过的错误信息
            errors = form.errors
            return render(req, 'register.html', {'errors': errors})


def login(req):
    if req.method == 'GET':
        return render(req, 'login.html')
    else:
        form = LoginForm(req.POST)
        if form.is_valid():
            # 用户名存在，密码相同，登录成功
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            req.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            errors = form.errors
            return render(req, 'login.html', {'errors': errors})


def logout(req):
    if req.method == 'GET':
        # 删除session中的user_id键值对
        # del req.session['user_id']
        req.session.flush()
        # 删除商品信息
        if req.session.get('goods'):
            del req.session['goods']
        return HttpResponseRedirect(reverse('goods:index'))


def user_center_site(req):
    if req.method == 'GET':
        user_id = req.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        activate = 'site'
        return render(req, 'user_center_site.html', {'user_address': user_address, 'activate': activate})
    else:
        form = AddressForm(req.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            mobile = form.cleaned_data['mobile']
            user_id = req.session.get('user_id')
            UserAddress.objects.create(user_id=user_id,
                                       address=address,
                                       signer_name=username,
                                       signer_mobile=mobile,
                                       signer_postcode=postcode)
            return HttpResponseRedirect(reverse('user:user_center_site'))
        else:
            errors = form.errors
            return render(req, 'user_center_site.html', {'errors': errors})


def user_info(req):
    if req.method == 'GET':
        activate = 'info'
        user_id = req.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        session_history = req.session.get('session_history')
        historical_goods = []
        if session_history:
            session_history = session_history[::-1]
            # if len(session_history) >= 5:
            for goods_id in session_history[:5]:
                if goods_id:
                    goods = Goods.objects.filter(pk=goods_id).first()
                    historical_goods.append(goods)
            # else:
            #     for goods_id in session_history:
            #         if goods_id:
            #             goods = Goods.objects.filter(pk=goods_id).first()
            #             historical_goods.append(goods)
        return render(req, 'user_center_info.html', {'activate': activate,
                                                     'user_address': user_address,
                                                     'historical_goods': historical_goods})


def del_history(req):
    if req.method == 'POST':
        session_history = req.session.get('session_history')
        if session_history:
            session_history = []
            req.session['session_history'] = session_history
    return JsonResponse({'code': 200, 'msg': '删除成功'})
