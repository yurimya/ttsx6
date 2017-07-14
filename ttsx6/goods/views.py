# coding=utf-8
from django.shortcuts import render
from haystack.generic_views import SearchView

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


def goods_list(request, tid, pindex, orderby):
    try:
        t1 = TypeInfo.objects.get(pk=int(tid))
        new_list = t1.goodsinfo_set.order_by('-id')[0:2]
        # 指定排序规则
        orderby_str = '-id'
        desc = '1'
        if orderby == '2':
            # 指定排序规则，升还是降
            desc = request.GET.get('desc', '1')
            if desc == '1':
                orderby_str = '-gprice'

            else:
                orderby_str = 'gprice'

        elif orderby == '3':
            orderby_str = '-gclick'
        # 查询：当前分类的所有商品，按每页15个来显示
        glist = t1.goodsinfo_set.order_by(orderby_str)
        paginator = Paginator(glist, 5)

        pindex1 = int(pindex)
        if pindex1<1:
            pindex1=1
        elif pindex1>paginator.num_pages: # 总页数
            pindex1=paginator.num_pages
        page=paginator.page(pindex1)
        context = {'title': '商品列表页', 'car_shop': '1','t1':t1, 'new_list': new_list, 'page': page, 'orderby': orderby, 'desc':desc}
        return render(request, 'goods/list.html', context)
    except:
        return render(request, '404.html')


def detail(request, id):   # 当点详细商品信息时，保存cookie，所以cookie代码在这写
    try:
        goods = GoodsInfo.objects.get(pk=int(id))
        goods.gclick += 1
        goods.save()
        new_list = goods.gtype.goodsinfo_set.order_by('-id')[0:2] # 详细页左边的广告
        context = {'title': '商品详细页', 'car_shop': '1', 'goods': goods, 'new_list': new_list}
        response = render(request, 'goods/detail.html', context)
        # 保存最近浏览
        # 先读取已存的，再进行拼接，最后输出
        # split()：拆分字符串。通过指定分隔符对字符串进行切片，并返回分割后的字符串列表（list）
        gids = request.COOKIES.get('goods_ids', '').split(',')
        # 判断这个编号是否存在 ，如果存在 则删除，然后再加到最前面
        if id in gids:
            gids.remove(id)
        gids.insert(0,id)  # 把最新浏览的放到最前面显示
        # 如果超过五个，则删除最后一个
        if len(gids) > 6:
            gids.pop()
                                        # 转换成字符串     过期时间：秒为单位的一个数字
        response.set_cookie('goods_ids', ','.join(gids), max_age=60*60*24*7)

        return response
    except:
        return render(request, '404.html')


class MySearchView(SearchView):
    def get_context_data(self, *args, **kwargs):
        context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context['car_shop']='1'
        page_range=[]
        page=context.get('page_obj')
        if page.paginator.num_pages<5:
            page_range=page.paginator.page_range
        elif page.number<=2:#第1、2页
            page_range=range(1,6)
        elif page.number>=page.paginator.num_pages-1:#倒数第1、2页 6 7 8 9 10
            page_range=range(page.paginator.num_pages-4,page.paginator.num_pages+1)
        else:# 3 4 5 6 7
            page_range=range(page.number-2,page.number+3)
        context['page_range']=page_range
        return context