# coding=utf-8
from django.db import models
from user.models import UserInfo
from goods.models import GoodsInfo
# Create your models here.


class OrderMain(models.Model):  # 主表
    order_id = models.CharField(max_length=20, primary_key=True)  # 自定义主键，在表中唯一不重复
    user = models.ForeignKey(UserInfo)  # 外键,关联表
    order_date = models.DateTimeField(auto_now_add=True)  # 日期时间
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)  # 购物的总金额 共五位，两位小数
    state = models.IntegerField(default=0)  # 支付状态


class OrderDetail(models.Model):  # 详单表
    order = models.ForeignKey(OrderMain)  # 与主表相关联
    goods = models.ForeignKey(GoodsInfo)  # 详单里面的商品
    count = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
