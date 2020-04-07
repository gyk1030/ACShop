from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from ac_order import  models
from ac_goods.models import UnitPrice


class OrderForms(forms.Form):
    '''订单数据校验'''
    price_id = forms.CharField( error_messages={'required': '请选择类型'})
    count = forms.CharField(error_messages={'required': '请填写数量'})

    def __init__(self,data):
        super(OrderForms,self).__init__(data)
        self.num_sum = 0

    def clean_price_id(self):
        self.price_id = self.cleaned_data.get('price_id')
        if self.price_id and self.price_id.isdigit():
            obj = UnitPrice.objects.filter(pk=self.price_id,isDelete=False).first()
            if obj:
                price = obj.price
                self.num_sum = obj.account.filter(isSale=0).count()
                return self.price_id,price
        raise ValidationError('输入有误')

    def clean(self):
        count = self.cleaned_data.get('count')
        if count and count.isdigit() and int(count)>0:
            if self.num_sum >= int(count):
                return self.cleaned_data
            else:
                raise ValidationError('库存不足')
        raise ValidationError('输入有误')







