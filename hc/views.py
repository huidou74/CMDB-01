from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from hc import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse  # 反向 URL
# from django.forms import Form, fields, widgets      # 继承类的时候 需要用到
from hc.form.form_class import *
from hc.jiami.jiami import *
from hc_auth import auth_data
# import json

from django.db.models import Q
from lyh_project import settings
from io import BytesIO
from hc.login_verify import check_code
# Create your views here.


def Code(request):
    img_obj, code = check_code.create_validate_code()
    stream = BytesIO()
    img_obj.save(stream, 'png')
    request.session[settings.CODEIMG] = code
    return HttpResponse(stream.getvalue())

# 主页
def index(request):
    if request.method == 'GET':
        if request.session['login'] :
            tag = 'login'
            tem = 'index'
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)

                    tag = 'auto_user'
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')

                    return render(request, './bootstarp/index.html', locals())
            else:

                pos, userinfo, img = '无权限,请登录', '普通用户', 'images/in.jpg'
                return render(request, './bootstarp/index.html', locals())
        else:
            return redirect('./bootstarp/host/login.html')


# 使用 form 表单 注册+ 渲染
def register(request):
    if request.method == 'GET':
        form = RegisterForm()   ## 实例化RegisterForm类
        return render(request, 'register.html',{'form':form})
    else :
        form = RegisterForm(request.POST)
        if form.is_valid():   #判断是否符合 实例化类的 规则
            # print(form.cleaned_data)   {'username': 'aa', 'password': '123'}
            username = form.cleaned_data['username']  #  判断 用户是否存在
            if_user = models.Login.objects.filter(username=username).first()
            if not if_user:
                password = form.cleaned_data['password']
                pwd = Jiami()  # 实例化对象
                password = pwd.base_str_encrypt(password)  # base64 加密
                form.cleaned_data.update({'password':password})  # 更新进去字典
                # print (form.cleaned_data) {'username': 'aa', 'password': 'c2hpYGJ1c2hpYFNCQHBpbGUxMjN3bytfO14lI2JhYmE=\n'}
                models.Login.objects.create(**form.cleaned_data)  # 以字典方式可以多个创建用户信息
                return render(request,'register_ok.html',locals())
            else:
                error = '该用户已存在'
                return render(request, 'error.html', locals())
        else:
            print(form.errors)  # 如何没通过验证，则会在errors 里面加了一些错误信息。然后返回前端显示
        return render(request, 'register.html', locals())


# 使用 form 表单 登录+ 渲染
def login(request):
    if request.method == 'GET':
        if request.session.get('login') :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                tem = 'index'
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')
                    return render(request, './bootstarp/index.html', locals())
        else :
            form = RegisterForm()   ## 实例化RegisterForm类
            return render(request, './bootstarp/host/login.html',locals())
    elif request.method == 'POST':

        form = RegisterForm(request.POST)
        if form.is_valid():   #判断是否符合 实例化类的 规则
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            pwd = Jiami()    # 实例化对象
            password = pwd.base_str_encrypt(password)    # base64 加密 然后查表
            user_obj = models.Login.objects.filter(username=username,
                                                    password=password)

            if user_obj.first():
                request.session['login'] = user_obj.first().username  # 加入 session 信息
                request.session.set_expiry(0)  # 意思就是关闭浏览器就清掉session, (10) 就是10秒

                # template标记
                tem = 'index'
                # 验证码比对
                code = request.POST.get('code').upper()
                if request.session[settings.CODEIMG].upper() != code:
                    mes_error = '验证码错误！ 请重新输入！'
                # 头像信息
                else:
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')

                    if not userinfo:
                        tag='login'
                        pos,userinfo,img ='无权限,请登录', '普通用户', 'images/in.jpg'
                    return render(request, './bootstarp/index.html', locals())
            else:
                mes_error = '账号或密码输入错误，请重新输入！'
                # return render(request, './bootstarp/host/login.html', locals())
        else:
            a = form.errors  # 如何没通过验证，则会在errors 里面加了一些错误信息。然后返回前端显示
        return render(request, './bootstarp/host/login.html', locals())

def reload_pwd(request):
    if request.method == 'GET':
        return render(request, 'reload.html',locals())
    elif request.method == 'POST':
        username = request.POST.get('username')    # 先取到 表单的用户名
        user = models.Login.objects.filter(username=username).first()  # 去查表 ，判断
        if user:
            password = str(user.password)   #  通过user 可以点出同表另外一个字段，将其转化成字符串
            print (password)          # 查看
            pwd = Jiami()     # 实例化对象
            new_pwd = pwd.base_str_decrypt(password)  # base64 解密
            print (new_pwd)       # 查看
            # return HttpResponse('该 '+ username + ' 用户的密码是： '+ new_pwd)
            error = '找回密码：  -->   该 '+ username + ' 用户的密码是： '+ new_pwd
            return render(request, 'error.html', locals())
        else:
            return HttpResponse('没有该用户，请正确输入！')


# form 表单方式 写 增改删  form + CBV -> 分页搞定 -> host_list.html
class List(View):
    def get(self, request, *args, **kwargs):
        # host_list = models.Host.objects.all()
        host_list = models.Host.objects.get_queryset().order_by('-id')
        p = Paginator(host_list, 10)

        get_p = request.GET.get('page', 1)  # get 到了就返回get的值， get不到了就返回1
        # print (hosts_page.number)  # 当前页码
        # print('数据总数:  ', p.count)  # 页码总数
        # print('数据页数:  ', p.num_pages)  # 当前页码
        # print('range(x, y):  ', p.page_range)  # 从多少页 到多少页
        # print('是否有下一页:  ', p.page(2).has_next())  # 是否有下一页
        # print('是否有上一页:  ', p.page(2).has_previous())  # 是否有上一页
        # print('是否有其他页:  ', p.page(2).has_other_pages())  # 是否有其他页
        # print('下一页的页码:  ', p.page(2).next_page_number())  # 下一页的页码
        # print('上一页的页码:  ', p.page(2).previous_page_number())  # 上一页的页码

        try:
            hosts_page = p.page(get_p)
        except PageNotAnInteger:
            hosts_page = p.page(1)
        except EmptyPage:
            hosts_page = p.page(p.num_pages)
        # return render(request, 'host_list.html',locals())
        menu_dict = request.session.get('menu_dict')
        # print (menu_dict)
        userinfo = request.session.get('auto_user')
        pos = request.session.get('auto_user_pos')
        img = request.session.get('auto_user_img')
        tem = 'form'

        list_tab = ['主机名', '实例名', 'CPU', '内存/G', '带宽/M', '登录端口', '公网IP', '操作系统', '全部']
        obj = models.Host.objects.all()

        q = request.GET.get('q')
        opt = request.GET.get('form')
        if q and opt:
            if opt == '主机名':
                obj_list = models.Host.objects.all().filter(Q(hostname__startswith=q))
                if not obj_list:
                    error = '查询结果为空! 请重新输入查询条件'
                print(obj_list)
                print(opt)
                return render(request, './bootstarp/host/list.html', locals())
            elif opt == '实例名':
                obj_list = models.Host.objects.all().filter(Q(ecsname__startswith=q))
                if not obj_list:
                    error = '查询结果为空! 请重新输入查询条件'
                print(obj_list)
                print(opt)
                return render(request, './bootstarp/host/list.html', locals())
            elif opt == 'CPU':
                if isinstance(q, int):
                    obj_list = models.Host.objects.all().filter(Q(cpu__startswith=int(q)))
                    print(obj_list)
                    print(opt)
                else :
                    error = '输入有误'
                return render(request, './bootstarp/host/list.html', locals())
            elif opt == '内存/G':
                if isinstance(q, int):
                    obj_list = models.Host.objects.all().filter(Q(mem__startswith=int(q)))
                    print(obj_list)
                    print(opt)
                else :
                    error = '输入有误'
                return render(request, './bootstarp/host/list.html', locals())
            elif opt == '带宽/M':
                if isinstance(q, int):
                    obj_list = models.Host.objects.all().filter(Q(speed__startswith=int(q)))
                    print(obj_list)
                    print(opt)
                else :
                    error = '输入有误'
                return render(request, './bootstarp/host/list.html', locals())
            elif opt == '登录端口':
                if isinstance(q,int):
                    obj_list = models.Host.objects.all().filter(Q(login_port__startswith=int(q)))
                    print(obj_list)
                    print(opt)
                else :
                    error = '输入有误'
                return render(request, './bootstarp/host/list.html', locals())
            elif opt == '公网IP':
                obj_list = models.Host.objects.all().filter(Q(eth1_network__startswith=q))
                if not obj_list:
                    error = '查询结果为空! 请重新输入查询条件'
                print(obj_list)
                print(opt)
                return render(request, './bootstarp/host/list.html', locals())
            elif opt == '操作系统':
                obj_list = models.Host.objects.all().filter(Q(os__name__startswith=q))
                if not obj_list:
                    error = '查询结果为空! 请重新输入查询条件'
                print(obj_list)
                print(opt)
                return render(request, './bootstarp/host/list.html', locals())
            elif opt == '全部':
                obj_list = models.Host.objects.all().filter(Q(ecsname=q) |
                                                            Q(hostname__startswith=q) |
                                                            Q(ecsname__startswith=q) |
                                                            Q(cpu__startswith=q) |
                                                            Q(mem__startswith=q) |
                                                            Q(speed__startswith=q) |
                                                            Q(login_port__startswith=q) |
                                                            Q(eth1_network__startswith=q) |
                                                            Q(os__name__startswith=q)
                                                            )
                if not obj_list:
                    error = '查询结果为空! 请重新输入查询条件'
                print(obj_list)
                print(opt)
                return render(request, './bootstarp/host/list.html', locals())

        return render(request, './bootstarp/host/list.html',locals())

    def post(self, request, *args, **kwargs):
        pass



# 添加主机数据   完成
class Add(View):
    def get(self, request,  *args, **kwargs):
        form = HostForm()
        message = '温馨提示，这里请正确填写对应数字，1: running ; 2: 下线 ; 3: 关机 ; 4: 删除'

        menu_dict = request.session.get('menu_dict')
        userinfo = request.session.get('auto_user')
        pos = request.session.get('auto_user_pos')
        img = request.session.get('auto_user_img')

        return render(request, './bootstarp/host/add.html', locals())

    def post(self, request,  *args, **kwargs):
        form = HostForm(data=request.POST)   # 将页面POST 上来的数据 给HostForm data = request.POST 并且实例化

        if form.is_valid():         # 验证提交的数据
            print (form.cleaned_data)   # 这 是我页面提交验证过的信息，是个大字典
            models.Host.objects.create(**form.cleaned_data)  # 通过他们form 表单自带的 cleaned_data 方法吧字典传入自动创建
            return  redirect('/host/list/')
        else:
            print (form.errors)     # 验证不过则返回 错误信息，是个带标签的信息
            return render(request,'./bootstarp/host/add.html',locals())


# 更新编辑数据    完成
class Update_Form(View):
    def get(self, request, pk):
        if request.session['login'] :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')
                    # print (pk)  # 前端 点击 编辑的ID
                    host_obj = models.Host.objects.filter(id=int(pk)).first()
                    form = HostForm(
                        initial = {
                            'hostname': host_obj.hostname,
                            'ecsname': host_obj.ecsname,
                            'login_port': host_obj.login_port,
                            'cpu': host_obj.cpu,
                            'mem': host_obj.mem,
                            'speed': host_obj.speed,
                            'eth1_network': host_obj.eth1_network,
                            'eth0_network': host_obj.eth0_network,
                            'sn': host_obj.sn,
                            'kernel': host_obj.kernel,
                            'remarks': host_obj.remarks,
                            'createtime': host_obj.createtime,
                            'expirytime': host_obj.expirytime,
                            'lab_id': host_obj.lab_id,
                            'os_id': host_obj.os_id,
                            'source_id': host_obj.source_id,
                            'region_id': host_obj.region_id,
                            'state': host_obj.state,
                        }
                    )
                    message = '温馨提示，这里请正确填写对应数字，1: running ; 2: 下线 ; 3: 关机 ; 4: 删除'
                    return render(request,'./bootstarp/host/add.html',locals())

    def post(self, request, pk):
        if request.session['login'] :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')

                    form = HostForm(data=request.POST)
                    if form.is_valid():
                        models.Host.objects.filter(id=int(pk)).update(**form.cleaned_data)
                        return redirect('/host/list/')
                    else:
                        return render(request,'./bootstarp/host/add.html',locals())



class Delete(View):   # 完成 删除
    def get(self, request ,pk, *args,**kwargs):
        print (pk)
        models.Host.objects.filter(id=int(pk)).delete()
        return redirect('/host/list/')   # 跳回当前页面
    def post(self):
        pass

class Mes_Host(View):
    def get(self, request, pk):
        if request.session['login'] :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')
                    ####  下面才是我的逻辑

                    host_obj = models.Host.objects.filter(id=int(pk)).first()

                    if host_obj:
                        logining = host_obj.logining  # 所属用户

                        for i in logining.all():  # 多对多 跨表查询
                            login = i.username
                            print (login)
                        disks = host_obj.disks.all()  # 查询磁盘

                        for x in disks:
                            disk = x.size
                            print (disk)
                        return render(request,'./bootstarp/host/mes.html',locals())
    def post(self, request):
        pass



# # 判断页面是否有session的装饰器
# def if_login(func):
#     def wapper(request):
#         if request.session.get('login', False):
#             return func(request)
#         else:
#             return  redirect('/login.html')
#     return wapper

# @if_login


#   注销 用户 OK
# 删除session
def delete_session(request):
    request.session.clear()
    get_session = request.session.get('login','Logout Successfully!')
    return redirect('./bootstarp/host/login.html')


# 登录验证的 CBV方法
# class Auth(View):
#     def dispatch(self, request, *args, **kwargs):
#         if request.session.get('login', False):
#             response = super(Auth, self).dispatch(request, *args, **kwargs)
#             return response
#         else:
#             return redirect('/login.html')
#
# class Index(Auth):
#     def get(self,request):
#         return render(request,'user.html')
#
# class Login(View):
#     def get(self,request):
#         return render(request, 'login.html')
#
#     def post(self,request):
#         username = request.POST.get('username', False)
#         password = request.POST.get('password', False)
#         passwd_ture = request.POST.get('password_ture')
#         if not username or not password or not passwd_ture:
#             return HttpResponse('输入不能为空！ 请正确输入！')
#         else:
#             if password == passwd_ture:
#                 user_obj =  models.Login.objects.filter(username=username,password=password)
#                 if user_obj.first():
#                     request.session['login'] = user_obj.first().username   # 加入 session 信息
#                     return render(request,'user.html',locals())
#                 else:
#                     error = username + ' 用户名或密码错误！ 请重新填写！'
#                     return render(request, 'error.html', locals())
#             elif password != passwd_ture:
#                 error = username + ' 两次输入的密码不同！ 请重新填写密码！'
#                 return render(request,'error.html',locals())
#         return render(request, 'login.html')



# def login(request):
#     if request.method   == 'POST':
#         user = request.POST.get('username')     #这里的两个是从template取过来的，即用户输入从的内容
#         passwd = request.POST.get('password')
#         passwd_ture = request.POST.get('password_ture')
#         a = models.Login.objects.filter(username=user).first()
#         if a and (passwd == passwd_ture):
#             if models.Login.objects.filter(password=passwd).first():
#                 return render(request, 'user.html', locals())
#             else:
#                 error = user + ' 密码输入错误！  请输入正确密码！'
#                 return render(request,'error.html',locals())
#         elif not a :
#             error = user + ' 用户名不存在！  请输入正确的用户名！'
#             return render(request, 'error.html', locals())
#         elif passwd != passwd_ture:
#             error = user + ' 两次输入的密码不同！ 请重新填写密码！'
#             return render(request, 'error.html', locals())
#     return render(request,'login.html')


# 注册的 FBV 方法
# def register(request):
#     if request.method == 'POST':
#         user = request.POST.get('username')  # 这里的两个是从template取过来的，即用户输入从的内容
#         passwd = request.POST.get('password')
#         passwd_ture = request.POST.get('password_ture')
#         # print(user,type(user))
#         # print (passwd)
#         a = models.Login.objects.filter(username=user).first()
#         # print (a,type(a))
#         if user != str(a) and (passwd == passwd_ture):
#             print (a,type(a))
#             obj = models.Login.objects.create(username=user,password=passwd)
#             return render(request, 'register_ok.html', locals())
#         elif (not str(a)) and (not passwd):
#             error = user + ' 用户名或者密码不能为空！'
#             return render(request, 'error.html', locals())
#         elif passwd != passwd_ture:
#             error = user + ' 两次输入的密码不同！ 请重新填写密码！'
#             return render(request, 'error.html', locals())
#         else:
#             error = user + ' 用户名已存在！  请输入重新定义用户名！'
#             return render(request, 'error.html', locals())
#     return render(request, 'register.html', locals())




#下面 基本都FBV 方法

# @if_login

#  展示所有 用户

# 用户数据页面
def date(request):
    date_all = models.Login.objects.all()
    num = len(date_all)
    return render(request,'date.html',locals())


# 修改密码  完成
def update(request):
    if request.method == 'POST':
        names = request.POST.get('name')
        old_passwd = request.POST.get('old_passwd')
        new_passwd = request.POST.get('new_passwd')
        date_name = models.Login.objects.filter(username=names).first()
        # date_passwd = models.Login.objects.filter(password=old_passwd).first() # 这里的密码是通过查找的用户 点 出来的密码
        if names == str(date_name):
            if old_passwd == date_name.password:
                obj = models.Login.objects.filter(username=names).update(password=new_passwd)
                user = names
                passwd = new_passwd
                return render(request,'update_ok.html',locals())
            elif old_passwd != date_name.password:
                error = "尊敬的用户： "+names + "您好！\n  原始密码输入错误，请返回重新输入！"
                return render(request,'error.html',locals())
        elif names != str(date_name):
            error = "尊敬的用户： "+names + "您好！\n  用户名不存在，请返回重新输入！"
            return render(request, 'error.html', locals())
    return render(request,'update.html',locals())


 #  删除用户可以了
def delete(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        password = request.POST.get('passwd')
        passwd = request.POST.get('passwd')
        pwd = Jiami()
        passwd = pwd.base_str_encrypt(passwd)
        y_n = request.POST.get('y_n').lower()
        date_user = models.Login.objects.filter(username=user).first()
        if user == str(date_user):
            if passwd == date_user.password:
                if y_n == 'yes' or y_n == 'y':
                    obj = models.Login.objects.filter(username=user).delete()
                    print(obj, type(obj))
                    return render(request, 'delete_ok.html', locals())
                elif y_n == 'no' or y_n == 'n':
                    error = "尊敬的用户： "+user + "您好！\n  您的确认结果为  否，不删除用户！"
                    return render(request, 'error.html', locals())
            elif passwd != date_user.password:
                error = "尊敬的用户： "+user + "您好！\n  原始密码输入错误，请返回重新输入！"
                return render(request, 'error.html', locals())
        elif user != str(date_user):
            error = "尊敬的用户： "+user + "您好！\n  用户名不存在，请返回重新输入！"
            return render(request, 'error.html', locals())

    return render(request,'delete.html',locals())


# @if_login
#   所有 host 的分页   可以了
def host(request):
    # Django分页出现UnorderedObjectListWarning: Pagination may yield inconsistent results with an unordered ob
    # 需要吧 objects.all()  改成 objects.get_queryset().order_by('id') 即可
    # hosts = models.Host.objects.all()
    # messeges = MessegeModel.objects.get_queryset().order_by('id')
    hosts = models.Host.objects.get_queryset().order_by('id')
    p = Paginator(hosts,10)

    # print('数据总数:  ', p.count)  # 页码总数
    # print('数据页数:  ', p.num_pages)  # 当前页码
    # print('range(x, y):  ', p.page_range)  # 从多少页 到多少页
    # print('是否有下一页:  ', p.page(2).has_next())  # 是否有下一页
    # print('是否有上一页:  ', p.page(2).has_previous())  # 是否有上一页
    # print('是否有其他页:  ', p.page(2).has_other_pages())  # 是否有其他页
    # print('下一页的页码:  ', p.page(2).next_page_number())  # 下一页的页码
    # print('上一页的页码:  ', p.page(2).previous_page_number())  # 上一页的页码

    get_p = request.GET.get('page',1)  # get 到了就返回get的值， get不到了就返回1

    try:
        hosts_page = p.page(get_p)
    except PageNotAnInteger:
        hosts_page = p.page(1)
    except EmptyPage:
        hosts_page = p.page(p.num_pages)

    return render(request , 'page.html', locals())


# @if_login
#   单个主机的详情  可以了
def messages(request):

    host = request.GET.get('all',False)
    if host :
        host_obj = models.Host.objects.filter(hostname=host).first()   # 数据查询 queryset
        if host_obj:
            logining = host_obj.logining.all()   # 所属用户
            for i in logining:     # 多对多 跨表查询
                login = i.username
            disks = host_obj.disks.all()   #  查询磁盘
            for i in disks:
                disk = i.size
            return render(request, 'host_messages.html',locals())
        else:
            # url = request.GET.get('all')
            # print (url)
            user = request.GET.get('all').split('/')[0]    # url 的拼接  好像没用到过。。
            user_obj = models.Host.objects.filter(hostname=user).first()
            if user_obj:
                path = '/host/messages/update_db/?all='+ user
                return redirect(path)
            else:
                return HttpResponse('温馨提示：  不许瞎几把 乱改链接路径 哦！')
    else:
        user = request.GET.get('all',False)
        user_obj = models.Host.objects.filter(hostname=user).first()
        if user_obj:
            path = '/host/messages/update_db/?all=' + user
            return redirect(path)
        else:
            return render(request , 'user.html')


from hc.api.salt_api import SaltApi
from hc.api.json_class import Json_dict
from lyh_project.settings import *
#  一键获取数据

def add_all_hosts(request):

    if request.method == 'GET':
        salt = SaltApi(API)
        data = salt.salt_command(SALT_TEST, SALT_CLIENT)
        orm = Json_dict(data, DATA_LIST, MES_DICT)
        rom_list = orm.for_data_values()
        for i in rom_list:
            for k in i.keys():
                if k == 'os_id':
                    os_jg = models.Os.objects.filter(name=i.get(k)).first()   # 先去找os 有没有，有就找ID，没有就创建
                    if os_jg:
                        os_id = os_jg.id
                        i.update({'os_id':os_id})
                    else:
                        models.Os.objects.create(name=i.get(k))
            models.Host.objects.create(**i)
        return redirect('/host/list/')


# @if_login
# 更新数据   可以了 ， 分开 特殊的字段
def update_db(request):
    user = request.GET.get('all')
    if request.method == 'GET':
        attr = models.Attr.objects.exclude(id__in=[5,12,13,16,17])
        host_obj = models.Host.objects.filter(hostname=user).first()
        disk = [i.size for i in (host_obj.disks.all())][0]  # 列表重写方式直接切割出字符串 <class 'str'>
        login = [i.username for i in (host_obj.logining.all())][0]  # manytomany  多对多
        return render(request,'update_db.html',locals())
    elif request.method == 'POST':
        id = request.POST.get('class')
        mes = request.POST.get('message')       # 拉取 post 表单数据是可以加判断用户数据类型的正确项。现在没时间写了就 省略
        if  mes :
            print (mes)
            data = models.Attr.objects.filter(id=int(id)).first()  # 拿到对应的属性
            print(user,data, mes)   # 用户， 数据， 修改的信息
            print ('=======================================')
            p = Update(user=user,data=data,id=id,mes=mes)
            status = p.start()
            if status == 1:
                path = '/host/messages/update_db/?all=' + user
                return redirect(path)
            elif status == 0:
                return HttpResponse('修改数据失败,请正确输入信息')
            else :
                return HttpResponse('温馨提示：   修改数据时出现未知错误 ')
        else:
            return HttpResponse('温馨提示： 输入信息不能为空 ')
    else:
        return HttpResponse("温馨提示：  不许瞎几把 乱改链接路径 哦！")


# 一对多 和多对多的修改  完成
def update_attr(request):
    user = request.GET.get('all')   #  主机
    attr = request.GET.get('attr')    # 原值，页面取到的值 如 中文的 ‘磁盘’
    value = request.GET.get('value')   # 属性
    dict1 = {'disk': 5, 'os': 12, 'source': 13, 'login': 16, 'lable': 17}  # 这是 ID
    dict2 = {'id': dict1.get(value.lower())}  # 取到 ID 值
    path = '/host/messages/update_db/?all=' + user
    obj_u = models.Host.objects.filter(hostname=user).first()  # 先在 host表里找到 主机
    if request.method == 'GET':                        # GET 搞定了 准备POST 的 一 对多关系的改
        attr_new = models.Attr.objects.filter(**dict2)    # 就返回一个 特殊属性值
        attr_disk = models.Disk.objects.all()
        attr_login = models.Login.objects.all()
        attr_os = models.Os.objects.all()
        attr_source = models.Source.objects.all()
        attr_lable = models.Lable.objects.all()
        return render(request,'attr_upate.html',locals())    # 返回  OK 正常！
    elif request.method == 'POST':
        if value == 'Disk':     # 多对多关系 disk
            id_disk = int(request.POST.get('class_disk'))  # 从页面POST获取 id -> 再指向disk的ID
            # obj_u = models.Host.objects.filter(hostname=user).first()  # 先在 host表里找到 主机
            disk_obj = models.Disk.objects.filter(id=id_disk)  # 再去 disk表里找到 对应ID 的字段信息
            obj_u.disks.clear()  # 多对多的修改关系是 先 clear 再 add
            obj_u.disks.add(*disk_obj)   # 更新的是 hc_host_disks 表的关系
            return redirect(path)    # 拼接链接 返回更新到数据的单个主机详细表
        elif value == 'Login':      # 多对多关系 login
            id_login = int(request.POST.get('class_login'))  # 从页面POST获取 id -> 再指向disk的ID
            # obj_u = models.Host.objects.filter(hostname=user).first()  # 先在 host表里找到 主机
            login_obj = models.Login.objects.filter(id=id_login)  # 再去 disk表里找到 对应ID 的字段信息
            obj_u.logining.clear()  # 多对多的修改关系是 先 clear 再 add
            obj_u.logining.add(*login_obj)  # 更新的是 hc_host_disks 表的关系
            return redirect(path)  # 拼接链接 返回更新到数据的单个主机详细表
        elif value == 'Os':
            id_os = int(request.POST.get('class_os'))    # 从页面POST获取 id -> 再指向disk的ID
            os_obj = models.Host.objects.filter(hostname=user).update(os_id=id_os)  # 先查询该用户，然后再更新对应OS 的ID
            # print (os_obj)    #通过修改ID 来改变它原有的属性
            return redirect(path)  # 拼接链接 返回更新到数据的单个主机详细表
        elif value == 'Source':
            id_source = int(request.POST.get('class_source'))  # 从页面POST获取 id -> 再指向disk的ID
            print (id_source)
            source_obj = models.Host.objects.filter(hostname=user).update(source_id=id_source)  # 先查询该用户，然后再更新对应source 的ID
            # print(source_obj)  # 通过修改ID 来改变它原有的属性
            return redirect(path)  # 拼接链接 返回更新到数据的单个主机详细表
        elif value == 'Lable':
            id_lable = int(request.POST.get('class_lable'))  # 从页面POST获取 id -> 再指向disk的ID
            lable_obj = models.Host.objects.filter(hostname=user).update(lab_id=id_lable)  # 先查询该用户，然后再更新对应lable 的ID
            # print(lable_obj)  # 通过修改ID 来改变它原有的属性
            return redirect(path)  # 拼接链接 返回更新到数据的单个主机详细表

        return HttpResponse('OK')



# @if_login
def create_db(request):
    user = request.GET.get('all')
    if request.method == 'GET':
        attr = models.Attr.objects.exclude(id__in=[5,12,13,16,17])
        return render(request, 'create_db.html', locals())
    elif request.method == 'POST':
        host = request.POST.get('hostname')
        attr = models.Attr.objects.exclude(id__in=[5,12,13,16,17])
        dic1 = {'hostname':host}
        if_host = models.Host.objects.filter(**dic1).first()
        if if_host :
            messages = host + '  该用户已存在，请重新创建！！'
            return HttpResponse(messages)
        for i in attr:
            user_attr = request.POST.get(i.name)   # 比如 '实例名':
            dic = {str(i.db_name.name):str(user_attr)}  #转成字典 扔到 我update 类里 执行
            dic1.update(dic)
        dic1['state'] = 3   # 主机状态
        # print (dic1)
        models.Host.objects.create(**dic1)    # 先添加char 字段的数据，再把多对多关系加入即可
        obj_host = models.Host.objects.filter(hostname=host).first()     # 这里一定先找到刚创建的 hostname ，通过这个才可以加多对多关系表
        disk_obj = models.Disk.objects.filter(id=1)   # 默认
        obj_host.disks.add(*disk_obj)
        username = request.session['login']   # 使用它的登录用户 成为默认的值
        login_obj = models.Login.objects.filter(username=username)
        obj_host.logining.add(*login_obj)
        # print (host,dic1)
        # p = Update(user=host, data='', id=1,mes='create',**dic1)  # user, data, mes  # 用户， 数据， 修改的信息
        # status = p.start()
        path = '/host/messages/?all=' + host
        return redirect(path)
        # p = Update(user='', data='', id='', mes='create')

# @if_login
# 删除 可以了
def delete_db(request):
    user = request.GET.get('all')
    status = models.Host.objects.filter(hostname=user).delete()
    if status :
        return redirect('/host/')

    else:
        return HttpResponse("温馨提示：  不许瞎几把 乱改链接路径 哦！")


#  update 专用
class Update(object):
    list_chr = ['实例名','登录端口','CPU','内存','带宽','公网IP','私网IP','SN','内核版本','备注', '创建时间','到期时间','主机状态']
    # list_foreign = ['标签','操作系统','来源IP']
    # list_manytomany = ['所属用户','磁盘']

    # data_obj = models.Host.objects.all()
    def __init__(self,user,data,mes,id=1,**kwargs):
        self.kwargs = kwargs    # 用户创建的信息。 然后写入数据库
        self.user = str(user)
        self.data = str(data)
        self.mes = str(mes)
        self.id = id
        self.a_host = {'hostname': self.user}
        # db = models.Db_name.objects.filter(id=self.id).first()
        # self.db = str(db)
    def start(self):    #  update 专用
        if self.data in Update.list_chr:
            char = self.char()
            return char

    def char(self):
        db = models.Db_name.objects.filter(id=self.id).first()  # 取到的字段  hostname
        dic1 = {'hostname': self.user}

        dic2 = {str(db): self.mes}
        print(dic1, dic2)
        if str(db) == 'state':
            if self.mes.isdigit() :
                if int(self.mes) in [1,2,3,4]:
                    dic2['state'] = int(self.mes)
            else:
                dic2['state'] = int(3)
                # return HttpResponse('请正确输入数字，1: Running . 2 :下线, 3:关机 ,  4:删除 ')
        start_db = models.Host.objects.filter(**dic1).update(**dic2)  # 这里有布尔值返回，1正确执行，0错误
        return start_db


def user_list(request):
    if request.method == 'GET':
        if request.session['login']:   # 登陆普通用户
            # tem = 'user_list'           # 标志位
            if request.session['auto_user']:
                menu_dict = request.session.get('menu_dict')
                userinfo = request.session.get('auto_user')
                pos = request.session.get('auto_user_pos')
                img = request.session.get('auto_user_img')

                # 用户数据信息    登陆用户
                date_user = models.Login.objects.all()
                num = len(date_user)

                # 权限用户
                date_auth = models.UserInfo.objects.all()
                num_auth = len(date_user)
                return render(request, './bootstarp/user/list.html', locals())



######   测试专用
# from django.db.models import Q
# def test_q(request):
#     list_tab = ['主机名','实例名','CPU','内存/G','带宽/M','登录端口','公网IP','操作系统','全部']
#     obj = models.Host.objects.all()
#     if request.method == 'GET':
#         q = request.GET.get('q')
#         opt = request.GET.get('form')
#         if q and opt:
#             if opt == '主机名':
#                 obj_list = models.Host.objects.all().filter(Q(hostname__startswith=q))
#                 print (obj_list)
#                 print (opt)
#             elif opt == '实例名':
#                 obj_list = models.Host.objects.all().filter(Q(ecsname__startswith=q))
#                 print(obj_list)
#                 print(opt)
#             elif opt == 'CPU':
#                 obj_list = models.Host.objects.all().filter(Q(cpu__startswith=q))
#                 print(obj_list)
#                 print(opt)
#             elif opt == '内存/G':
#                 obj_list = models.Host.objects.all().filter(Q(mem__startswith=q))
#                 print(obj_list)
#                 print(opt)
#             elif opt == '带宽/M':
#                 obj_list = models.Host.objects.all().filter(Q(speed__startswith=q))
#                 print(obj_list)
#                 print(opt)
#             elif opt == '登录端口':
#                 obj_list = models.Host.objects.all().filter(Q(login_port__startswith=q))
#                 print(obj_list)
#                 print(opt)
#             elif opt == '公网IP':
#                 obj_list = models.Host.objects.all().filter(Q(eth1_network__startswith=q))
#                 print(obj_list)
#                 print(opt)
#             elif opt == '操作系统':
#                 obj_list = models.Host.objects.all().filter(Q(os__name__startswith=q))
#                 print(obj_list)
#                 print(opt)
#             elif opt == '全部':
#                 obj_list = models.Host.objects.all().filter(Q(ecsname=q) |
#                                                             Q(hostname__startswith=q) |
#                                                             Q(ecsname__startswith=q) |
#                                                             Q(cpu__startswith=q) |
#                                                             Q(mem__startswith=q) |
#                                                             Q(speed__startswith=q) |
#                                                             Q(login_port__startswith=q) |
#                                                             Q(eth1_network__startswith=q) |
#                                                             Q(os__name__startswith=q)
#                                                             )
#                 # print(obj_list)
#                 # print(opt)
#             return render(request, 'test_q.html', locals())
#     elif request.method == 'POST' :
#         q = request.POST.get('q')
#         # print (q)
#         return HttpResponse('OK')

# 菜单 menu_list pos_list auth_group_list  auth_list
def menu_list(request):   #  查询 菜单
    if request.method == 'GET':
        if request.session['login'] :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                tag = 'menu_list'
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')
                    # 以上是 我需要初始化的数据
                    menu_jg1 = []
                    menu_jg2 = []
                    auth_test = obj_auto.first().pos.auth.all()  # 所有的目录的权限
                    for x in auth_test:
                        menu_jg2.append(str(x.group.ti))  # 真实的菜单
                    # 去重 保持顺序
                    for i in menu_jg2:
                        if i not in menu_jg1:
                            menu_jg1.append(i)
                    # print (menu_jg1)

        return render(request,'./bootstarp/menu/list.html',locals())

def pos_list(request):   # 查询 职位
    if request.method == 'GET':
        if request.session['login'] :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                tag = 'pos_list'
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')
                    # 以上是 我需要初始化的数据
                    user_all = models.UserInfo.objects.all().order_by('-id')
                    auth_test = obj_auto.first().pos  # 所有的目录的权限
                    return render(request, './bootstarp/pos/list.html', locals())


def pos_add(request):
    if request.method == 'GET':
        if request.session['login'] :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                tag = 'pos_add'
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')
                    # 实际渲染的表单
                    form1 = PosUser_Form()   ## 实例化 PosUser_Form 类 添加 岗位用户
                    form2 = Pos_Form()     ## 实例化 Pos_Form 类   添加 职责岗位
                    return render(request, './bootstarp/pos/add.html',locals())
    elif request.method == 'POST':
        if request.session['login'] :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                tag = 'pos_add'
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')
                    # 获取表单
                    form1 = PosUser_Form()  #  创建 用户
                    form2 = Pos_Form()      #  创建 岗位
                    if 'user' in request.POST:   #  创建 用户
                        form1 = PosUser_Form(request.POST)  # 创建 用户
                        if form1.is_valid():  # 判断是否符合 实例化类的 规则
                            f_pos_id = int(form1.cleaned_data['pos_id'])
                            # print(form1.cleaned_data)  # {'name': 'boss2', 'passwd': '123', 'pos_id': '1'}
                            f_pos = models.UserInfo.objects.filter(id=f_pos_id).first() # 通过岗位跨表去找用户图片

                            if f_pos:   # 找到了就 继续创建
                                form1.cleaned_data.update({'img_id':int(f_pos.id),'pos_id':f_pos_id})
                                # print(form1.cleaned_data)   # {'name': 'boss2', 'passwd': '123', 'pos_id': 1, 'img_id': 1}
                                f_JG= models.UserInfo.objects.create(**form1.cleaned_data)
                            else:
                                form1.cleaned_data.update({'img_id': 5, 'pos_id': f_pos_id})
                                f_JG = models.UserInfo.objects.create(**form1.cleaned_data)
                        form1 = PosUser_Form()  # 创建 用户
                        form2 = Pos_Form()  # 创建 岗位
                        return render(request, './bootstarp/pos/add.html', locals())
                    elif 'pos' in request.POST:    #  创建 岗位
                        form2 = Pos_Form(request.POST)  # 创建 岗位
                        if form2.is_valid():   #判断是否符合 实例化类的 规则
                        # print(form.cleaned_data)   {'username': 'aa', 'password': '123'}
                            if 'y' in request.POST:
                                if 'name_id' in request.POST:
                                    name = request.POST.get('name')
                                    name_id = []
                                    for i in request.POST.getlist('name_id'):
                                        name_id.append(int(i))
                                    if 0 in name_id:
                                        obj_jg = models.Position.objects.create(name=name)
                                    else:
                                        obj_jg = models.Position.objects.create(name=name)
                                        pos_name = models.Position.objects.filter(name=name).first()
                                        for i in name_id:
                                            models.UserInfo.objects.filter(id=i).update(pos_id=pos_name.id)
                                    if obj_jg:
                                        yn_error = '创建成功'
                            elif 'n' in request.POST:
                                yn_error = '拒绝创建 NO '
                            else:
                                yn_error = '请确认选择 Yes & NO '
                        form1 = PosUser_Form()  # 创建 用户
                        form2 = Pos_Form()  # 创建 岗位
                        return render(request, './bootstarp/pos/add.html', locals())

# 这里只有老板 有权限修改 删除 添加 权限
class Pos_Update(View):
    def get(self, request, pk):
        if request.session['login'] :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')
                    userinfo_name = models.UserInfo.objects.filter(id=int(pk)).first()
                    pos_name = models.Position.objects.all()  # 所有岗位 -> pos_name.id  + pos_name
                    auth_name = models.Auth.objects.all()   # 所有权限 ->  auth_name.id  + auth_name
                    return render(request, './bootstarp/pos/update.html', locals())

    def post(self,request,pk,*args, **kwargs):
        if request.session['login'] :
            user = request.session['login']
            obj_user = models.Login.objects.filter(username=user).first()
            username = user
            password = obj_user.password
            if request.session['auto_user']:
                menu_dict = request.session.get('menu_dict')
                auth_user = request.session['auto_user']
                obj_auto = models.UserInfo.objects.filter(name=auth_user)
                if obj_auto:
                    auth_data.menu_auth(obj_auto, request)
                    userinfo = request.session.get('auto_user')
                    pos = request.session.get('auto_user_pos')
                    img = request.session.get('auto_user_img')
                    userinfo_name = models.UserInfo.objects.filter(id=int(pk)).first()

                    if 'add' in request.POST:
                        add_id = request.POST.getlist('add_id')
                        for i in add_id:
                            if i != '0':
                                userinfo_name.pos.auth.add(int(i))
                        mes1 = '添加成功'

                    elif 'remove' in request.POST:
                        remove_id = request.POST.getlist('remove_id')
                        print(remove_id)
                        for i in remove_id:
                            if i != '0':
                                userinfo_name.pos.auth.remove(int(i))
                        mes2 = '移除成功'
                    else:
                        error = '选择错误，请重新选择'
                    userinfo_name = models.UserInfo.objects.filter(id=int(pk)).first()
                    auth_name = models.Auth.objects.all()  # 所有权限 ->  auth_name.id  + auth_name
                    return render(request, './bootstarp/pos/update.html', locals())


def pos_del(request, pk):
    if request.method == 'GET':
        # 删除所选用户
        models.UserInfo.objects.filter(id=int(pk)).delete()
        return redirect('/position/list/')


def auth_group_list(request):   # 查询 权限组
    reverse_url = reverse("user_info")   # 反向 URL
    return redirect(reverse_url)
def auth_list(request):   # 查询  权限
    reverse_url = reverse("user_info")
    return redirect(reverse_url)


# 404 页面
def page_not_found(request):
    return render(request,'./404/index.html',{})

# 500错误
def page_error(request):
    return render(request, './404/index.html', {})