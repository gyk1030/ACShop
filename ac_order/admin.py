from django.contrib import admin

# Register your models here.

from ac_order.models import OrderInfo


@admin.register(OrderInfo)  # 注册admin
class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['pk','order_no','user','total_price','count','add_time','trade_status','trade_no','isDelete']  # list_display定义所要显示的字段
    list_editable = ['trade_status','isDelete']  # 定义在admin当前界面内可修改的字段
    list_display_links = ['order_no']  # 定义admin在当前界面内不可直接修改的字段，需要link到另一个界面修改
    search_fields = ['pk', 'user']

