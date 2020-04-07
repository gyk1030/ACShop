from django.test import TestCase

# Create your tests here.

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ACShop.settings')

application = get_wsgi_application()


from ac_order.models import OrderInfo
from ac_user.models import UserInfo
from django.db.models import Q

# user = UserInfo.objects.get(pk=1)
# orders = OrderInfo.objects.filter(Q(user=user) & Q(trade_status=0) | Q(trade_status=3))
# for order in orders:
#     # print(order.order_no)
#     for i in order.account.all():
#         print(i.account_str)
#         print(str(i.price).split(':')[0])
#         print(i.sale_time)
#         print(i.price.price)
#         print('---------------')


user = UserInfo.objects.filter(pk=None,isDelete=False).first()
print(user)