#!/usr/bin/python
#-*- coding:utf8 -*-
#BY:  H.c
from hc import models
from django.forms import Form      # 继承类的时候 需要用到
from django.forms import fields    #
from django.forms import widgets

# 使用系统封装好的 forms 表单
class RegisterForm(Form):        # TextInput 和 PasswordInput 是系统定义好的
    username = fields.CharField(
        required= True ,
        min_length= 2,     #输入的最小字节数
        max_length= 8,     #输入的最大字节数
        error_messages= {'required':'用户名不能为空'},  # 报错的信息
        widget = widgets.TextInput(attrs={'class':'form-control'})  # 前端的输入框
    )
    password = fields.CharField(
        min_length= 2,
        max_length=10,
        error_messages={'required':'密码不能为空'},
        widget = widgets.PasswordInput(attrs={'class':'form-control'})
    )
    # password_again = fields.CharField(
    #     min_length=2,
    #     max_length=10,
    #     error_messages={'required':'确认密码不能为空'},
    #     widget = widgets.PasswordInput(attrs={'class':'form-control'})   # 确认密码的输入框
    # )
    # def clean(self):
    #     try:
    #         pwd = self.cleaned_data['password']    # 取到密码信息
    #         pwd_again = self.cleaned_data['password_again']  #取到 确认密码的信息
    #         if pwd == pwd_again:
    #             del self.cleaned_data['password_again']  # 如果数据库里 没有这个字段，不删除这个信息就会报错
    #             return  self.cleaned_data          # 一样的 则正确返回
    #         else:
    #             from django.core.exceptions import ValidationError   # 如果不对加载内置模块
    #             self.add_error('password_again',ValidationError('密码输入不一致'))
    #             return  self.cleaned_data
    #     except KeyError as e:
    #         return self.cleaned_data




#   创建数据 form表单
class HostForm(Form):
    hostname = fields.CharField(
                required = True ,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    ecsname = fields.CharField(
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    login_port = fields.IntegerField(
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    cpu = fields.IntegerField(
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    mem = fields.IntegerField(      # 存入的类型不一样，所以这里要 IntagerField
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    speed = fields.IntegerField(
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    eth1_network =fields.CharField(
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    eth0_network =fields.CharField(
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    sn = fields.CharField(
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    kernel = fields.CharField(
                required = True,
                widget=widgets.TextInput(attrs={'class': 'form-control','style':'color: green;'})
                )
    remarks = fields.CharField(
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    createtime = fields.CharField(
                required = True,
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'})
                )
    expirytime = fields.CharField(
                required=True,
                widget=widgets.TextInput(attrs={'class': 'form-control','style':'color: green;'})
                )
    state = fields.IntegerField(
                required= True,
                min_value=1,
                max_value=4,   # 允许输入的值，最为1，最大为4
                widget = widgets.TextInput(attrs={'class':'form-control','style':'color: green;'}),
                )
    # ForeignKey
    # state_id = fields.ChoiceField(
    #             required= True,
    #             choices=[],
    #             widget = widgets.Select(attrs={'class': 'form-control'})
    #             )
    lab_id = fields.ChoiceField(
                required = True,
                choices = [],
                widget = widgets.Select(attrs={'class': 'form-control','style':'color: green;'})
                )
    os_id = fields.ChoiceField(
                required = True,
                choices = [],
                widget = widgets.Select(attrs={'class':'form-control','style':'color: green;'})
                )
    source_id = fields.ChoiceField(
                required = True,
                choices  = [],
                widget = widgets.Select(attrs={'class':'form-control','style':'color: green;'})
                )
    region_id = fields.ChoiceField(     # 一对多的 region_id 字段不加_id 时会报错
                required = True,   # 因为 fields.CharField 渲染的input的框是，输入的都是str()类型，ID 又是唯一的所有这里
                choices = [],      # 所有插数据的时候 str() 和int() 数据类型不一样会报错
                # choices = models.Region.objects.values_list('id','name'),    # values_list这里取到的还是int()
                                                # values_list 通过这个方法可以拿到元组 即 ('id','name')
                # form.cleaned_data['region'] = int(form.cleaned_data['region'])
                # 可以这么理解。但是最好别这样用，一对多数据多了的时候 就很麻烦
                #  所有最好的方法就是 在source  后面 加个 _id  即可  ->  source_id  插入数据时就不会报错
                widget = widgets.Select(attrs={'class':'form-control','style':'color: green;'})  # 加样式是 通过 form-control 修改
                )
    #login_port = fields.CharField()   M2M 没写

    def __init__(self, *args, **kwargs):
        super(HostForm, self).__init__(*args, **kwargs)   # 先执行 父类的 __init__方法，也就是 View类的__init__方法
        # self.fields['state_id'].choices = models.Host.objects.values_list('id', 'state_choices')
        self.fields['lab_id'].choices = models.Lable.objects.values_list('id','name')  # 列表
        self.fields['os_id'].choices = models.Os.objects.values_list('id','name')
        self.fields['source_id'].choices = models.Source.objects.values_list('id','name')
        self.fields['region_id'].choices = models.Region.objects.values_list('id','name')
        # 这个 self.fields 值 是执行父类初始化__init__时产生的，会把当前这个子类的所有字段值，当成属性做了次深度copy
        # 成一个字典，然后用过切片取值。重新将.choices 赋值，赋值的是后面一对多查表的值。
        # 这种方法 不用重启服务，当DB数据更新时，也会自动刷入表单渲染





#   创建岗位用户 form表单
class PosUser_Form(Form):
    name = fields.CharField(
        required= True ,
        min_length= 2,     #输入的最小字节数
        max_length= 8,     #输入的最大字节数
        error_messages= {'required':'用户名不能为空'},  # 报错的信息
        widget = widgets.TextInput(attrs={'class':'form-control'})  # 前端的输入框
    )
    passwd = fields.CharField(
        min_length= 2,
        max_length=10,
        error_messages={'required':'密码不能为空'},
        widget = widgets.PasswordInput(attrs={'class':'form-control'})
    )
    passwd_t = fields.CharField(
        min_length=2,
        max_length=10,
        error_messages={'required':'确认密码不能为空'},
        widget = widgets.PasswordInput(attrs={'class':'form-control'})   # 确认密码的输入框
    )
    pos_id = fields.ChoiceField(     # 一对多的 region_id 字段不加_id 时会报错
                required = True,   # 因为 fields.CharField 渲染的input的框是，输入的都是str()类型，ID 又是唯一的所有这里
                choices = [],      # 所有插数据的时候 str() 和int() 数据类型不一样会报错
                widget = widgets.Select(attrs={'class':'form-control'})  # 加样式是 通过 form-control 修改
                )                #SelectMultiple 多选框

    def __init__(self, *args, **kwargs):
        super(PosUser_Form, self).__init__(*args, **kwargs)   # 先执行 父类的 __init__方法，也就是 View类的__init__方法
        self.fields['pos_id'].choices = models.Position.objects.values_list('id','name') # 列表

    def clean(self):
        user_name = self.cleaned_data.get('name')
        if user_name:
            try:
                pwd = self.cleaned_data['passwd']  # 取到密码信息
                pwd_again = self.cleaned_data['passwd_t']  #取到 确认密码的信息
                if pwd == pwd_again:
                    del self.cleaned_data['passwd_t']  # 如果数据库里 没有这个字段，不删除这个信息就会报错
                    user_obj = models.UserInfo.objects.filter(name=user_name).first()
                    if not user_obj:   # 判断用户是否已创建
                        return  self.cleaned_data          # 一样的 则正确返回
                    else:
                        from django.core.exceptions import ValidationError  # 如果不对加载内置模块  创建岗位
                        self.add_error('passwd_t', ValidationError('该用户已被创建, 请修改创建的用户名！ \n'))
                        return self.cleaned_data
                else:
                    from django.core.exceptions import ValidationError   # 如果不对加载内置模块
                    self.add_error('passwd_t',ValidationError('密码输入不一致！ \n'))
                    return  self.cleaned_data
            except KeyError as e:
                return self.cleaned_data



#   创建岗位  form表单
class Pos_Form(Form):
    name = fields.CharField(
        required= True ,
        min_length= 2,     #输入的最小字节数
        max_length= 8,     #输入的最大字节数
        error_messages= {'required':'岗位名不能为空'},  # 报错的信息
        widget = widgets.TextInput(attrs={'class':'form-control'})  # 前端的输入框
    )
    name_id = fields.MultipleChoiceField(     # 一对多的 region_id 字段不加_id 时会报错
                required = True,   # 因为 fields.CharField 渲染的input的框是，输入的都是str()类型，ID 又是唯一的所有这里
                choices = [],      # 所有插数据的时候 str() 和int() 数据类型不一样会报错
                widget = widgets.SelectMultiple(attrs={'class':'form-control','style':'height: 200px;'})  # 加样式是 通过 form-control 修改
                )                #SelectMultiple 多选框  请正确选择该岗位对应的用户

    def __init__(self, *args, **kwargs):
        super(Pos_Form, self).__init__(*args, **kwargs)   # 先执行 父类的 __init__方法，也就是 View类的__init__方法
        self.fields['name_id'].choices = models.UserInfo.objects.values_list('id','name')  # 列表
        (self.fields['name_id'].choices).insert(0,(0, '选择此处，只创建岗位，暂时不添加用户'))

    def clean(self):
        pos_name = self.cleaned_data.get('name')
        if pos_name:
            try:
                pos_obj = models.Position.objects.filter(name=pos_name).first()
                if not pos_obj:  # 判断  岗位 是否已创建
                    return  self.cleaned_data          # 一样的 则正确返回
                else:
                    from django.core.exceptions import ValidationError  # 如果不对加载内置模块  创建岗位
                    self.add_error('name', ValidationError('该岗位已创建, 请修改创建的岗位名. \n'))
                    return self.cleaned_data
            except KeyError as e:
                return self.cleaned_data

