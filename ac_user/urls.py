# Author:gyk
from django.conf.urls import url
from ac_user import views
from common.utils import err404

urlpatterns = [
    url('^personal/$', views.PersonalViewset.as_view(), name='personal'),
    url('^get_code/$', views.get_code, name='get_code'),
    url('^code_auth/$', views.code_auth, name='code_auth'),
    url('^reset_pwd/$', views.ResetPwdViewset.as_view(), name='reset_pwd'),
    url('^send_email/$', views.send_email, name='send_email'),
    url('^log_out/$', views.log_out, name='log_out'),
    url('^payed/$', views.payed, name='payed'),
    url('^payed_info/$', views.payed_info, name='payed_info'),
    url('.*', err404)
]
