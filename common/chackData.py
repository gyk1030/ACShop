# Author:gyk

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ACShop.settings')  # 添加到django模块
application = get_wsgi_application()  # 注册app

from ac_goods.models import UnitPrice, Account, TypeInfo, LevelInfo
from ac_order.models import OrderInfo
from ac_user.models import UserInfo


class GetTable():
    def __init__(self, table):
        self.table = table

    def get(self, *args, **kwargs):
        return self.table.objects.filter(isDelete=False, *args, **kwargs).first()

    def gets(self, *args, **kwargs):
        return self.table.objects.filter(isDelete=False, *args, **kwargs)

    def create(self, *args, **kwargs):
        return self.table.objects.create(*args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.table.objects.filter(*args, **kwargs).update(isDelete=True)


class Order():
    @property
    def order(self):
        return GetTable(OrderInfo)


class Goods():
    @property
    def price(self):
        return GetTable(UnitPrice)

    @property
    def account(self):
        return GetTable(Account)

    @property
    def type(self):
        return GetTable(TypeInfo)

    @property
    def level(self):
        return GetTable(LevelInfo)


class User():
    @property
    def user(self):
        return GetTable(UserInfo)


if __name__ == '__main__':
    # obj = Order()
    # a = obj.order.gets(order_no='e4c2fe74cfa948afb9cf72b86344c4a5')[0].update(isDelete=True)

    a = Goods().level.gets()
    print(a)

