# Generated by Django 2.1.7 on 2020-03-05 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ac_order', '0008_auto_20200112_0534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderinfo',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order', to='ac_goods.UnitPrice', verbose_name='单价'),
        ),
    ]
