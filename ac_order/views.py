import traceback
import datetime
import time

from django.views import View
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db import transaction

from common.chackData import Goods, Order
from common import response_utils
from common.utils import get_name
from ac_order.PAY.alipay import AliPay
from ACShop.settings import ORDER_TIMEOUT, TIME_OUT_EXPRESS, ALIPAY_GETWAY
from common.logg import Logger

logger = Logger()


class OrderPayView(View):
    '''订单支付页面'''

    def get(self, request, order_no=None):
        try:
            name = get_name(request)
            types = Goods().type.gets()
            if not order_no:
                order_no = request.GET.get('order_no')

            data = {}
            order = Order().order.get(order_no=order_no)
            if not order:
                data['msg'] = '获取订单信息失败'
                return render(request, 'ac_order/order.html', data)

            order_data = {}
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

            data['types'] = types
            data['name'] = name
            data['order_data'] = order_data

            return render(request, 'ac_order/order.html', data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return render(request, 'error.html', {'error': 500})

    def post(self, request):
        try:
            # 参数校验
            user = request.user
            order_no = request.POST.get('order_no')
            if not user:
                return response_utils.wrapper_400('获取用户对象失败')
            if not order_no:
                return response_utils.wrapper_400('缺少参数order_no')

            order = Order().order.get(order_no=order_no, user=user, trade_status=0)  # trade_status交易状态为等待支付
            if not order:
                return response_utils.wrapper_400('订单无效')

            url = self._ali_pay(order_no, order.total_price)
            if not url:
                return response_utils.wrapper_400('获取支付订单失败')

            data = {}
            data['url'] = url

            return response_utils.wrapper_200(data=data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return response_utils.wrapper_500('获取支付订单失败，系统内部错误')

    def _ali_pay(self, order_no, total_price):
        try:
            pay_instance = AliPay()
            url = pay_instance.direct_pay(
                subject="账号订单",
                out_trade_no=order_no,
                total_amount=float(total_price)
            )
            re_url = "{0}?{1}".format(ALIPAY_GETWAY, url)
            return re_url
        except Exception as e:
            logger.error(traceback.format_exc())
            return None


class CheckOrder(View):
    '''订单支付结果查询/////上线时不用的'''

    def post(self, request):
        # 用户及参数校验
        order_no = request.POST.get('order_no')
        if not order_no:
            return response_utils.wrapper_400('缺少参数order_no')

        res = self._ali_pay(order_no)
        if not res:
            return response_utils.wrapper_400('查询失败')

        return response_utils.wrapper_200()

    @transaction.atomic()
    def _ali_pay(self, order_no):
        try:
            '''支付宝查询'''
            pay_instance = AliPay()
            c = 0
            while c < TIME_OUT_EXPRESS * 60 / 5:  # 超过支付时间跳出循环
                c += 1
                print(c)
                time.sleep(5)
                response = pay_instance.alipay_trade_query(out_trade_no=order_no)
                code = response['alipay_trade_query_response'].get('code', None)
                trade_status = response['alipay_trade_query_response'].get('trade_status', None)
                trade_no = response['alipay_trade_query_response'].get('trade_no', None)
                # print('.........................................')
                # print(response)
                # print(trade_status)
                # print(trade_no)
                # print('.........................................')
                if code == '10000' and trade_status == 'TRADE_SUCCESS':
                    tran_id = transaction.savepoint()
                    # 支付成功
                    try:
                        order_res = self.modify_order_handler(order_no, trade_status, trade_no)
                        account_res = self.modify_account_status(order_no)
                        if order_res and account_res:
                            return True
                        else:
                            transaction.savepoint_rollback(tran_id)
                            # return False
                    except Exception:
                        transaction.savepoint_rollback(tran_id)
                    break
        except Exception as e:
            return False

    def modify_order_handler(self, order_no, trade_status, trade_no):
        '''修改订单记录'''
        try:
            order = Order().order.get(order_no=order_no)
            trade_status_list = ['WAIT_BUYER_PAY', 'TRADE_CLOSED', 'TRADE_SUCCESS', 'TRADE_FINISHED']
            if order and trade_status in trade_status_list:
                order.trade_status = trade_status_list.index(trade_status)
                order.trade_no = trade_no
                order.save()
                return True
        except Exception as e:
            return False

    def modify_account_status(self, order_no):
        '''修改账号状态'''
        try:
            order = Order().order.get(order_no=order_no)
            account_list = Goods().account.gets(order=order, isSale=2)
            if account_list:
                for account in account_list:
                    account.isSale = 1
                    account.save()
                return True
        except Exception as e:
            return False


class KillOrder(View):
    '''订单超时，删除订单'''

    def get(self, request):
        try:
            order_no = request.GET.get('order_no')
            if not order_no:
                return response_utils.wrapper_400('order_no参数缺失！')

            order = Order().order.gets(order_no=order_no)
            if order.exists():
                Order().order.delete(order_no=order_no)

            return redirect('/order/ordered/')
        except Exception as e:
            logger.error(traceback.format_exc())
            return render(request, 'error.html', {'error': 500})


class PayResultHandler(View):
    '''支付宝调用接口'''

    def get(self, request):
        '''处理与return_url请求相似'''
        try:
            self.alipay = AliPay()
            params = request.GET.dict()
            order_no = params.get('out_trade_no')
            sign = params.pop('sign', None)
            data = {'code': 200}
            verify_result = self.alipay.verify(params, sign)  # 验签

            if not (order_no and sign) or not verify_result:
                data['code'] = 400
                return render(request, 'ac_order/result.html', data)

            data['order_no'] = order_no
            return render(request, 'ac_order/result.html', data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return render(request, 'error.html', {'error': 500})

    @transaction.atomic()
    def post(self, request):
        '''处理notify_url接收到的请求'''
        try:
            processed_dict = {}  # 定义一个字典，用来存放支付宝发来的信息，后面用起来方便
            for key, value in request.POST.items():
                processed_dict[key] = value

            # 取出签名进行验证
            sign = processed_dict.pop('sign', None)

            verify_result = self.alipay.verify(processed_dict, sign)  # verify方法会解析所接收的数据，得到是否支付成功的结果，True or False
            if not verify_result:
                return response_utils.wrapper_400('验签失败')

            order_no = processed_dict.get('out_trade_no', None)  # 订单号
            trade_no = processed_dict.get('trade_no', None)  # 支付宝交易号
            trade_status = processed_dict.get('trade_status', None)  # 交易状态
            tran_id = transaction.savepoint()
            try:
                order_res = self.modify_order_handler(order_no, trade_status, trade_no)
                account_res = self.modify_account_status(order_no)
                if order_res and account_res:
                    pass
                else:
                    transaction.savepoint_rollback(tran_id)
            except Exception:
                transaction.savepoint_rollback(tran_id)
            return response_utils.wrapper_200()  # 最后记着给支付宝返回一个信息
        except Exception as e:
            logger.error(traceback.format_exc())
            return response_utils.wrapper_500()

    def modify_order_handler(self, order_no, trade_status, trade_no):
        '''修改订单记录'''
        try:
            order = Order().order.get(order_no=order_no)
            trade_status_list = ['WAIT_BUYER_PAY', 'TRADE_CLOSED', 'TRADE_SUCCESS', 'TRADE_FINISHED']
            if order and trade_status in trade_status_list:
                order.trade_status = trade_status_list.index(trade_status)
                order.trade_no = trade_no
                order.save()
                return True
        except Exception as e:
            logger.error(traceback.format_exc())
            return False

    def modify_account_status(self, order_no):
        '''修改账号状态'''
        try:
            order = Order().order.get(order_no=order_no)
            account_list = Goods().account.gets(order=order, isSale=2)
            if account_list:
                for account in account_list:
                    account.isSale = 1
                    account.save()
                return True
        except Exception as e:
            logger.error(traceback.format_exc())
            return False


class OrderPage(View):
    '''订单记录页面返回'''

    def get(self, request):
        try:
            name = get_name(request)
            types = Goods().type.gets()

            data = {}
            data['types'] = types
            data['name'] = name
            return render(request, 'ac_order/ordered.html', data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return render(request, 'error.html', {'error': '500'})


class OrderList(View):
    '''订单记录数据返回'''

    def get(self, request):
        try:
            user = request.user
            page_id = request.GET.get('page', 1)
            limit = request.GET.get('limit', 10)
            if not user:
                return response_utils.wrapper_400('获取用户对象失败')

            orders = Order().order.gets(user=user)  # 条件：用户
            if not orders:
                return response_utils.wrapper_400('无订单信息')

            orders_list = []
            for index, order in enumerate(orders):
                order_dic = {}
                order_dic.setdefault('id', index + 1)
                order_dic.setdefault('order_no', order.order_no)
                order_dic.setdefault('price', str(order.price))
                order_dic.setdefault('total_price', order.total_price)
                order_dic.setdefault('count', order.count)
                order_dic.setdefault('add_time', order.add_time.strftime('%Y-%m-%d %H:%M:%S'))
                order_dic.setdefault('trade_status', order.get_trade_status_display())
                order_dic.setdefault('trade_no', order.trade_no)
                order_dic.setdefault('trade_type', order.get_pay_mode_display())
                orders_list.append(order_dic)

            try:
                paginator = Paginator(orders_list, limit)  # 分页，每页显示limit个
                order_list = paginator.page(int(page_id))
                order_list = [i for i in order_list]  # 将数据从Page对象中遍历出来
                page_count = paginator.count
            except:
                logger.error(traceback.format_exc())
                return response_utils.wrapper_400('分页失败')

            return response_utils.wrapper_200(data=order_list, args=('count',page_count))
        except Exception as e:
            logger.error(traceback.format_exc())
            return response_utils.wrapper_500('获取订单记录失败，系统内部错误')


class OrderDetail(View):
    '''获取个人订单详情页面'''

    def get(self, request):
        try:
            user = request.user
            types = Goods().type.gets()
            order_no = request.GET.get('order_no')

            if not user:
                return render(request, 'ac_order/order_detail.html', {'msg': '获取用户对象失败'})

            order = Order().order.get(user=user, order_no=order_no)  # 条件：用户，订单号
            if not order:
                return render(request, 'ac_order/order_detail.html', {'msg': '获取订单信息失败'})

            order_dic = {}
            order_dic.setdefault('order_no', order.order_no)
            order_dic.setdefault('price', str(order.price))
            order_dic.setdefault('total_price', order.total_price)
            order_dic.setdefault('count', order.count)
            order_dic.setdefault('add_time', order.add_time.strftime('%Y-%m-%d %H:%M:%S'))
            order_dic.setdefault('trade_status', order.get_trade_status_display())
            order_dic.setdefault('trade_no', order.trade_no)
            order_dic.setdefault('trade_type', order.get_pay_mode_display())

            data = {}
            data['types'] = types
            data['name'] = user.name
            data['order_dic'] = order_dic
            return render(request, 'ac_order/order_detail.html', data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return render(request, 'error.html', {'error': '500'})


class GoodsDetail(View):
    '''单个订单所有数据返回'''

    def get(self, request):
        try:
            # 获取参数
            page_id = request.GET.get('page', 1)
            order_no = request.GET.get('order_no', None)
            limit = request.GET.get('limit', 5)

            # 条件：用户、订单、交易状态
            accounts = Goods().account.gets(Q(order__trade_status=2) | Q(order__trade_status=3),
                                            order__order_no=order_no)
            if not accounts:
                return response_utils.wrapper_400('无商品信息')

            goods_list = []
            for index, account in enumerate(accounts):
                account_dic = {}
                info = str(account.price).split(':')
                account_dic.setdefault('id', index + 1)
                account_dic.setdefault('order_no', order_no)
                account_dic.setdefault('type', info[0])
                account_dic.setdefault('account_str', account.account_str)
                account_dic.setdefault('price', info[1])
                account_dic.setdefault('sale_time', account.sale_time.strftime('%Y-%m-%d %H:%M:%S'))
                goods_list.append(account_dic)

            try:
                paginator = Paginator(goods_list, limit)  # 分页，每页显示limit个
                good_list = paginator.page(int(page_id))
                good_list = [i for i in good_list]  # 将数据从Page对象中遍历出来
                page_count = paginator.count  # 页码总数
            except Exception as e:
                logger.error(traceback.format_exc())
                return response_utils.wrapper_400('分页失败')

            return response_utils.wrapper_200(data=good_list, args=('count',page_count))
        except Exception as e:
            logger.error(traceback.format_exc())
            return response_utils.wrapper_500('获取订单详情信息失败，系统内部错误')
