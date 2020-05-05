import traceback

from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
from django.core.paginator import Paginator
from django.views import View
from rest_framework.decorators import api_view

from ACShop.settings import FROM, SUBJECT, HOST, APIKEY
from ac_user.myforms import RegForms, ResetForms, PerForms
from common.chackData import User, Order, Goods
from common.utils import CustomBackend, gen_code_num, get_name
from common.emails import to_send
from common.yunpian import YunPian
from common.pictureCode import gen_code
from common import response_utils
from common.logg import Logger

logger = Logger()


class Register(View):
    '''注册视图'''

    def get(self, request):
        return render(request, 'ac_user/register.html')

    def post(self, request):
        try:
            forms = RegForms(request, request.POST)
            if not forms.is_valid():
                return response_utils.wrapper_400(forms.errors or '注册失败')

            data = {}
            dic = forms.cleaned_data
            dic.pop('re_pwd')
            dic.pop('code')

            resp = User().user.create(**dic)
            if not resp:
                return response_utils.wrapper_400('创建用户失败')

            data['url'] = '/login/'
            logger.info('{0}注册成功'.format(dic.get('username')))
            return response_utils.wrapper_200(data=data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return response_utils.wrapper_500('注册失败，系统内部错误！')


class Login(View):
    '''登录视图'''

    def get(self, request):
        return render(request, 'ac_user/login.html')

    def post(self, request):
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            valid_code = request.POST.get('valid_code')
            if not (username and password and valid_code):
                return render(request, 'ac_user/login.html', {'error': '参数缺失!'})

            # 从session中取出验证码,跟提交的验证码做比较，忽略大小写
            if valid_code.upper() == request.session.get('valid_code'):
                auth = CustomBackend()  # 自定义验证类
                user = auth.authenticate(request, username=username, password=password)
                if not user:
                    return render(request, 'ac_user/login.html', {'error': '用户名或密码错误!'})

                print('验证成功.....')
                login(request, user)
                request.session['user'] = user.id
                return redirect('/goods/index/')
            else:
                error = '验证码错误'
                return render(request, 'ac_user/login.html', {'error': error})
        except Exception as e:
            logger.error(traceback.format_exc())
            return response_utils.wrapper_500('登录失败，系统内部错误！')


class ResetPwd(View):
    '''重置密码'''

    def get(self, request):
        return render(request, 'ac_user/reset_pwd.html')

    def post(self, request):
        try:
            response = {'status': 100, 'msg': None}

            forms = ResetForms(request, request.POST)
            if not forms.is_valid():
                return response_utils.wrapper_400(forms.errors or '参数格式错误！')

            dic = forms.cleaned_data
            print(dic)
            email = dic['email']
            password = dic['password']
            password = make_password(password)  # 为密码加密
            resp = User().user.gets(email=email).update(password=password)
            if not resp:
                return response_utils.wrapper_400('密码修改失败')
            response['msg'] = '密码修改成功'
            response['url'] = '/login/'

            return response_utils.wrapper_200(data=response)
        except Exception as e:
            logger.error(traceback.format_exc())
            return response_utils.wrapper_500('修改密码失败，系统内部错误！')


class PersonalList(View):
    '''个人资料信息返回'''

    def get(self, request):
        try:
            user = request.user
            types = Goods().type.gets()
            user_data = {}
            data = {}
            if not user:
                data['msg'] = '获取用户对象失败'
                return render(request, 'ac_user/personal.html', data)

            user_data['name'] = user.name
            user_data['username'] = user.username
            user_data['email'] = user.email
            user_data['sex'] = user.sex
            user_data['birth'] = str(user.birth) if user.birth else ''
            user_data['address'] = user.address if user.address else ''

            data['types'] = types
            data['name'] = user.name
            data['user'] = user_data

            return render(request, 'ac_user/personal.html', data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return render(request, 'error.html', {'error': 500})

    def post(self, request):
        try:
            user = request.user
            types = Goods().type.gets()
            data = {}
            if not user:
                data['msg'] = '获取用户对象失败'
                return render(request, 'ac_user/personal.html', data)

            forms = PerForms(request, request.POST)
            if forms.is_valid():
                forms.cleaned_data.pop('old_pwd')
                forms.cleaned_data.pop('re_pwd')
                if not forms.cleaned_data.get('password'):
                    forms.cleaned_data.pop('password')
                User().user.gets(username=user).update(**forms.cleaned_data)
                return redirect('/users/personal/')
            else:
                data['errors'] = forms.errors
                all_error = forms.errors.get('__all__')
                if all_error:
                    all_error = all_error[0]
                data['all_error'] = all_error if all_error else ''
                data['types'] = types
                return render(request, 'ac_user/personal.html', data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return render(request, 'error.html', {'error': 500})


class PayedPage(View):
    '''购买信息页面返回'''

    def get(self, request):
        try:
            name = get_name(request)
            types = Goods().type.gets()

            data = {}
            data['name'] = name
            data['types'] = types
            return render(request, 'ac_user/payed.html', data)
        except Exception as e:
            logger.error(traceback.format_exc())
            return render(request, 'error.html', {'error': 500})


class PayedList(View):
    '''购买信息数据返回'''

    def get(self, request):
        try:
            user = request.user
            page_id = request.GET.get('page', 1)
            limit = request.GET.get('limit', 10)
            if not user:
                return response_utils.wrapper_400('获取用户对象失败')

            orders = Order().order.gets(Q(trade_status=2) | Q(trade_status=3), user=user)
            if not orders:
                return response_utils.wrapper_400('无订单信息')

            accounts_list = []
            index = 0
            for order in orders:
                for account in order.account.all():
                    index += 1
                    account_dic = {}
                    info = str(account.price).split(':')
                    account_dic.setdefault('id', index)
                    account_dic.setdefault('order_no', order.order_no)
                    account_dic.setdefault('type', info[0])
                    account_dic.setdefault('account_str', account.account_str)
                    account_dic.setdefault('price', info[1])
                    account_dic.setdefault('sale_time', account.sale_time.strftime('%Y-%m-%d %H:%M:%S'))
                    accounts_list.append(account_dic)

            try:
                paginator = Paginator(accounts_list, limit)  # 分页
                account_list = paginator.page(int(page_id))
                account_list = [i for i in account_list]  # 将数据从Page对象中遍历出来
                page_count = paginator.count
            except Exception as e:
                logger.error(traceback.format_exc())
                return response_utils.wrapper_400('分页失败')

            return response_utils.wrapper_200(data=account_list, args=('count', page_count))
        except Exception as e:
            logger.error(traceback.format_exc())
            return response_utils.wrapper_500('获取已购买商品信息失败，系统内部错误')


@api_view(['GET'])
def log_out(request):
    '''登出'''
    try:
        logout(request)
        return redirect('/login/')
    except Exception as e:
        logger.error(traceback.format_exc())
        return redirect('/login/')


@api_view(['GET'])
def get_code(request):
    '''获取图片验证码'''
    try:
        data, code_str = gen_code()
        print(code_str)
        request.session['valid_code'] = code_str.upper()  # 把验证码放到session
        return HttpResponse(data)
    except Exception as e:
        logger.error(traceback.format_exc())
        return HttpResponse('')


@api_view(['POST'])
def send_email(request):
    '''发送邮件'''
    # if request.method == 'POST':
    try:
        email = request.POST.get('email')
        if not email:
            return response_utils.wrapper_400('参数缺失email')

        ret = User().user.gets(email=email).exists()
        if not ret:
            return response_utils.wrapper_400('该邮箱未注册')

        code = gen_code_num(6)  # 生成6为数字验证码
        print(code)
        send_res, msg = to_send(code, email, FROM, SUBJECT, HOST)
        if not send_res:
            return response_utils.wrapper_400(msg)

        request.session[email] = code
        return response_utils.wrapper_200()
    except Exception as e:
        logger.error(traceback.format_exc())
        return response_utils.wrapper_500('发送邮件失败，系统内部错误')


@api_view(['POST'])
def code_auth(request):
    '''发送短信验证码'''
    # if request.method == 'POST':
    try:
        phone = request.POST.get('phone')
        code = gen_code_num(4)  # 调用生成随机验证码
        print(code)
        yun_pian = YunPian('APIKEY')  # 实例化
        sms_status = yun_pian.send_sms(code, phone)  # 接收云片网发来的状态码，0表成功，其他代表错误
        if sms_status['code'] != 0:  # ==0是才成功///记着改回来
            request.session[phone] = code
            return response_utils.wrapper_200()
        return response_utils.wrapper_400('发送验证码失败')
    except Exception as e:
        logger.error(traceback.format_exc())
        return response_utils.wrapper_500('发送验证码失败，服务器内部错误')
