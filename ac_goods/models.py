from django.db import models

# Create your models here.
import datetime
delay = datetime.datetime.now()+datetime.timedelta(hours=8)

class TypeInfo(models.Model):
    avatar = models.FileField(upload_to='avatar/',default='avatar/default.jpg')
    title = models.CharField(max_length=20,verbose_name='类型',unique=True)
    isDelete = models.BooleanField(default=False,verbose_name='是否删除')
    description = models.CharField(max_length=255,verbose_name='类型简介')

    class Meta():
        verbose_name_plural = '账号类型'

    def __str__(self):
        return self.title

class LevelInfo(models.Model):
    name = models.CharField(max_length=6,verbose_name='级别',unique=True)  # “小白账号”，“稳定账号”，“100+账号”
    isDelete = models.BooleanField(default=False,verbose_name='是否删除')
    description = models.CharField(max_length=255,verbose_name='级别简介')

    class Meta():
        verbose_name_plural = '账号级别'

    def __str__(self):
        return self.name

class UnitPrice(models.Model):
    type = models.ForeignKey(TypeInfo,related_name='price',on_delete=models.CASCADE,verbose_name='类型')
    level = models.ForeignKey(LevelInfo,related_name='price',on_delete=models.CASCADE,verbose_name='级别')
    price = models.DecimalField(decimal_places=2,max_digits=5,verbose_name='价格')
    Choice = ((0,'人民币'))
    currency = models.IntegerField(choices=Choice,default=0,verbose_name='货币')
    unit = models.CharField(max_length=10,default='个',verbose_name='单位')
    isDelete = models.BooleanField(default=False)

    class Meta():
        unique_together = ('type', 'level')
        verbose_name_plural = '单位价格'

    def __str__(self):
        return self.type.title+'-'+self.level.name+':'+str(self.price)

class Account(models.Model):
    price = models.ForeignKey('UnitPrice',related_name='account',on_delete=models.CASCADE,verbose_name='价格')
    account_str = models.CharField(max_length=50,verbose_name='账号信息',unique=True)
    add_time = models.DateTimeField(auto_now=True,verbose_name='添加时间')
    allow_sale_time = models.DateTimeField(null=True,blank=True,verbose_name='可售时间')
    sale_time = models.DateTimeField(verbose_name='出售时间',null=True,blank=True)
    order = models.ForeignKey('ac_order.OrderInfo',related_name='account', on_delete=models.CASCADE,null=True,blank=True)  # 订单编号
    Choice = ((0,'未出售'),(1,'已出售'),(2,'已锁定'))
    isSale = models.IntegerField(choices=Choice,default=0,verbose_name='是否出售')
    isDelete = models.BooleanField(default=False,verbose_name='是否删除')

    def clean(self, exclude=None):
        self.allow_sale_time = datetime.datetime.now()+datetime.timedelta(hours=8)  # 修改允许出售时间

    class Meta():
        verbose_name_plural = '账号信息'

    def __str__(self):
        return self.account_str
