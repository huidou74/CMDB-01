#!/usr/bin/python
#-*- coding:utf8 -*-
#BY:  H.c

import os

from publishing_system.main_salt import MainSalt, sub_run



def run_salt_cmd(hosts_list):
    meassages_list= []
    jgs = []
    error=''
    for i in hosts_list:
        app_name = i.get('app_name')
        package = i.get('package')
        salt_id = i.get('id')
        path_app = i.get('path') + app_name
        path = os.getcwd() + r'/project_path/'
        cmd = 'cd {0} && if [ -d ./{1} ];then cd {1} ; else mkdir {1} ; fi && if [ -d ./huidou ];then cd huidou && git pull ; else git clone {2} ;fi'.format(
            path, app_name, package)
        ret = sub_run(cmd)  # 去执行上面的克隆仓库的任务
        # print ('true - >  ',ret.stdout.read())   # 正确返回
        # print ('error - >  ',ret.stderr.read())  # 错误返回
        error = ret.stderr.read()
        if ret.stdout.read(): # 判断上面的shell 执行结果
            m_salt = MainSalt(salt_id)
            pillar_dic = {'path':path_app, 'app': app_name }
            salt_ret = m_salt.push_package(pillar_dic)
            # print(salt_ret)
            c_path = 'cd {0} && cat huidou/test.txt'.format(path_app)
            meassages = m_salt.cmd_run([c_path, ])
            meassages_list.append(meassages)
            mess = meassages.get(salt_id).get('ret')
    if meassages_list:
        for i in meassages_list:
            mess = i.get(salt_id).get('ret')
            jgs.append('主机: \n{0} \n返回结果:\n \n{1}\n\n-------------------------\n'.format(salt_id, mess))
    if jgs:
        print (type(jgs),jgs)
        return jgs
    elif error:
        return '执行失败 : '+error
    else:
        return '执行程序异常！'



class Salt_Run(object):
    meassages_list = []
    error = ''
    jgs = ''
    salt_id =[]
    rets = {}
    def __init__(self,hosts_list):
        self.hosts_list = hosts_list
        self.path = os.getcwd() + r'/project_path/'
        self.cmd = 'cd {0} && if [ -d ./{1} ];then cd {1} ; else mkdir {1} ; fi && if [ -d ./huidou ];then cd huidou && git pull ; else git clone {2} ;fi'
        self.salt_id = []
    def run_list(self):
        for i in self.hosts_list:
            app_name = i.get('app_name')
            package = i.get('package')
            salt_id = i.get('id')
            Salt_Run.salt_id.append(salt_id)
            path_app = i.get('path') + app_name
            ret = sub_run(self.cmd.format(self.path, app_name, package))
            Salt_Run.error = ret.stderr.read()
            if ret.stdout.read():  # 判断上面的shell 执行结果
                m_salt = MainSalt(salt_id)
                pillar_dic = {'path': path_app, 'app': app_name}

                Salt_Run.rets.update(m_salt.push_package(pillar_dic))

                c_path = 'cd {0} && cat huidou/test.txt'.format(path_app)
                meassages = m_salt.cmd_run([c_path, ])
                Salt_Run.meassages_list.append(meassages)
        print (Salt_Run.rets)
        if Salt_Run.meassages_list:
            for dic in Salt_Run.meassages_list:

                x = Salt_Run.salt_id.pop(0)
                mess = dic.get(x).get('ret')
                Salt_Run.jgs += ('主机: \n{0} \n返回结果:\n \n{1}\n\n-----------------------\n'.format(x, mess))
            if Salt_Run.jgs:
                return Salt_Run.jgs
            elif Salt_Run.error:
                return '执行失败 : ' + Salt_Run.error
            else:
                return '执行程序异常！'


