# coding=utf-8
from django.shortcuts import render, redirect
from django.http import JsonResponse
from models import *
from hashlib import sha1
import datetime
from login_decorator import *
# Create your views here.


def register(request):
    context = {'title': '注册', 'top': '0'}
    return render(request, 'user/register.html', context)


def register_handle(request):
    # 接收数据
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    umail = post.get('user_email')
    # 加密
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd_sha1
    user.umail = umail
    user.save()
    # 完成后转向
    return redirect('/user/login/')


def register_valid(request):
    uname = request.GET.get('uname')
    result = UserInfo.objects.filter(uname=uname).count()
    context = {'valid': result}
    return JsonResponse(context)


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '登录', 'uname':uname, 'top': '0'}
    return render(request, 'user/login.html', context)


def logout(request):
    request.session.flush()
    return redirect('/user/login/')


def login_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('user_pwd')
    uname_jz = post.get('uname_jz', '0')
    s1 = sha1()
    s1.update(upwd)
    upwd_sha1 = s1.hexdigest()
    context = {'title': '登录', 'uname': uname, 'upwd': upwd, 'top': '0'}
    # 根据用户名查询数据，如果未查到返回[]，如果查到则返回[UserInfo]
    users = UserInfo.objects.filter(uname=uname)
    print users
    print users[0]
    print users[0].uname
    if len(users) == 0:
    # 用户名错误
        context['name_error'] = '1'
        return render(request, 'user/login.html', context)
    else:
        if users[0].upwd == upwd_sha1:
            # 登陆成功
            # 记录当前登录的用户
            request.session['uid'] = users[0].id
            request.session['uname'] = users[0].uname
            # 记住用户名
            path = request.session.get('url_path')
            response = redirect(path)
            if uname_jz == '1':
                response.set_cookie('uname', uname, expires=datetime.datetime.now() + datetime.timedelta(days=7))
            else:
                response.set_cookie('uname', '', max_age=-1)
            return response
        else:
            # 密码错误
            context['pwd_error'] = '1'
            return render(request, 'user/login.html', context)


@ss
def center(request):
    user=UserInfo.objects.get(pk=request.session['uid'])
    context={'title':'用户中心','user':user}
    return render(request,'user/center.html',context)


@ss
def order(request):
    context={'title':'用户订单'}
    return render(request,'user/order.html',context)


@ss
def site(request):
    user = UserInfo.objects.get(pk=request.session['uid'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.ucode = post.get('ucode')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '收货地址', 'user': user}
    return render(request, 'user/site.html', context)

