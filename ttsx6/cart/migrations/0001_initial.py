# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [

        ('user', '0002_auto_20170711_2200'),
        ('goods', '0001_initial'),

        ('goods', '0001_initial'),
        ('user', '0001_initial'),

    ]

    operations = [
        migrations.CreateModel(
            name='CartInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('count', models.IntegerField()),
                ('goods', models.ForeignKey(to='goods.GoodsInfo')),
                ('user', models.ForeignKey(to='user.UserInfo')),
            ],
        ),
    ]
