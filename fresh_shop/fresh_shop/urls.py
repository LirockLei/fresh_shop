"""fresh_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.staticfiles.urls import static
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve

from fresh_shop import settings
from fresh_shop.settings import MEDIA_URL, MEDIA_ROOT
from goods import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 导入应用
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('goods/', include(('goods.urls', 'goods'), namespace='goods')),
    path('order/', include(('order.urls', 'order'), namespace='order')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    # 首页路径
    path('', views.index),

    # path(r'^static/(?P<path>.*)$', serve, {"document_root": settings.STATICFILES_DIRS[0]}),
    #
    # path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    #
    # path(r'^$', views.index)
]

urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)