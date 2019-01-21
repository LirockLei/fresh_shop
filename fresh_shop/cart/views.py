from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from goods.models import Goods


def cart(req):
    if req.method == 'GET':
        session_goods = req.session.get('goods')
        # 组装返回数据的格式：[objects1, objects2...]
        # objects ====> [Goods object, is_select, num, total_price]
        result = []
        if session_goods:
            for se_goods in session_goods:
                # se_goods的格式为[goods_id, num, is_select]
                goods = Goods.objects.filter(pk=se_goods[0]).first()
                total_price = goods.shop_price * se_goods[1]
                data = [goods, se_goods[1], se_goods[2], total_price]
                result.append(data)
        return render(req, 'cart.html', {'result': result})


def add_cart(req):
    if req.method == 'POST':
        # 接收商品id值和商品数量num
        # 组装存储的商品格式：[goods_id, num, is_select]
        # 组装多个商品格式：[[goods_id, num, is_select], [goods_id, num, is_select]]
        goods_id = int(req.POST.get('goods_id'))
        goods_num = int(req.POST.get('goods_num'))
        goods_list = [goods_id, goods_num, 1]

        session_goods = req.session.get('goods')
        if session_goods:
            # 1.添加购物车中已有的商品，则修改
            flag = True
            for se_goods in session_goods:
                if se_goods[0] == goods_id:
                    se_goods[1] += goods_num
                    flag = False
            if flag:
                # 2.添加的商品不存在于购物车中，则新增
                session_goods.append(goods_list)
            req.session['goods'] = session_goods
            count = len(session_goods)
        else:
            # 第一次添加购物车，需要组装商品格式为[[goods_id, num, is_select]]
            req.session['goods'] = [goods_list]
            count = 1
        return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


def cart_num(req):
    if req.method == 'GET':
        session_goods = req.session.get('goods')
        count = len(session_goods) if session_goods else 0
    return JsonResponse({'code': 200, 'msg': '请求成功', 'count': count})


def all_cart_price(req):
    if req.method == 'GET':
        session_goods = req.session.get('goods')
        # 总的商品件数
        all_total = len(session_goods) if session_goods else 0
        all_price = 0
        is_select_num = 0
        for se_goods in session_goods:
            # se_goods的格式为[goods_id, num, is_select]
            if se_goods[2]:
                goods = Goods.objects.filter(pk=se_goods[0]).first()
                all_price += goods.shop_price * se_goods[1]
                is_select_num += 1
        return JsonResponse({'code': 200, 'msg': '请求成功', 'all_total': all_total, 'all_price': all_price,
                             'is_select_num': is_select_num})


def change_cart(req):
    if req.method == 'POST':
        # 修改商品数量和选择状态
        # 修改session中商品信息结构为[goods_id, num, is_select]

        # 1.获取商品id值和数量/选择状态
        goods_id = int(req.POST.get('goods_id'))
        goods_num = req.POST.get('goods_num')
        good_select = req.POST.get('goods_select')
        # 修改
        session_goods = req.session.get('goods')
        for se_goods in session_goods:
            if se_goods[0] == goods_id:
                se_goods[1] = int(goods_num) if goods_num else se_goods[1]
                se_goods[2] = int(good_select) if good_select else se_goods[2]
        req.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def del_goods(req):
    if req.method == 'POST':
        goods_id = int(req.POST.get('goods_id'))
        session_goods = req.session.get('goods')
        for se_goods in session_goods:
            if se_goods[0] == goods_id:
                session_goods.remove(se_goods)
                break
        req.session['goods'] = session_goods
        # 在登录状态下，删除数据库的购物车中的商品信息
        user_id = req.session.get('user_id')
        if user_id:
            ShoppingCart.objects.filter(goods_id=goods_id, user_id=user_id).delete()
        return JsonResponse({'code': 200, 'msg': '请求成功'})