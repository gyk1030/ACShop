# Generated by Django 2.1.7 on 2020-03-21 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac_goods', '0008_auto_20200112_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='isSale',
            field=models.CharField(choices=[(0, '未出售'), (1, '已出售'), (2, '已锁定')], default=0, max_length=1, verbose_name='是否出售'),
        ),
    ]
