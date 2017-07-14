# coding=utf-8
from django.db import models
from goods.models import GoodsInfo
# Create your models here.


class CartInfo(models.Model):
    # 谁买了多少个什么
    user = models.ForeignKey('user.UserInfo') # 引用类的另一种方式，也可以和下面的一样引用就是从最上方导入
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()