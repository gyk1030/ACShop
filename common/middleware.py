# Author:gyk

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from ACShop.settings import EXCEPT_URL_GET,EXCEPT_URL
import re


class AuthenticateMiddleware(MiddlewareMixin):
    '''用户认证'''
    def process_request(self,request):
        user = request.user
        # if request.path.startswith('/admin/'):
        #     return None
        for i in EXCEPT_URL:
            if re.findall(i,request.path):
                return None
        for i in EXCEPT_URL_GET:  # 部分页面只放行get请求
            if (re.findall(i,request.path) and request.method == 'GET') or user.is_authenticated:
                return None
        return redirect('/login/')
