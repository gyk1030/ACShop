from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse

from ac_user.myforms import RegForms, ResetForms, PerForms
from common.chackData import User, Order, Goods
from django.db.models import Q

from django.contrib.auth import login as logg
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import logout

from ACShop.settings import FROM, SUBJECT, HOST
from common.utils import CustomBackend, gen_code_num
# from common.authenticate import Authenticate,get_user
from common.emails import to_send
from common.yunpian import YunPian
from common.pictureCode import gen_code

from django.views import View

class UserViewset(View):
    '''注册视图'''
    def get(self,request):
        return render(request, 'ac_user/register.html')
    def post(self,request):
        response = {'status': 100, 'msg': None}
        forms = RegForms(request, request.POST)

        if forms.is_valid():
            dic = forms.cleaned_data
            dic.pop('re_pwd')
            dic.pop('code')
            User().user.create(**dic)
            response['msg'] = '注册成功'
            response['url'] = '/login/'
        else:
            response['status'] = 101
            response['msg'] = '注册失败'
            response['errors'] = forms.errors
            print(forms.errors)
        return JsonResponse(response)

class LoginViewset(View):
    '''登录视图'''
    def get(self,request):
        return render(request, 'ac_user/login.html')
    def post(self,request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_code = request.POST.get('valid_code')
        # 从session中取出验证码,跟提交的验证码做比较
        # 忽略大小写
        if valid_code.upper() == request.session['valid_code']:
            auth = CustomBackend()  # 实例化自定义验证类
            user = auth.authenticate(request, username=username, password=password)
            if user:
                print('验证成功.....')
                logg(request, user)
                request.session['user'] = user.id
                return redirect('/goods/index/')
            else:
                error = '用户名或密码错误'
                return render(request, 'ac_user/login.html', {'error': error})
        else:
            error = '验证码错误'
            return render(request, 'ac_user/login.html', {'error': error})

# 登出
def log_out(request):
    logout(request)
    return redirect('/login/')


# 重置密码
class ResetPwdViewset(View):
    def get(self,request):
        return render(request, 'ac_user/reset_pwd.html')
    def post(self,request):
        response = {'status': 100, 'msg': None}

        forms = ResetForms(request, request.POST)
        if forms.is_valid():
            dic = forms.cleaned_data
            print(dic)
            email = dic['email']
            password = dic['password']
            password = make_password(password)
            User().user.gets(email=email).update(password=password)
            response['msg'] = '密码修改成功'
            response['url'] = '/login/'
        else:
            response['status'] = 101
            response['msg'] = '密码修改失败'
            response['errors'] = forms.errors
        return JsonResponse(response)


# 个人资料信息返回
class PersonalViewset(View):
    def get(self,request):
        # user = Authenticate(request)
        user = request.user
        types = Goods().type.gets()
        user_data = {}
        if user:
            user_data['name'] = user.name
            user_data['username'] = user.username
            user_data['email'] = user.email
            user_data['sex'] = user.sex
            user_data['birth'] = str(user.birth) if user.birth else ''
            user_data['address'] = user.address if user.address else ''
            return render(request, 'ac_user/personal.html', {'types': types, 'name': user.name, 'user': user_data})

    def post(self,request):
        user = request.user
        types = Goods().type.gets()
        info = {'status': 100, 'msg': {}}
        if user:
            forms = PerForms(request, request.POST)
            if forms.is_valid():
                forms.cleaned_data.pop('old_pwd')
                forms.cleaned_data.pop('re_pwd')
                User().user.gets(username=user).update(**forms.cleaned_data)
                return redirect('/users/personal/')
            else:
                info['status'] = 101
                info['msg'].setdefault('errors', forms.errors)
                all_error = forms.errors.get('__all__')
                if all_error:
                    all_error = all_error[0]
                info['msg']['all_error'] = all_error if all_error else ''
                return render(request, 'ac_user/personal.html', {'types': types, 'info': info})
        else:
            info['msg'] = '信息修改成功'
            return render(request, 'ac_user/personal.html', {'types': types, 'info': info})


# 购买信息页面返回
@login_required(login_url='/login/')
def payed(request):
    user = request.user
    types = Goods().type.gets()
    if request.method == 'GET':
        return render(request, 'ac_user/payed.html', {'name': user.name, 'types': types, })


# 购买信息数据返回
@login_required(login_url='/login/')
def payed_info(request):
    n = 1
    if request.method == 'GET':
        user = request.user
        page_id = request.GET.get('page', 1)
        limit = request.GET.get('limit', 10)
        accounts_list = []
        accounts_dic = {'code': 0, 'msg': None, 'count': 0, 'data': None}
        if user:
            orders = Order().order.gets(Q(trade_status=2 or 3), user=user)
            for order in orders:
                for account in order.account.all():
                    account_dic = {}
                    info = str(account.price).split(':')
                    account_dic.setdefault('id', n)
                    account_dic.setdefault('order_no', order.order_no)
                    account_dic.setdefault('type', info[0])
                    account_dic.setdefault('account_str', account.account_str)
                    account_dic.setdefault('price', info[1])
                    account_dic.setdefault('sale_time', account.sale_time.strftime('%Y-%m-%d %H:%M:%S'))
                    accounts_list.append(account_dic)
                    n += 1

                paginator = Paginator(accounts_list, limit)  # 分页，每页显示limit个
                try:
                    account_list = paginator.page(int(page_id))
                    account_list = [i for i in account_list]  # 将数据从Page对象中遍历出来
                    page_count = paginator.count
                    accounts_dic['count'] = page_count
                    accounts_dic['data'] = account_list
                except:
                    pass
        return JsonResponse(accounts_dic)


# 获取图片验证码
def get_code(request):
    data, code_str = gen_code()
    print(code_str)
    request.session['valid_code'] = code_str.upper()  # 把验证码放到session
    return HttpResponse(data)


# 发送邮件
def send_email(request):
    # 发送邮件
    info = {'stu': 101, 'msg': '发送失败'}
    if request.method == 'POST':
        email = request.POST.get('email', None)
        ret = User().user.gets(isDelete=False, email=email).exists()
        print(email)
        if ret:
            code = gen_code_num(6)
            print(code)
            send_res, msg = to_send(code, email, FROM, SUBJECT, HOST)
            if send_res:
                request.session[email] = code
                info['stu'], info['msg'] = 100, msg
            else:
                info['msg'] = msg
        else:
            info['msg'] = '该邮箱未被注册'
    return JsonResponse(info)


# 发送短信验证码
def code_auth(request):
    info = {'stu': 101, 'msg': '发送失败'}
    if request.method == 'POST':
        phone = request.POST.get('phone')
        code = gen_code_num(4)  # 调用生成随机验证码
        print(code)
        try:
            yun_pian = YunPian('APIKEY')  # 实例化
            sms_status = yun_pian.send_sms(code, phone)  # 接收云片网发来的状态码，0表成功，其他代表错误
            if sms_status['code'] != 0:  # ==0是才成功///记着改回来
                request.session[phone] = code
                info['stu'], info['msg'] = 100, '发送成功'
        except Exception as e:
            info['msg'] = '发送短信验证码失败'
        return JsonResponse(info)
    if request.method == 'GET':
        return JsonResponse('请求无效')


# 错误页面
def error(request):
    return render(request, '404.html')
