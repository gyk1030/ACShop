# Author:gyk
from django.conf.urls import url
from ac_goods import views
from common.utils import err404

urlpatterns = [
    url('^index/', views.GoodsList.as_view(), name='index'),
    url('^detail/', views.GoodsDetail.as_view(), name='detail'),
    url('.*', err404)
]

