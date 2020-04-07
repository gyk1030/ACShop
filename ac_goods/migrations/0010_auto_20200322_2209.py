# Generated by Django 2.1.7 on 2020-03-22 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac_goods', '0009_auto_20200321_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='isSale',
            field=models.IntegerField(choices=[(0, '未出售'), (1, '已出售'), (2, '已锁定')], default=0, verbose_name='是否出售'),
        ),
    ]
