from django.test import TestCase

# Create your tests here.
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ACShop.settings')

application = get_wsgi_application()


from ac_goods.models import TypeInfo,LevelInfo,UnitPrice,Account


# 查看所有账号的类型及级别
# accounts = Account.objects.all()
# for acc in accounts:
#     print(acc.price.type)
#     print(acc.price.level)



# 查看指定价格对象的价格价格
# price = UnitPrice.objects.filter(type__title='CB账号',level__name='小白账号')
# for i in price:
#     print(i.price)


# 查看指定账号类型的所有级别及价格
# type_obj = TypeInfo.objects.filter(title='CB账号').first()
# levels = type_obj.price.all()
# for i in levels:
#     print(i.price)
#     print(i.level)



# 查询所有类型信息
# types = TypeInfo.objects.all()
# type_list = []
# for type in types:
#     data_dic = {}
#     sum = 0
#     for i in type.price.all():
#         count1 = i.account.count()
#         sum += count1
#     data_dic.setdefault('title', type.title)
#     data_dic.setdefault('description', type.description)
#     data_dic.setdefault('sum', sum)
#     type_list.append(data_dic)
#     print(data_dic)



# 查询指定订单信息
# levels = LevelInfo.objects.all()
# level_list = []
# for j in levels:
#     prices = UnitPrice.objects.filter(type__pk=5, level__name=j.name)
#     for i in prices:
#         level_dic = {}
#         level_dic.setdefault('level', j.name)
#         level_dic.setdefault('price', i.price)
#         level_dic.setdefault('count', i.account.count())
#         level_dic.setdefault('title', i.type.title)
#         level_list.append(level_dic)
# print(level_list)



# p = UnitPrice.objects.all().first()
# print(p.get_currency_display())


# p = UnitPrice.objects.filter(type__pk='7', level__name='小白账号').first()
# print(p.unit)
# import datetime
# time_now = datetime.datetime.now()
#
# account_list = Account.objects.filter(price=1, isDelete=False, isSale=0,
#                                       allow_sale_time__lt=time_now).order_by('add_time')[:2]
#
# account_list = Account.objects.filter(price=7, isSale=0, allow_sale_time__lt=time_now).order_by('add_time')
# print(account_list)
# for i in account_list:
#     # i.order = 1
#     i.sale_time = time_now
#     i.isSale = True
#     i.save()
# account_list.update(sale_time=time_now,isSale=0)

# print(account_list)



# 打印日志测试
# from common.logg import Logger
# logger = Logger()
# logger.info('asdasd')