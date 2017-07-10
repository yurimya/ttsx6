# coding=utf-8
from django.db import models
from tinymce.models import HTMLField
# Create your models here.


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.title.encode('utf-8')


class GoodsInfo(models.Model):
    gtitle = models.CharField(max_length=50) # 商品名
    gpic = models.ImageField(upload_to='goods') # 图片
    gprice = models.DecimalField(max_digits=5, decimal_places=2)# 价格 前者表示总共多少位，后者表示小数位数
    gclick = models.IntegerField(default=0) # 点击量
    gunit = models.CharField(max_length=20) # 单位  例：2/500g
    isDelete = models.BooleanField(default=False)
    gsubtitle = models.CharField(max_length=200) # 详细名称
    gkucun = models.IntegerField(default=100) # 库存
    gcontent = HTMLField()  # 富文本编辑器
    gtype = models.ForeignKey('TypeInfo')

# 模型类定义好去后台管理admin