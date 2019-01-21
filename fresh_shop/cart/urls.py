from django.urls import path

from cart import views

urlpatterns = [
    # 购物车
    path('cart/', views.cart, name='cart'),
    # 加入购物车
    path('add_cart/', views.add_cart, name='add_cart'),
    # 购物车数量刷新
    path('cart_num/', views.cart_num, name='cart_num'),
    # 购物车计算价格
    path('all_cart_price/', views.all_cart_price, name='all_cart_price'),
    # 修改购物车中的数量和状态
    path('change_cart/', views.change_cart, name='change_cart'),
    # 删除购物车中的商品
    path('del_goods/', views.del_goods, name='del_goods'),
]