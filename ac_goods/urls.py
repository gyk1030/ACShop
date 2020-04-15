# Author:gyk
from django.conf.urls import url
from ac_goods import views
from common.utils import err404

urlpatterns = [
    # url('^index/(\d+)', views.index, name='index'),
    url('^index/', views.GoodsList.as_view(), name='index'),
    url('^detail/', views.GoodsDetail.as_view(), name='detail'),
    # url('^gen_order/(\d+)', views.CreateOrderView.as_view(), name='gen_order'),
    # url('^time_out', views.time_out, name='time_out'),
    url('.*', err404)
]

