# Generated by Django 2.1.7 on 2020-01-12 02:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ac_goods', '0007_auto_20200106_0609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='order',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='account', to='ac_order.OrderInfo'),
        ),
        migrations.AlterField(
            model_name='account',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account', to='ac_goods.UnitPrice', verbose_name='价格'),
        ),
        migrations.AlterField(
            model_name='unitprice',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price', to='ac_goods.LevelInfo', verbose_name='级别'),
        ),
        migrations.AlterField(
            model_name='unitprice',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price', to='ac_goods.TypeInfo', verbose_name='类型'),
        ),
    ]
