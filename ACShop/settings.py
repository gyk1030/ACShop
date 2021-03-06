"""
Django settings for ACShop project.

Generated by 'django-admin startproject' using Django 2.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p#j2&d(6jilv*b21gfp755n1ma^qg1sue4!i!_q#jbx&)ifb8^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ac_user.apps.AcUserConfig',
    'ac_order.apps.AcOrderConfig',
    'ac_goods.apps.AcGoodsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.AuthenticateMiddleware'
]

ROOT_URLCONF = 'ACShop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ACShop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'acshop',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': 3306
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# 静态文件夹
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static'),
    os.path.join(BASE_DIR,'media')
]

# 存放用户上传的文件、头像
MEDIA_ROOT=os.path.join(BASE_DIR,'media')

# 指定用户表
AUTH_USER_MODEL = "ac_user.UserInfo"

# 云片网apikey
APIKEY = '57ca89c4b286e82d56db94434b4f4f79'

# session过期时间
SESSION_COOKIE_AGE = 8*3600+60

# 邮箱相关配置
HOST = 'smtp.163.com'  # 设置邮箱的域名
SUBJECT = '【账号网】'  # 设置邮件标题
FROM = '13572551532@163.com'  # 设置发件人邮箱


# 支付相关配置
APP_ID = '2016101000651666'
ALIPAY_GETWAY = 'https://openapi.alipaydev.com/gateway.do'
APP_PRIVATE_KEY_PATH = 'ac_order/KEYS/app-private-2048.txt'  # 应用私钥
ALIPAY_PUBLIC_KEY_PATH = 'ac_order/KEYS/alipay-public-2048.txt'  #支付宝公钥
RETURN_URL = 'http://127.0.0.1:8000/order/Pay/'  # 同步回调地址
NOTIFY_URL = 'http://127.0.0.1:8000/goods/index/'  # 异步回调地址


# 不进行身份验证url
EXCEPT_URL = ['/login/','/register/','/users/code_auth/','/acshop/admin.*',]
EXCEPT_URL_GET = ['/goods/index/','/goods/detail/','/users/get_code/','/uses/send_email/',
                  '/users/reset_pwd/','/static/.*','/media/.*',]

# 订单/支付二维码超时时间(min)
ORDER_TIMEOUT = 0.5
TIME_OUT_EXPRESS = 2


# celery相关配置
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 43200}  # 设置超时时间，一定要设置
BACKEND='redis://127.0.0.1:6379/3'
BROKER='redis://127.0.0.1:6379/4'


# 日志相关配置
LOG_NAME = 'acshop.log'
LOG_PATH = os.path.join(BASE_DIR , 'log' , LOG_NAME)


# 是否为linux环境
LINUX_ENV = False


# 允许售卖延时时间（h）
ALLOW_SALE_TIME = 8