from django.contrib import admin

# Register your models here.

from ac_goods.models import TypeInfo,LevelInfo,UnitPrice,Account




@admin.register(TypeInfo)  # 注册admin
class TypeInfoAdmin(admin.ModelAdmin):
    list_display = ['pk','title','isDelete']  # list_display定义所要显示的字段
    list_editable = ['isDelete']  # 定义在admin当前界面内可修改的字段
    list_display_links = ['title']  # 定义admin在当前界面内不可直接修改的字段，需要link到另一个界面修改


@admin.register(LevelInfo)
class LevelInfoAdmin(admin.ModelAdmin):
    list_display = ['pk','name','isDelete']
    list_editable = ['isDelete']
    list_display_links = ['name']

    # 多对多不能直接显示，需要借助方法查询后返回，type是任意起的方法名
    # def type(self,obj):
    #     return [i.title for i in obj.type.all()]  # type_info是跨表的字段


@admin.register(UnitPrice)
class UnitPriceAdmin(admin.ModelAdmin):
    list_display = ['pk','type','level','price','currency','unit']
    list_display_links = ['type']


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['pk','price','account_str','add_time','allow_sale_time','sale_time','isSale','isDelete']
    list_editable = ['isDelete']
    list_display_links = ['account_str']
    search_fields = ['pk','account_str']
    ordering = ['add_time']