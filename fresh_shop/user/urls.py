from django.urls import path

from user import views


urlpatterns = [
    # 注册
    path('register/', views.register, name='register'),
    # 登录
    path('login/', views.login, name='login'),
    # 退出
    path('logout/', views.logout, name='logout'),
    # 收货地址
    path('user_center_site/', views.user_center_site, name='user_center_site'),
    # 用户中心
    path('user_info/', views.user_info, name='user_info'),
    # 清空历史记录
    path('del_history/', views.del_history, name='del_history'),
]