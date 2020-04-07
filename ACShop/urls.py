"""ACShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from ACShop import settings
from django.views.static import serve
from ac_user.views import LoginViewset,UserViewset


from django.shortcuts import render
def ceshi(request):
    return render(request,'测试.html')
def ceshi1(request):
    return render(request,'测试1.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    url('^login/$', LoginViewset.as_view(), name='login'),
    url('^register/$', UserViewset.as_view(), name='register'),
    url('^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    path('goods/', include('ac_goods.urls')),
    path('users/', include('ac_user.urls')),
    path('order/', include('ac_order.urls')),

    path('',ceshi),
    path('1/',ceshi1)
    # url('^get_code/$', views.get_code, name='get_code'),
]
