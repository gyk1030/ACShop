from django.contrib import admin

# Register your models here.

from ac_user.models import UserInfo


@admin.register(UserInfo)  # 注册admin
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['pk','name']
    # list_display = ['pk','username','user','email']  # list_display定义所要显示的字段
    # list_display_links = ['username']  # 定义admin在当前界面内不可直接修改的字段，需要link到另一个界面修改
    # search_fields = ['username']

