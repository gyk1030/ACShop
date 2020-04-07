from django.db import models

# Create your models here.

class OrderInfo(models.Model):
    order_no = models.CharField(max_length=36,verbose_name='订单编号')  # 订单编号
    user = models.ForeignKey('ac_user.UserInfo',related_name='order',on_delete=models.CASCADE,verbose_name='用户')  # 对应用户
    price = models.ForeignKey('ac_goods.UnitPrice',related_name='order', verbose_name='单价',on_delete=models.CASCADE)
    total_price = models.DecimalField(decimal_places=2, max_digits=7, verbose_name='总价格')  # 总价格
    count = models.IntegerField()  # 商品数量
    add_time = models.DateTimeField(auto_now=True,verbose_name='生成时间')  # 生成时间
    Trade_Choice = ((0,'等待支付'),(1,'交易超时'),(2,'交易成功'),(3,'交易完毕'))  # (等待支付，交易超时或支付后退款，交易成功，交易成功不可退款)
    trade_status = models.IntegerField(choices=Trade_Choice,default=0,verbose_name='交易状态')  # 交易状态
    trade_no = models.CharField(max_length=36,verbose_name='交易号')  # 交易号
    Pay_Choice = ((0,'支付宝'),(1,'微信'),(2,'银行卡'))
    pay_mode = models.IntegerField(choices=Pay_Choice,default=0,verbose_name='支付方式')
    isDelete = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = '订单信息'

    def __str__(self):
        return self.order_no



# class OrderDetailInfo(models.Model):
