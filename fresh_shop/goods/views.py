from django.shortcuts import render

from goods.models import GoodsCategory, Goods


def index(req):
    if req.method == 'GET':
        # 组装结果的对象：包含分类和该分类的前四个商品信息
        categorys = GoodsCategory.objects.all()
        result = []
        for category in categorys:
            show_goods = category.goods_set.all()[:4]
            data = [category, show_goods]
            result.append(data)
        category_type = GoodsCategory.CATEGORY_TYPE
        return render(req, 'index.html', {'result': result, 'category_type': category_type})


def detail(req, id):
    if req.method == 'GET':
        good = Goods.objects.filter(pk=id).first()
        category_id = good.category_id
        categorys = GoodsCategory.objects.filter(pk=category_id).first()
        category_name = categorys.CATEGORY_TYPE[category_id-1][1]
        return render(req, 'detail.html', {'good': good, 'category_name': category_name})


def my_list(req, id):
    if req.method == 'GET':
        category = GoodsCategory.objects.filter(pk=id).first()
        all_goods = category.goods_set.all()
        goods = []
        for i in all_goods:
            goods.append(i)
        goods = goods[0:2]
        category_type = category.CATEGORY_TYPE
        cate = category_type[id-1]
        return render(req, 'list.html', {'category': category,
                                         'category_type': category_type,
                                         'cate': cate,
                                         'goods': goods})
