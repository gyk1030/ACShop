from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse

import datetime
import time
import threading

from ac_order.PAY.alipay import AliPay
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import transaction

from common.chackData import Goods
from common.chackData import Order

from ACShop.settings import ORDER_TIMEOUT,MODE_LIST,TIME_OUT_EXPRESS


'''################################################ 支付相关操作 #################################################'''
class OrderPay(View):
    order_no = None
    # 参数验证
    def verify(self,user,order_no,pay_mode):
        if order_no and pay_mode in MODE_LIST:
            order = Order().order.get(order_no=order_no, user=user, trade_status=0)
            if order:
                return True, order
            else:
                return False, '订单无效或不存在'
        else:
            return False, '参数错误'

    # 根据支付方式分发执行函数
    def pay_dispatch(self,pay_mode):
        if pay_mode == MODE_LIST[0]:
            mode = '_ali_pay'
        elif pay_mode == MODE_LIST[1]:
            mode = '_wx_pay'
        else:
            mode = '_bank_pay'
        return mode

class OrderPayView(OrderPay):
    # 订单支付页面
    res = {'status': 0, 'url': None, 'msg': None}
    def get(self,request, order_no=None):
        user = request.user
        types = Goods().type.gets()
        if request.method == 'GET':
            if not order_no:
                order_no = request.GET.get('order_no')
            order = Order().order.get(order_no=order_no)
            order_data = {}
            if order:
                order_data.setdefault('order_no', order_no)
                order_data.setdefault('user', order.user)
                order_data.setdefault('price', order.price.price)
                order_data.setdefault('total_price', order.total_price)
                order_data.setdefault('count', order.count)
                delta = datetime.timedelta(minutes=ORDER_TIMEOUT)  # 设置延时时间
                end_time = (order.add_time + delta).strftime('%Y/%m/%d,%H:%M:%S')
                order_data.setdefault('end_time', str(end_time))
                type = order.price.type.title
                level = order.price.level.name
                order_data.setdefault('type', type + '：' + level)

                return render(request, 'ac_order/order.html', {'types': types, 'order_data': order_data, 'name': user.name})
            else:
                self.res['msg'] = '订单不存在'
                return JsonResponse(self.res)

    def post(self, request):
        # 参数校验
        user = request.user
        order_no = request.POST.get('order_no')
        pay_mode = request.POST.get('mode')
        res,msg = self.verify(user,order_no,pay_mode)
        if res is True:
            mode = self.pay_dispatch(pay_mode)
            if hasattr(OrderPayView,mode):
                try:
                    getattr(OrderPayView,mode)(self, order_no, msg.total_price)
                    threading.Thread(target=ChackView().post,args=request).start()
                    return JsonResponse(self.res)
                except Exception as e:
                    self.res['msg'] = '请求失败'
            else:
                self.res['msg'] = '支付方式错误'
        else:
            self.res['msg'] = msg
        return JsonResponse(self.res)

    # 支付宝支付
    def _ali_pay(self, order_no, total_price):
        pay_instance = AliPay()
        url = pay_instance.direct_pay(
            subject="账号订单",
            out_trade_no=order_no,
            total_amount=float(total_price)
        )
        re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
        self.res['url'] = re_url
        self.res['status'] = 1
        self.res['msg'] = '请求成功'

    # 微信支付
    def _wx_pay(self, order_no, total_price):
        self.res['msg'] = '暂不支持微信支付'

    # 银行卡支付
    def _bank_pay(self, order_no, total_price):
        self.res['msg'] = '暂不支持银行卡支付'


# 订单支付结果查询
class ChackView(OrderPay):
    res = {'status': 0, 'msg': None}
    def post(self, request):
        # 用户及参数校验
        user = request.user
        order_no = request.POST.get('order_no')
        pay_mode = request.POST.get('mode')
        res,msg = self.verify(user,order_no,pay_mode)
        if res is True:
            mode = self.pay_dispatch(pay_mode)
            # 检查查询函数是否存在
            if hasattr(ChackView,mode):
                try:
                    getattr(ChackView,mode)(self,order_no)
                    print()
                    return JsonResponse(self.res)
                except Exception:
                    self.res['msg'] = '查询失败'
        else:
            self.res['msg'] = msg
        return JsonResponse(self.res)

    @transaction.atomic()
    def _ali_pay(self,order_no):
        '''支付宝查询'''
        pay_instance = AliPay()
        c = 0
        while c<TIME_OUT_EXPRESS*60/5:  # 超过支付时间跳出循环
            c+=1
            print(c)
            time.sleep(5)
            response = pay_instance.alipay_trade_query(out_trade_no=order_no)
            code = response['alipay_trade_query_response'].get('code',None)
            trade_status = response['alipay_trade_query_response'].get('trade_status',None)
            trade_no = response['alipay_trade_query_response'].get('trade_no',None)
            print('.........................................')
            print(response)
            print(trade_status)
            print(trade_no)
            print('.........................................')
            if code == '10000' and  trade_status == 'TRADE_SUCCESS':
                tran_id = transaction.savepoint()
                # 支付成功
                try:
                    order_res = self.modify_order_handler(order_no, trade_status, trade_no)
                    account_res = self.modify_account_status(order_no)
                    if order_res and account_res:
                        self.res['status'] = 1
                        self.res['msg'] = '订单和账号状态修改成功'
                        # self.res['url'] = '/order/order_detial/?order_no={}'.format(order_no)
                    else:
                        self.res['msg'] = '订单和账号状态修改失败'
                except Exception:
                    transaction.savepoint_rollback(tran_id)
                break


    def modify_order_handler(self, order_no, trade_status, trade_no):
        '''修改订单记录'''
        order = Order().order.get(order_no=order_no)
        trade_status_list = ['WAIT_BUYER_PAY', 'TRADE_CLOSED', 'TRADE_SUCCESS', 'TRADE_FINISHED']
        if order:
            if trade_status in trade_status_list:
                try:
                    order.trade_status = trade_status_list.index(trade_status)
                    order.trade_no = trade_no
                    order.save()
                    return True
                except Exception:
                    pass
        return False

    def modify_account_status(self, order_no):
        '''修改账号状态'''
        order = Order().order.get(order_no=order_no)
        account_list = Goods().account.gets(order=order, isSale=2)
        if account_list:
            try:
                for account in account_list:
                    account.isSale = 1
                    account.save()
                return True
            except Exception:
                pass
        return False

    # 微信查询
    def _wei_xin_pay(self, order_no):
        pass

    # 银行卡查询
    def _bank_pay(self, order_no):
        pass


# 订单超时，删除订单
class KillOrder(View):
    def get(self,request):
        order_no = request.GET.get('order_no')
        if not order_no:
            order_no = request.GET.get('order_no')
        order = Order().order.gets(order_no=order_no)
        if order.exists():
            Order().order.delete(order_no=order_no)
        return redirect('/order/ordered/')


# 支付宝调用接口
class PayView(View):
    alipay = AliPay()

    def get(self,request):
        '''处理与return_url请求相似'''
        params = request.GET.dict()
        order_no = params.get('out_trade_no')
        sign = params.pop('sign',None)
        verify_result = self.alipay.verify(params,sign)
        if verify_result:
            return render(request,'ac_order/result.html',{'Success':True,'order_no':order_no})
        else:
            return render(request,'ac_order/result.html',{'Failure':True,'order_no':order_no})

    @transaction.atomic()
    def post(self, request):
        '''处理notify_url接收到的请求'''
        processed_dict = {}  # 定义一个字典，用来存放支付宝发来的信息，后面用起来方便
        for key, value in request.POST.items():
            processed_dict[key] = value

        # 取出签名进行验证
        sign = processed_dict.pop('sign', None)

        verify_result = self.alipay.verify(processed_dict, sign)  # verify方法会解析所接收的数据，得到是否支付成功的结果，True or False
        if verify_result is True:

            order_no = processed_dict.get('out_trade_no', None)  # 订单号
            trade_no = processed_dict.get('trade_no', None)  # 支付宝交易号
            trade_status = processed_dict.get('trade_status', None)  # 交易状态
            tran_id = transaction.savepoint()
            try:
                self.modify_order_handler(order_no, trade_status, trade_no)
                self.modify_account_status(order_no)
            except Exception:
                transaction.savepoint_rollback(tran_id)
            return JsonResponse('success')  # 最后记着给支付宝返回一个信息
        else:pass

    def modify_order_handler(self, order_no, trade_status, trade_no):
        '''修改订单记录'''
        order = Order().order.get(order_no=order_no)
        trade_status_list = ['WAIT_BUYER_PAY', 'TRADE_CLOSED', 'TRADE_SUCCESS', 'TRADE_FINISHED']
        if order:
            if trade_status in trade_status_list:
                try:
                    order.trade_status = trade_status_list.index(trade_status)
                    order.trade_no = trade_no
                    order.save()
                    return True
                except Exception:
                    pass
        return False

    def modify_account_status(self,order_no):
        '''修改账号状态'''
        order = Order().order.get(order_no=order_no)
        account_list = Goods().account.gets(order=order, isSale=2)
        if account_list:
            try:
                for account in account_list:
                    account.isSale = 1
                    account.save()
                return True
            except Exception:
                pass
        return False


'''############################################### 支付相关操作 ##################################################33333333333'''


# 订单记录页面返回
class Ordered(View):
    def get(self,request):
        user = request.user
        types = Goods().type.gets()
        return render(request, 'ac_order/ordered.html', {'types': types, 'name': user.name})



# 订单记录数据返回
class OrderInfo(View):
    def get(self,request):
        user = request.user
        n = 1
        page_id = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        orders_dic = {'code': 0, 'msg': '', 'count': 0, 'data': ''}
        orders_list = []
        if user:
            # 条件：用户
            orders = Order().order.gets(user=user)
            for order in orders:
                order_dic = {}
                order_dic.setdefault('id', n)
                order_dic.setdefault('order_no', order.order_no)
                order_dic.setdefault('price', str(order.price))
                order_dic.setdefault('total_price', order.total_price)
                order_dic.setdefault('count', order.count)
                order_dic.setdefault('add_time', order.add_time.strftime('%Y-%m-%d %H:%M:%S'))
                order_dic.setdefault('trade_status', order.get_trade_status_display())
                order_dic.setdefault('trade_no', order.trade_no)
                order_dic.setdefault('trade_type', order.get_pay_mode_display())
                orders_list.append(order_dic)
                n += 1

            paginator = Paginator(orders_list, limit)  # 分页，每页显示limit个
            try:
                order_list = paginator.page(int(page_id))
                order_list = [i for i in order_list]  # 将数据从Page对象中遍历出来
                page_count = paginator.count
                orders_dic['count'] = page_count
                orders_dic['data'] = order_list
            except:
                pass
        return JsonResponse(orders_dic)


# 获取个人订单详情
class OrderDetail(View):
    def get(self,request):
        user = request.user
        types = Goods().type.gets()
        order_no = request.GET.get('order_no')
        order_dic = {}
        if user:
            # 条件：用户，订单号
            order = Order().order.get(Q(user=user) & Q(order_no=order_no))
            if order:
                order_dic.setdefault('order_no', order.order_no)
                order_dic.setdefault('price', str(order.price))
                order_dic.setdefault('total_price', order.total_price)
                order_dic.setdefault('count', order.count)
                order_dic.setdefault('add_time', order.add_time.strftime('%Y-%m-%d %H:%M:%S'))
                order_dic.setdefault('trade_status', order.get_trade_status_display())
                order_dic.setdefault('trade_no', order.trade_no)
                order_dic.setdefault('trade_type', order.get_pay_mode_display())

        return render(request, 'ac_order/order_detail.html',
                      {'types': types, 'name': user.name, 'order_dic': order_dic})


# 单个订单所有账号信息
class GoodsInfo(View):
    def get(self,request):
        user = request.user
        n = 1
        page_id = request.GET.get('page', 1)
        order_no = request.GET.get('order_no', None)
        limit = request.GET.get('limit', 5)
        goods_dic = {'code': 0, 'msg': '', 'count': 0, 'data': ''}
        goods_list = []
        if user:
            # 条件：用户、订单、交易状态
            accounts = Goods().account.gets(Q(order__trade_status=2) | Q(order__trade_status=3),
                                            order__order_no=order_no)
            for account in accounts:
                account_dic = {}
                info = str(account.price).split(':')
                account_dic.setdefault('id', n)
                account_dic.setdefault('order_no', order_no)
                account_dic.setdefault('type', info[0])
                account_dic.setdefault('account_str', account.account_str)
                account_dic.setdefault('price', info[1])
                account_dic.setdefault('sale_time', account.sale_time.strftime('%Y-%m-%d %H:%M:%S'))
                goods_list.append(account_dic)
                n += 1

            paginator = Paginator(goods_list, limit)  # 分页，每页显示limit个
            try:
                goods_list = paginator.page(int(page_id))
                goods_list = [i for i in goods_list]  # 将数据从Page对象中遍历出来
                page_count = paginator.count
                goods_dic['count'] = page_count
                goods_dic['data'] = goods_list
            except:
                pass
        return JsonResponse(goods_dic)



# 错误页面
def error(request):
    return render(request, '404.html')
