# coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    goods_list = [] # [{},{},{}]===>{'typeinfo':,'new_list':,'click_list':}
    # 查询分类对象
    # 查询每个分类中最新的4个商品
    # 查询每个对象中最火的4个商品
    type_list = TypeInfo.objects.all() # 获取所有商品分类
    for t1 in type_list:
        nlist = t1.goodsinfo_set.order_by('-id')[0:4]  # 找出相对应的所有食物通过倒序排序，取最新的四个
        clist = t1.goodsinfo_set.order_by('-gclick')[0:4]
        goods_list.append({'t1': t1, 'nlist': nlist, 'clist': clist})
    context = {'title': '首页', 'glist': goods_list, 'car_shop': '1'}
    return render(request, 'goods/index.html', context)


def goods_list(request, tid, pindex):
    try:
        t1 = TypeInfo.objects.get(pk=int(tid))
        new_list = t1.goodsinfo_set.order_by('-id')[0:2]
        # 查询：当前分类的所有商品，按每页15个来显示
        glist = t1.goodsinfo_set.order_by('-id')
        paginator = Paginator(glist, 15)

        pindex1 = int(pindex)
        if pindex1<1:
            pindex1=1
        elif pindex1>paginator.num_pages: # 总页数
            pindex1=paginator.num_pages
        page=paginator.page(pindex1)
        context = {'title': '商品列表页', 'car_shop': '1','t1':t1, 'new_list': new_list, 'page': page}
        return render(request, 'goods/list.html', context)
    except:
        return render(request, '404.html')


def detail(request, id):
    try:
        goods = GoodsInfo.objects.get(pk=int(id))
        goods.gclick += 1
        goods.save()
        new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2] # 详细页左边的广告
        context = {'title': '商品详细页', 'car_shop': '1', 'goods': goods, 'new_list': new_list}
        return render(request, 'goods/detail.html', context)
    except:
        return render(request, '404.html')