import os
from celery import Celery
from django.conf import settings
from ACShop.settings import BACKEND, BROKER

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ACShop.settings")

cel = Celery('ac_goods', backend=BACKEND, broker=BROKER)

cel.config_from_object('django.conf:settings')
cel.autodiscover_tasks(lambda: settings.INSTALLED_APPS)