# Author:gyk

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ACShop.settings')
application = get_wsgi_application()


from ac_goods.models import Account
from ACShop.settings import ALLOW_SALE_TIME
import random

seeds = 'abcdefghijklmnopqrstuvwxyz'
a = len(seeds) - 15


def test(e):
    n = 0
    while n < e:
        n += 1
        w = ''
        for i in range(15):
            b = random.choice(seeds)
            w+=b
        yield w


import datetime
if __name__ == '__main__':
    q = test(300)
    for i in q:
        a = random.randint(1, 7)
        allow_sale_time = datetime.datetime.now()+datetime.timedelta(hours=ALLOW_SALE_TIME)
        x = Account(account_str=i,price_id=a,allow_sale_time=allow_sale_time)
        x.save()
