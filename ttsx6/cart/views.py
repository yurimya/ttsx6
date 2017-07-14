# coding=utf-8
from django.db.models import Sum
from django.shortcuts import render
from django.http import JsonResponse
from models import *
from user.login_decorator import ss
from user.models import UserInfo
# Create your views here.


def add(request):
    try:
        uid = request.session.get('uid')
        gid = int(request.GET.get('gid'))
        count = int(request.GET.get('count', '1'))
        # 先获取一下这个商品有没有买过，买过：就加数量，没买过：创建对象
        carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
        # print request.get_full_path()
        # print carts
        # print carts[0]
        if len(carts) == 1:
            cart = carts[0]
            cart.count += count
            cart.save()
        else:
            cart = CartInfo() # 创建cart对象,这里别忘记要引用models
            cart.user_id = uid # 通过外键可以得到
            cart.goods_id = gid # 通过外键可以得到
            cart.count = count
            cart.save()
        return JsonResponse({'isadd': 1}) # 添加成功
    except:
        return JsonResponse({'isadd': 0}) # 添加失败


def count(request):
    # 查询当前人买了多少商品
    uid = request.session.get('uid')
    # cart_count = CartInfo.objects.filter(user_id=uid).count()  # 显示买了多少种商品
    cart_count = CartInfo.objects.filter(user_id=uid).aggregate(Sum('count')).get('count__sum')  # count__sum 显示共买了多少商品
    if cart_count == None:
        cart_count = 0
    return JsonResponse({'cart_count': cart_count})


@ss # 判断：没登陆就去登陆页面
def index(request):
    uid = request.session.get('uid') # 作用是查看是否登录
    cart_list = CartInfo.objects.filter(user_id=uid) # 通过筛选当前用户的id 获取当前用户购买的商品数据
    context = {'title': '购物车', 'cart_list': cart_list}
    return render(request, 'cart/cart.html', context)


def edit(request):
    id = request.GET.get('id')
    count = request.GET.get('count')
    cart = CartInfo.objects.get(pk=id) # 创建一个对象用来保存数据
    cart.count = count
    cart.save()
    return JsonResponse({'ok': 1})


def del1(request):
    id = request.GET.get('id')
    cart = CartInfo.objects.get(pk=id)
    cart.delete()
    return JsonResponse({'ok': 1})


def order(request):
    user = UserInfo.objects.get(pk=request.session.get('uid')) # 通过session中存储的uid，获取当前登录的用户
    cart_ids = request.POST.getlist('cart_id') # 获取到选中的（会有很多的cart_id所以用getlist方法)， cart_id是键（就是name属性）
    cart_list = CartInfo.objects.filter(id__in=cart_ids) # 想要找到，需要在模板那边提交过来才能找到
    context = {'title': '提交订单', 'user': user, 'cart_list': cart_list}
    return render(request, 'cart/order.html', context)
