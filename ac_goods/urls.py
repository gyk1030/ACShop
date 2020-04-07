# Author:gyk
from django.conf.urls import url
from ac_goods import views


urlpatterns = [
    # url('^index/(\d+)', views.index, name='index'),
    url('^index/', views.IndexView.as_view(), name='index'),
    url('^detail/', views.GoodsDetailView.as_view(), name='detail'),
    # url('^gen_order/(\d+)', views.CreateOrderView.as_view(), name='gen_order'),
    # url('^time_out', views.time_out, name='time_out'),
    url('', views.error)
]
