# Generated by Django 2.1.7 on 2020-01-12 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac_order', '0007_auto_20200112_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='trade_status',
            field=models.IntegerField(choices=[(0, '等待支付'), (1, '交易超时'), (2, '交易成功'), (3, '交易完毕')], default=0, verbose_name='交易状态'),
        ),
    ]
