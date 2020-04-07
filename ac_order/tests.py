from django.test import TestCase

# Create your tests here.
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ACShop.settings')

application = get_wsgi_application()

from ac_order import models
from common.chackData import Order,Goods
# models.OrderInfo.objects(pk=1)

from ac_goods.models import Account
from ac_order.models import OrderInfo
# accounts = Account.objects.filter(order__order_no='c68b9751866b4b00aaed3e9f1b7cad19')
# for account in accounts:
#     print(account)

# order = OrderInfo.objects.filter(order_no='23132').first()
# print(order)

# if hasattr(locals(),'Account'):
#     a = getattr(locals(),'Account')
# import datetime
# time_now = datetime.datetime.now()
#
# order = Order().order.get(order_no='27c5339c64c248928674e4699aff3b34')
# goods = Goods().account.gets(price=order.price, allow_sale_time__lt=time_now).order_by(
#                 'add_time')[:order.count]
# print(goods)




from django.db.models import Q

order_no = '27df9c84fe7f4453925177298525b0d0'
accounts = Goods().account.gets(Q(order__trade_status=2 or 3), order__order_no=order_no )
print(accounts)


orders = Order().order.gets(Q(trade_status=3)|Q(trade_status=2), order_no=order_no )
print(orders)