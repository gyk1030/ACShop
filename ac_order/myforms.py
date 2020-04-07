from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from ac_order import  models
from ac_goods import  models as mod


class OrderForms(forms.Form):
    price_id = forms.CharField( error_messages={'required': '该字段必填'})
    count = forms.CharField(error_messages={'required': '该字段必填'})

    def clean_price_id(self):
        self.num_sum = 0
        price_id = self.cleaned_data.get('price_id')
        if price_id.isdigit():
            obj = mod.UnitPrice.objects.filter(pk=price_id).first()
            if obj:
                self.price = obj.price
                self.num_sum = obj.account_set.count()
                return self.price
        raise ValidationError('输入有误')

    def clean(self):
        count = self.cleaned_data.get('count')
        if count and count.isdigit():
            if self.num_sum >= int(count):
                return self.cleaned_data
            else:
                raise ValidationError('库存不足')
        raise ValidationError('输入有误')







