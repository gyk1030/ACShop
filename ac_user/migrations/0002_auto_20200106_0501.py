# Generated by Django 2.1.7 on 2020-01-05 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ac_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='isDelete',
            field=models.BooleanField(default=False, verbose_name='是否删除'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(default='凡夫俗子', max_length=20, null=True, verbose_name='昵称'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='username',
            field=models.CharField(max_length=20, unique=True, verbose_name='用户名'),
        ),
    ]
