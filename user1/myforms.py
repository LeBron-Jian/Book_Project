from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError

from user1 import models

widget_input = widgets.TextInput(attrs={'class': 'form-control'})
widget_num = widgets.NumberInput(attrs={'class': 'form-control'})
widget_password = widgets.PasswordInput(attrs={'class': 'form-control'})

class PublisherForm(forms.Form):
    name = forms.CharField(
        label='出版社名称',
        min_length=4,
        max_length=32,
        error_messages={
            'required': '不能为空',
            'min_length': '不能小于4位',
        },
        widget=widget_input
    )

    def clean_name(self):
        val = self.cleaned_data.get('name')
        if not val.isdigit():
            return val
        else:
            raise ValidationError('名称不能是纯数字')

class AuthorForm(forms.Form):
    name = forms.CharField(
        label='姓名',
        min_length=2,
        max_length=16,
        error_messages={
            'required': '不能为空',
            'min_length': '不能小于2位',
        },
        # widget = widget_input,
    )
    age = forms.IntegerField(
        label='年龄',
        min_value=1,
        max_value=150,
        error_messages={
            'required': '不能为空',
            'invalid': '格式错误',
            'min_value': '不能小于1岁',
            'max_value': '不能大于100岁',
        },
        # widget = widget_input,
    )
    addr = forms.CharField(
        label='地址',
        min_length=2,
        max_length=32,
        error_messages={
            'required': '不能为空',
            'min_length': '不能小于两位',
        },
        # widget = widget_input,
    )

    # 给每一key 添加一个样式
    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.field[field].widget.attrs.update({
                'class': 'form-control'
            })

    def clean_name(self):
        val = self.cleaned_data.get('name')
        if not val.isdigit():
            return val
        else:
            raise ValidationError("姓名不能是纯数字")

    def clean_addr(self):
        val = self.cleaned_data.get('addr')
        if not val.isdigit():
            return val
        else:
            raise ValidationError("地址不能是纯数字")

class BookForm(forms.Form):
    title = forms.CharField(
        label='书名称',
        max_length=32,
        error_messages={
            'required': '不能为空',
        },
        widget=widget_input
    )
    price = forms.DecimalField(
        label='价格',
        max_digits=8,
        decimal_places=2,
        error_messages={
            'required': '不能为空',
            'max_digits': '不能超过8位',
        },
        widget=widget_num
    )
    '''
    # 最后选择自己去添加select
    publisher = forms.ChoiceField(
        label='出版社',
        # choices=((1, '篮球'), (1, '足球')),
        choices=models.Publisher.objects.all().values_list('id', 'name'),
        initial=1,
        widget=widgets.Select(attrs={'class': 'form-control'})
    )
    # 可以不用重启，刷新就有新的数据
    def __init__(self,*args,**kwargs):
        super(BookForm, self).__init__(*args,**kwargs)
        self.fields['publisher'].widget.choice = 
        models.Publisher.objects.all().values_list('id','name')
    
    '''

    def clean_title(self):
        val = self.cleaned_data.get('title')
        if not val.isdigit():
            return val
        else:
            raise ValidationError("名称不能为纯数字")

    def clean_price(self):
        val = self.cleaned_data.get('price')
        if val < 0:
            raise ValidationError("价格不能为负数")
        else:
            return val

class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        min_length=2,
        max_length=16,
        error_messages={
            'required': '不能为空',
            'min_length': '不能小于2位'
        },
        widget=widget_input

    )

    password = forms.CharField(
        label='密码',
        min_length=2,
        max_length=16,
        error_messages={
            'required': '不能为空',
            'min_length': '不能小于2位'
        },
        widget=widget_password
    )

    def clean_username(self):
        val = self.cleaned_data.get('username')
        if not val.isdigit():
            return val
        else:
            raise ValidationError("用户名不能是纯数字")

