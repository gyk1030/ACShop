# Author:gyk

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from ACShop.settings import EXCEPT_URL_GET,EXCEPT_URL_POST
import re


class AuthenticateMiddleware(MiddlewareMixin):
    '''用户认证'''
    def process_request(self,request):
        user = request.user
        print(request.path)
        # if request.path in EXCEPT_URL_POST:  # 如登录、注册、忘记密码页面等包括get和post请求的全部放行
        #     return None
        for i in EXCEPT_URL_POST:
            if re.findall(i,request.path):
                return None
        for i in EXCEPT_URL_GET:  # 部分页面只放行get请求
            if (re.findall(i,request.path) and request.method == 'GET') or user.is_authenticated:
                return None
        return redirect('/login/')
