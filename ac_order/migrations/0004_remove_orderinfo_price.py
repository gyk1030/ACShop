# Generated by Django 2.1.7 on 2020-01-06 06:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ac_order', '0003_orderinfo_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderinfo',
            name='price',
        ),
    ]