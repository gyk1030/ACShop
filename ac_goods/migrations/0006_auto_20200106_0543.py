# Generated by Django 2.1.7 on 2020-01-05 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac_goods', '0005_auto_20200106_0541'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='allow_sale_time',
            field=models.DateTimeField(auto_now=True, verbose_name='可售时间'),
        ),
    ]
