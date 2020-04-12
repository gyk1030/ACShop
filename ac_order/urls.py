# Author:gyk
from django.conf.urls import url
from ac_order import views
from common.utils import err404

urlpatterns = [
    url('^order_pay/', views.OrderPayView.as_view(), name='order_pay'),  # 订单支付处理

    url('^Pay/', views.PayView.as_view()),  # 支付接口
    url('^goods_info/', views.GoodsDetail.as_view(),name='goods_info'),  # 单个订单所有账号信息接口
    url('^kill_order/', views.KillOrder.as_view(),name='kill_order'),  # 订单超时未支付，删除订单
    url('^chack/', views.ChackView.as_view(),name='chack'),  # 查询订单支付后结果

    url('^ordered/', views.Ordered.as_view(),name='ordered'),  # 个人订单页面
    url('^order_info/', views.OrderInfo.as_view(),name='order_info'),  # 个人订单页面数据接口
    url('^order_detail/', views.OrderDetail.as_view(),name='order_detail'),  # 个人订单页面单个订单

    url('.*', err404)
]

