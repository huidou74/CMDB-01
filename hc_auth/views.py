from django.shortcuts import render, HttpResponse, redirect
from hc import models
from hc_auth import auth_data
from lyh_project import settings
# Create your views here.
def auth_demo(request):
    if request.method == 'GET':
        return  render(request, './bootstarp/host/auth_login.html' ,locals())
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        host_obj = models.UserInfo.objects.filter(name=username, passwd=password)
        if host_obj.first():
            code = request.POST.get('code').upper()
            if request.session[settings.CODEIMG].upper() != code:
                error = '验证码错误！ 请重新输入！'
                return render(request, './bootstarp/host/auth_login.html', locals())
            else:
                auth_data.menu_auth(host_obj, request)
                request.session['auto_user'] = host_obj.first().name
                request.session['auto_user_pos'] = str(host_obj.first().pos)
                request.session['auto_user_img'] = str(host_obj.first().img)
                return redirect('/index/')
        else:
            error = '账号或密码输入错误,登录失败'
            return render(request, './bootstarp/host/auth_login.html',locals())



def index(request):
    menu_dict = request.session.get('menu_dict')
    return render(request, 'bootstarp/host/list.html', locals())

# 这里循环的数据是写死的，加了权限需要在这里补充 列表加数据
def user_info(request):
    if request.method == 'GET':
        user = request.session['login']
        obj_user = models.Login.objects.filter(username=user).first()
        tem = 'user_auth_info'
        if request.session['auto_user']:
            menu_dict = request.session.get('menu_dict')
            auth_user = request.session['auto_user']
            obj_auto = models.UserInfo.objects.filter(name=auth_user)
            if obj_auto:
                auth_data.menu_auth(obj_auto, request)
                userinfo = request.session.get('auto_user')
                pos = request.session.get('auto_user_pos')
                img = request.session.get('auto_user_img')

        username = request.session.get('auto_user')
        obj_auth_user = models.UserInfo.objects.filter(name=username).first()
        # print (obj_auth_user)   # 用户名
        # print (obj_auth_user.pos.name)   # 岗位名名字

        dict_a = {}
        list_a = []
        list_b = []
        list_c = []
        list_d = []
        list_e = []
        list_f = []
        list_g = []
        for i in obj_auth_user.pos.auth.all():
            # print (i.group.id, i.id)
            if i.group.id == 8:
                list_a.append(str(i))
                dict_a.update({str(i.group):list_a})
            elif i.group.id == 5:
                list_b.append(str(i))
                dict_a.update({str(i.group): list_b})
            elif i.group.id == 3:
                list_c.append(str(i))
                dict_a.update({str(i.group): list_c})
            elif i.group.id == 7:
                list_d.append(str(i))
                dict_a.update({str(i.group): list_d})
            elif i.group.id == 4:
                list_e.append(str(i))
                dict_a.update({str(i.group): list_e})
            elif i.group.id == 6:
                list_f.append(str(i))
                dict_a.update({str(i.group): list_f})
            elif i.group.id == 9:
                list_g.append(str(i))
                dict_a.update({str(i.group): list_f})

        return render(request, './bootstarp/user_auth_info.html', locals())













