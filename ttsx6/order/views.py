<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
# coding=utf-8
from datetime import datetime
from django.shortcuts import render, redirect
from django.db import transaction
from models import *
from cart.models import CartInfo
# Create your views here.
'''
1、创建订单主表
2、接收所有的购物车请求
3、查询到请求的购物车信息
4、逐个判断库存
5、如果库存足够
    5.1、创建订单详单
    5.2、改变库存
    5.3、计算总金额
    5.4、删除购物车数据
6、如果库存不够，则放弃之前的保存，转到购物车
'''

# 引入事务，详细查看文档（课件第一页有链接），此举为了手动提交事务
@transaction.atomic
# def do_order(request):
#     isok = True
#     sid = transaction.savepoint()  # 设置保存点，在commit，rollback之前所有的数据更改都不会生效，而是放到临时表中
#     try:
#         uid = request.session.get('uid')
#         # 1创建主单
#         now_str = datetime.now().strftime('%Y%m%d%H%M%S')  # 提交订单的时间 （把日期转换成时间）不知道去百度查
#         main = OrderMain()
#         main.order_id = '%s%d' % (now_str, uid)
#         main.user_id = uid
#         main.save()
#         #2
#         cart_ids = request.POST.get('cart_ids').split(',')
#         #3
#         cart_list = CartInfo.objects.filter(id__in=cart_ids)
#         total = 0
#         for cart in cart_list:  #4
#             if cart.count <= cart.goods.gkucun: #5
#                 #5.1
#                 detail = OrderDetail()
#                 detail.order = main  # 当前的详单是属于这个主单的
#                 detail.goods = cart.goods # 当前购物车的商品就是详单中的商品
#                 detail.count = cart.count
#                 detail.price = cart.price
#                 detail.save()
#                 #5.2
#                 cart.goods.kucun -= cart.count
#                 cart.goods.save()
#                 # 5.3
#                 total += cart.count*cart.goods.gprice
#                 main.total = total
#                 main.save()
#                 #5.4
#                 cart.delete()
#             else:#6
#                 isok = False
#                 transaction.savepoint_rollback(sid)  # 回滚事务
#                 break
#         if isok:
#             transaction.savepoint_commit(sid)
#     except:
#         transaction.savepoint_rollback(sid)  # 回滚事务
#         isok = False
#     if isok:
#         return redirect('/user/order/')
#     else:
#         return redirect('/cart/')
def do_order(request):
    isok=True
    sid=transaction.savepoint()
    try:
        uid=request.session.get('uid')
        #1
        now_str=datetime.now().strftime('%Y%m%d%H%M%S')
        main=OrderMain()
        main.order_id='%s%d'%(now_str,uid)
        main.user_id=uid
        main.save()
        #2
        cart_ids=request.POST.get('cart_ids').split(',')#'4,6,5'
        #3
        cart_list=CartInfo.objects.filter(id__in=cart_ids)
        total=0
        for cart in cart_list:#4
            if cart.count<=cart.goods.gkucun:#5
                #5.1
                detail=OrderDetail()
                detail.order=main
                detail.goods=cart.goods
                detail.count=cart.count
                detail.price=cart.goods.gprice
                detail.save()
                #5.2
                cart.goods.gkucun-=cart.count
                cart.goods.save()
                #5.3
                total+=cart.count*cart.goods.gprice
                main.total=total
                main.save()
                #5.4
                cart.delete()
            else:#6
                isok=False
                transaction.savepoint_rollback(sid)
                break
        if isok:
            transaction.savepoint_commit(sid)
    except:
        transaction.savepoint_rollback(sid)
        isok=False

    if isok:
        return redirect('/user/order/')
    else:
        return redirect('/cart/')
>>>>>>> itcast
