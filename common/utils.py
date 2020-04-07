# Author:gyk

from django.db.models import Q
from ac_user.models import UserInfo
from django.contrib.auth.backends import ModelBackend
from ac_goods.models import TypeInfo
import uuid
import random

seeds = '1234567890'

# 重写认证方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None,**kwargs):
        try:
            user = UserInfo.objects.get(Q(isDelete=False) & (Q(username=username) | Q(email=username)))
            if user.check_password(password):
                return user
        except Exception:
            return None

def get_name(request):
    if request.user.is_authenticated:
        return request.user.name
    else:
        return None


# 利用uuid生成一个新的订单号
def get_new_no():
    return str(uuid.uuid4()).replace('-','')


# 生成n位数字验证码
def gen_code_num(n):
    random_str = []
    for i in range(n):
        random_str.append(random.choice(seeds))
    code = ''.join(random_str)
    return code


def get_types():
    return TypeInfo.objects.filter(isDelete=False)

