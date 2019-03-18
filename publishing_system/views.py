
# Create your views here.


from django.shortcuts import render, HttpResponse, redirect
from hc import models
from hc_auth import auth_data
import os,sys

from publishing_system.task import add, mian_salt
from celery.result import AsyncResult
from lyh_project.celery import app

from publishing_system.main_salt import MainSalt,UtcTime, sub_run
from publishing_system.salt_run import Salt_Run

def publish(request):
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

                # 渲染所有数据
                envs = models.Use_Env.objects.all()
                return render(request, './bootstarp/publishing/right_away.html', locals())
    else:
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
                # 上面是权限页面需要的数据
                # 下面才是我的逻辑
                envs = models.Use_Env.objects.all()
                env = request.POST.get('env')
                app = request.POST.get('app')
                obj_list = models.App.objects.filter(name=app, environment__name=env).first()  # 跨表查询

                hosts_list = []
                if obj_list:
                    for i in obj_list.hosts.all():
                        id = i.hostname   #id   #hc - 01
                        # print ('id -> ',id)
                        hosts_list.append({'id':str(i.hostname),'path':str(obj_list.path),'app_name': str(obj_list),'package':str(obj_list.package.pack_path)})
                    aaa = Salt_Run(hosts_list)
                    jgs=aaa.run_list()
                    
                return render(request, './bootstarp/publishing/right_away.html', locals())





def celery_status(request):
    time_list = ['year', 'month', 'day', 'hour', 'minute']
    time_dict = {}
    envss = models.Use_Env.objects.all()
    if request.method == 'GET':
        # 页面权限需要的数据
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

                # 当前应用 的逻辑
                x = request.GET.get('x')
                y = request.GET.get('y')
                envs = request.GET.get('envs')
                apps = request.GET.get('apps')
                obj_list = models.App.objects.filter(name=apps, environment__name=envs).first()  # 跨表查询                
                hosts_list = []
                if obj_list:
                    for i in obj_list.hosts.all():
                        id = i.hostname  # id   #hc - 01
                        hosts_list.append({'id': str(i.hostname), 'path': str(obj_list.path), 'app_name': str(obj_list),
                                           'package': str(obj_list.package.pack_path)})
                try :
                    if x and y or envs and apps:
                        try :
                            after = request.GET.get('after')
                            if after:
                                utc = UtcTime(after=int(after))
                                ctime_x = utc.after_time()
                                if ctime_x:
                                    #  最核心的代码
                                    if  x and y:
                                        ret = add.apply_async(args=[int(x), int(y)], eta=ctime_x)
                                        num = ret.id
                                    elif envs and apps:
                                        ret = mian_salt.apply_async(args=[hosts_list], eta=ctime_x)
                                        num = ret.id
                        except ValueError:
                            after_error = '请正确输入数值'

                        year = request.GET.get('year')
                        mouth = request.GET.get('month')
                        day = request.GET.get('day')
                        hour = request.GET.get('hour')
                        minute = request.GET.get('minute')
                        if year and mouth and day and hour and minute:
                            try:
                                for i in time_list:
                                    a = request.GET.get(i)
                                    time_dict.update({i: int(a)})
                                utc = UtcTime(**time_dict)
                                ctime_x = utc.ctime()
                                if ctime_x:
                                    if x and y:
                                        ret = add.apply_async(args=[int(x), int(y)], eta=ctime_x)
                                        num = ret.id
                                    elif envs and apps:
                                        ret = mian_salt.apply_async(args=[hosts_list], eta=ctime_x)
                                        num = ret.id
                            except ValueError:
                                error = '请正确输入日期数值'
                        else:
                            error = '请将表格数据输入完整'
                except ValueError:
                    error = '请正确输入日期数值'

                cancel = request.GET.get('cancel')
                if cancel:
                    async = AsyncResult(id=cancel, app=app)
                    async.revoke(terminate=True)
                    cancel_tag='取消成功'   #  定时任务的取消 是 还没执行之前就取消，执行了放在消息队列里面了就不行被取消
                    async.forget()
                stop = request.GET.get('stop')
                if stop:
                    async = AsyncResult(id=stop, app=app)
                    async.revoke()
                    stop_tag='中止成功'   #  定时任务的中止， 是 在执行的过程中，中止任务，必须是在执行的时候
                    async.forget()
                return render(request, './bootstarp/publishing/timing.html', locals())
    elif request.method == 'POST':
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
                ret = request.POST.get('id', '').strip(' ')
                data = ""
                forget = request.POST.get('forget')

                if ret:
                    async = AsyncResult(id=ret, app=app)
                    if async.successful():
                        data = "执行成功，数据如下"
                        jg = async.get()
                        if not forget:
                            jg='清除完成'
                            async.forget()
                    elif async.failed():
                        data = '执行失败'
                    elif async.status == 'PENDING':
                        data = "等待被执行"
                    elif async.status == 'RETPY':
                        data = '任务异常正常重试'
                    elif async.status == 'STARTED':
                        data = "任务正在执行"
                    else:
                        data = "未知"
                else:
                    data = '请正确填写对应 ID '
                return render(request,'./bootstarp/publishing/timing.html', locals())