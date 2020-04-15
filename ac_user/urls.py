# Author:gyk
from django.conf.urls import url
from ac_user import views
from common.utils import err404

urlpatterns = [
    url('^personal/$', views.PersonalList.as_view(), name='personal'),
    url('^reset_pwd/$', views.ResetPwd.as_view(), name='reset_pwd'),
    url('^payed/$', views.PayedPage.as_view(), name='payed'),
    url('^payed_info/$', views.PayedList.as_view(), name='payed_info'),

    url('^get_code/$', views.get_code, name='get_code'),
    url('^code_auth/$', views.code_auth, name='code_auth'),
    url('^send_email/$', views.send_email, name='send_email'),
    url('^log_out/$', views.log_out, name='log_out'),
    url('.*', err404)
]
