from django import forms
from django.core.exceptions import ValidationError
from ac_user import models
from django.contrib import auth
import re
from django.contrib.auth.hashers import make_password


class CommForms(forms.Form):
    '''通用（登录注册）检验字段'''
    email = forms.EmailField(label='邮箱', error_messages={'invalid': '邮箱格式错误',
                                                         'required': '该字段必填'})
    password = forms.CharField(min_length=3, max_length=13, label='密码',
                               error_messages={'min_length': '密码太短', 'max_length': '密码太长',
                                               'required': '该字段必填'})
    re_pwd = forms.CharField(min_length=3, max_length=13, label='确认密码',
                             error_messages={'min_length': '密码太短', 'max_length': '密码太长',
                                             'required': '该字段必填'})

    def __init__(self, request, data):
        super(CommForms, self).__init__(data)
        self.request = request

    # 全局钩子函数（校验两次密码是否一致）
    def clean(self):
        password = self.cleaned_data.get('password')
        re_pwd = self.cleaned_data.get('re_pwd')
        if password != re_pwd:
            raise ValidationError('密码不一致')
        elif password and re_pwd:
            password = make_password(password)  # 为新密码加密
            self.cleaned_data['password'] = password
        else:
            raise ValidationError('密码不能为空')
        return self.cleaned_data


class RegForms(CommForms):
    '''注册数据校验'''
    code = forms.CharField(min_length=4, max_length=4,
                           error_messages={'min_length': '验证码太短', 'max_length': '验证码太长',
                                           'required': '验证码为空'})
    username = forms.CharField(min_length=11, max_length=11, label='手机号',
                               error_messages={'min_length': '手机号太短', 'max_length': '手机号太长',
                                               'required': '该字段必填'})

    def clean_code(self):
        ucode = self.cleaned_data.get('code')
        username = self.request.POST.get('username')
        code = self.request.session.get(username)
        print(code, ucode)
        if code == ucode:
            return code
        else:
            raise ValidationError('验证码错误')

    # 局部钩子函数（校验该用户名在数据库已经存在）
    def clean_username(self):
        # self 是当前forms对象，cleaned_data是清洗后的数据，从字典中取出name
        username = self.cleaned_data.get('username')
        user = models.UserInfo.objects.filter(isDelete=False, username=username).first()
        if user:
            raise ValidationError('该手机号已经被注册')
        else:
            return username

    def clean_email(self):
        # self 是当前forms对象，cleaned_data是清洗后的数据，从字典中取出name
        email = self.cleaned_data.get('email')
        user = models.UserInfo.objects.filter(isDelete=False, email=email).first()
        if user:
            raise ValidationError('该邮箱已经被注册')
        else:
            return email


class ResetForms(CommForms):
    '''重置密码数据校验'''
    code = forms.CharField(min_length=4, max_length=4,
                           error_messages={'min_length': '验证码太短', 'max_length': '验证码太长',
                                           'required': '验证码为空'})

    def clean_code(self):
        code = self.cleaned_data.get('code')
        email = self.request.POST.get('email')
        ucode = self.request.session.get(email)
        if code == ucode:
            return ucode
        else:
            raise ValidationError('验证码错误')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = models.UserInfo.objects.filter(isDelete=False, email=email).first()
        if user:
            return email
        else:
            raise ValidationError('该邮箱还未被注册')


class PerForms(CommForms):
    '''个人信息修改数据校验'''
    name = forms.CharField(min_length=3, max_length=10, label='昵称',
                           error_messages={'min_length': '昵称太短', 'max_length': '昵称太长',
                                           'required': '该字段必填'})
    old_pwd = forms.CharField(min_length=3, max_length=20, label='旧密码',
                              error_messages={'min_length': '密码太短', 'max_length': '密码太长',
                                              'required': '该字段必填'})
    sex = forms.IntegerField(error_messages={'invalid': '数据格式错误'})
    birth = forms.DateField(error_messages={'invalid': '日期格式错误'})
    address = forms.CharField(min_length=3, max_length=30, label='地址',
                              error_messages={'min_length': '地址太短', 'max_length': '地址太长', })

    def __init__(self, request, data):
        super(PerForms, self).__init__(request, data)
        self.request = request
        self.fields['password'].required = False  # 非空允许
        self.fields['re_pwd'].required = False
        self.fields['birth'].required = False
        self.fields['address'].required = False

    def clean_old_pwd(self):
        old_pwd = self.cleaned_data.get('old_pwd')
        user = self.request.user
        user = auth.authenticate(self.request, username=user, password=old_pwd)
        if user:
            return old_pwd
        else:
            raise ValidationError('密码错误')

    def clean_sex(self):
        sex = self.cleaned_data.get('sex')
        if sex not in [0,1]:
            raise ValidationError('性别数据错误')
        else:return sex

    def clean_birth(self):
        birth = self.cleaned_data.get('birth')
        if not birth:
            return birth
        else:
            clean_birth = re.findall('\d{4}-\d{2}-\d{2}',str(birth))
            if not clean_birth:
                raise ValidationError('时间格式不正确')
            return birth

