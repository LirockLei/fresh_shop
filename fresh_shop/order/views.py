from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render

from cart.models import ShoppingCart
from fresh_shop.settings import ORDER_NUMBER
from order.models import OrderInfo, OrderGoods
from user.models import UserAddress
from utils.functions import make_order_sn


def place_order(req):
    if req.method == 'GET':
        # 获取当前登录系统的用户
        user = req.user
        user_id = req.session.get('user_id')
        carts = ShoppingCart.objects.filter(user=user, is_select=True).all()
        carts_num = len(carts)
        # 计算小计和总价
        total_price = 0
        for cart in carts:
            # 小计金额
            price = cart.goods.shop_price * cart.nums
            cart.gooods_price = price
            # 总金额
            total_price += price
        # 获取当前登录系统的用户的收货地址信息
        address = UserAddress.objects.filter(user_id=user_id).all()
        return render(req, 'place_order.html', {'carts': carts,
                                                'total_price': total_price,
                                                'carts_num': carts_num,
                                                'address': address
                                                })


def order(req):
    if req.method == 'POST':
        # 1.获取收货地址的id值
        ad_id = req.POST.get('ad_id')
        # 2.创建订单
        user_id = req.session.get('user_id')
        # 获取订单编号
        order_sn = make_order_sn()
        # 计算订单金额
        shop_cart = ShoppingCart.objects.filter(user_id=user_id, is_select=True)
        order_mount = 0
        for cart in shop_cart:
            order_mount += cart.goods.shop_price * cart.nums
        # 收货信息
        user_address = UserAddress.objects.filter(pk=ad_id).first()
        order = OrderInfo.objects.create(user_id=user_id,
                                         order_sn=order_sn,
                                         order_mount=order_mount,
                                         address=user_address.address,
                                         signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile)
        # 3.创建订单详情
        for cart in shop_cart:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums)
        # 4.删除购物车中的内容
        # 删除数据库中的购物车信息
        shop_cart.delete()
        # 删除session中的购物车信息
        session_goods = req.session.get('goods')
        for se_goods in session_goods[:]:
            # se_goods结构[goods_id, nums, is_select]
            if se_goods[2]:
                session_goods.remove(se_goods)
        req.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})


def user_order(req):
    if req.method == 'GET':
        page = int(req.GET.get('page', 1))
        # 获取登录系统用户的id值
        user_id = req.session.get('user_id')
        # 查询当前用户产生的订单信息
        orders = OrderInfo.objects.filter(user_id=user_id)
        status = OrderInfo.ORDER_STATUS
        # 分页
        pg = Paginator(orders, ORDER_NUMBER)
        orders = pg.page(page)
        activate = 'order'
        return render(req, 'user_center_order.html', {'orders': orders, 'status': status, 'activate': activate})
