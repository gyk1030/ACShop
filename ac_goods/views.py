from django.shortcuts import render, redirect, HttpResponse

import datetime
from django.core.paginator import Paginator
from django.db import transaction

from ac_goods.myforms import OrderForms

from common.chackData import Goods,Order
from common.utils import get_new_no,get_name
from django.views import View



class IndexView(View):
    '''主页面'''
    def get(self, request):
        name = get_name(request)
        types = Goods().type.gets()
        page_id = request.GET.get('page_id', '1')  # 当前页
        limit = request.GET.get('limit', 4)  # 每页显示条数
        if page_id.isdigit():
            page_id = int(page_id)
        type_list = []
        has_previous = False  # 是否有前一页
        has_next = False  # 是否有后一页

        for type in types:
            data_dic = {}  # 存放每个类型下的所有信息
            sum = 0  # 每个类型下的账号总数
            print(type.price)
            for i in type.price.filter():
                count1 = i.account.filter(isSale=0).count()
                sum += count1
            data_dic.setdefault('title', type.title)
            data_dic.setdefault('description', type.description)
            data_dic.setdefault('sum', sum)
            data_dic.setdefault('avatar', type.avatar)
            data_dic.setdefault('type_id', type.pk)
            type_list.append(data_dic)
        paginator = Paginator(type_list, limit)  # 分页
        goods_list = paginator.page(page_id)
        page_list = paginator.page_range
        if page_id > 1:
            has_previous = True
        if page_id < page_list[-1]:
            has_next = True
        return render(request, 'ac_goods/index.html', {'types': types, 'goods_list': goods_list,
                                                       'page_list': page_list, 'has_previous': has_previous,
                                                       'has_next': has_next, 'page_curr': page_id, 'name': name})


# 购买页面
class GoodsDetailView(View):
    '''详情页面'''
    def get(self, request, type_id=None, *args):
        # 获取数据
        name = get_name(request)
        error = {}
        types = Goods().type.gets()
        if not type_id:
            type_id = request.GET.get('type_id', None)
        if args:
            error['status'] = args[0]['status']
            error['msg'] = args[0]['msg']
        type = Goods().type.get(pk=type_id)

        if not type:
            return render(request, '404.html')
        title = type.title
        avatar = type.avatar
        levels = Goods().level.gets()
        level_list = []

        for level in levels:
            price = Goods().price.get(type__pk=type_id, level__name=level.name)
            if price:
                level_dic = {}
                level_dic.setdefault('level', level.name)
                unit = price.unit
                units = price.get_currency_display() + '/' + unit  # 构造单位：人民币/个 or 美元/个
                level_dic.setdefault('price', price.price)
                level_dic.setdefault('count', price.account.filter(isSale=0).count())
                level_dic.setdefault('units', units)
                level_dic.setdefault('price_id', price.pk)
                level_list.append(level_dic)

        return render(request, 'ac_goods/detail.html', {'types': types, 'level_list': level_list,
                                                        'title': title, 'avatar': avatar,
                                                        'type_id': type_id, 'name': name,
                                                        'error': error})


    @transaction.atomic()
    def post(self, request):
        # 获取数据
        user = request.user
        info = {'status': 100, 'msg': None}
        type_id = request.GET.get('type_id', None)
        print('?????', type_id)
        order_data = {}

        # 校验数据
        forms = OrderForms(request.POST)
        if not forms.is_valid():
            info['status'] = 101
            error_all = forms.errors.get('__all__')
            error_price_id = forms.errors.get('price_id')
            info['msg'] = error_price_id if error_price_id else error_all
            return self.get(request, type_id, info)
        if type_id is None:
            return self.get(request, type_id, info)

        # 生成订单
        tran_id = transaction.savepoint()  # 建立事物点
        try:
            dic = forms.cleaned_data
            price_id, price = dic['price_id']
            price_obj = Goods().price.get(pk=price_id)
            count = dic['count']
            total_price = float(price) * int(count)  # 计算出总价格

            order_no = get_new_no()  # 生成一个唯一随机订单号
            order_data.setdefault('order_no', order_no)  # 订单号
            order_data.setdefault('user', user)  # 用户
            order_data.setdefault('price', price_obj)  # 单价
            order_data.setdefault('total_price', total_price)  # 总价格
            order_data.setdefault('count', count)  # 数量

            create_res = self.create_order(order_data)  # 创建订单
            dispatch_res = self.dispatch_account(order_no)
            if create_res and dispatch_res:
                return redirect('/order/order_pay/?order_no={}'.format(order_no))
        except Exception as e:
            print(e)
            transaction.savepoint_rollback(tran_id)  # 期间出错，全部回滚
        info['status'] = 101
        info['msg'] = '订单生成失败'
        return self.get(request, type_id, info)

    def create_order(self,order_data):
        '''创建订单'''
        if order_data:
            try:
                return Order().order.create(**order_data)
            except Exception:
                return False
        else:
            return False

    def dispatch_account(self,order_no):
        '''分配账号信息'''
        time_now = datetime.datetime.now()
        order = Order().order.get(order_no=order_no)
        count = int(order.count)
        try:
            account_list = Goods().account.gets(price=order.price, isSale=0, allow_sale_time__lt=time_now).order_by('add_time')[:count]
            for i in account_list:
                i.order = order
                i.isSale = 2
                i.sale_time = time_now
                i.save()
            return True
        except Exception:
            return False

# 错误页面
def error(request):
    return render(request, '404.html')
