import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User


class IsLoginMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # path = request.path
        # if path not in ['/user/register/', '/user/login/', '/cart/cart/', '/goods/detail/', '/cart/add_cart/']:
        #     try:
        #         # 登录校验
        #         user_id = request.session.get('user_id')
        #         if user_id:
        #             user = User.objects.get(pk=user_id)
        #             # 给request.user属性赋值，赋为当前登录系统的用户
        #             request.user = user
        #     except Exception as e:
        #         if path in ['/goods/index/']:
        #             # 跳过之后的代码，直接访问路由对应的视图函数
        #             return None
        #         return HttpResponseRedirect(reverse('user:login'))
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.get(pk=user_id)
            # 给request.user属性赋值，赋为当前登录系统的用户
            request.user = user
        path = request.path
        # if path == '/':
        #     return None
        not_need_check = ['^/$', '/user/register/', '/user/login/', '/goods/index/', '/goods/detail/.*', '/cart/.*/']
        for check_path in not_need_check:
            if re.match(check_path, path):
                return None
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))


class SessionToDbMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # 同步session与数据库中的商品信息
        # 1.判断用户是否登录，登录才进行数据同步
        user_id = request.session.get('user_id')
        if user_id:
            # 2.同步
            session_goods = request.session.get('goods')
            # 2.1 判断session中的商品是否存在于数据库中，如果存在就更新
            # 2.2 如果不存在，就创建
            if session_goods:
                for se_goods in session_goods:
                    cart = ShoppingCart.objects.filter(user_id=user_id, goods_id=se_goods[0]).first()
                    if cart:
                        # 商品存在，更新数据库的购物车中的商品信息
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 商品不存在，创建数据库的购物车中的商品信息
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=se_goods[0],
                                                    nums=se_goods[1],
                                                    is_select=se_goods[2])

            # 2.3 同步数据库的数据到session中
            db_carts = ShoppingCart.objects.filter(user_id=user_id)
            if db_carts:
                # 生成式
                new_session_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in db_carts]
                request.session['goods'] = new_session_goods
                # result = []
                # for cart in db_carts:
                #     data = [cart.goods_id, cart.nums, cart.is_select]
                #     result.append(data)
        return response


class HistoricalLogMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        # 组装一个session_history = [[history1], [history2]]
        path = request.path
        pass_path = '/goods/detail/.*/'
        if re.match(pass_path, path):
            re_check = '\d+'
            goods_id = int(re.findall(re_check, path)[-1])
            session_history = request.session.get('session_history', [])
            if session_history:
                for se_history in session_history:
                    if se_history == goods_id:
                        session_history.remove(goods_id)
                        session_history.append(goods_id)
                        return response
                session_history.append(goods_id)
            else:
                session_history.append(goods_id)
                request.session['session_history'] = session_history

        return response
