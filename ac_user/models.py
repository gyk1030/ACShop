from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    username = models.CharField(max_length=20, null=False, unique=True,verbose_name='用户名')
    name = models.CharField(max_length=20, null=True, default='凡夫俗子',verbose_name='昵称')
    email = models.EmailField(null=True,blank=True,verbose_name='邮箱')
    choices = ((1,'男'),(2,'女'))
    sex = models.IntegerField(choices=choices,default=1,verbose_name='性别')
    birth = models.DateField(null=True,blank=True,verbose_name='出生日期')
    address = models.CharField(max_length=50,null=True,blank=True,verbose_name='地址')
    isDelete = models.BooleanField(default=False,verbose_name='是否删除')

    class Meta():
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.username