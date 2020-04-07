"""
WSGI config for ACShop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ACShop.settings')  # 将当前文件设置为django项目的模块
application = get_wsgi_application()  # 注册所有app

# 第三方py文件要想导入django项目的模块，必须有上面两行代码
