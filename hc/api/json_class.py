#!/usr/bin/python
#-*- coding:utf8 -*-
#BY:  H.c
# from salt_api import SaltApi
# from lyh_project.settings import *
# api = 'https://192.168.1.8:8001/'

# 给 grains.items 用的
# login_port 和 disk   ->   登录端口 和 磁盘信息 使用 cmd.run -> 去取值
class Json_dict(object):
    orm_data_list = []
    cache_data = {}
    def __init__(self, data, data_list ,mes_dict):
        self.data = data
        self.data_list = data_list
        self.mes_dict = mes_dict

    def for_data_values(self):
        for v in self.data.values():
            self.format_data(v)
            b = self.orm_data()
            Json_dict.orm_data_list.append(b)
        return Json_dict.orm_data_list

    def format_data(self, v):
        if isinstance(v, dict):  # 找字典
            # print ('dict ->   ',v)
            for i in v.keys():
                if i in self.data_list:
                    if i == 'mem_total':
                        a = (v.get(i) / 1024)
                        Json_dict.cache_data.update({'mem': int(str(round(a)).split('.')[0])})
                    elif i == 'ipv4':
                        Json_dict.cache_data.update({'eth0_network': v.get(i)[1]})
                    elif i == 'kernel':
                        b = v.get('kernel') + '  ' + v.get('kernelrelease')
                        Json_dict.cache_data.update({'kernel': b})
                    elif i == 'os':
                        c = v.get('os') + '  ' + v.get('osrelease')
                        Json_dict.cache_data.update({'os': c})
                        os_id = Json_dict.cache_data.pop('os')
                        Json_dict.cache_data.update({'os_id': os_id})
                    elif i == 'num_cpus':
                        Json_dict.cache_data.update({'cpu': v.get(i)})
                    elif i == 'localhost':
                        Json_dict.cache_data.update({'hostname': v.get(i)})
                    elif i == 'host':
                        Json_dict.cache_data.update({'ecsname': v.get(i)})
                    else:
                        Json_dict.cache_data.update({i: v.get(i)})
        return Json_dict.cache_data

    def orm_data(self):
        for a in self.mes_dict:
            if isinstance(a, str):
                self.mes_dict[0] = Json_dict.cache_data.pop('id')
            elif isinstance(a, dict):
                for kk in a.values():
                    kk.update(Json_dict.cache_data)
        # print ('需要的数据  -> ',mes_dict)
        Json_dict.cache_data.clear()
        data_orm = {}
        for i in self.mes_dict:
            if isinstance(i, dict):
                for vv in i.values():
                    data_orm.update(vv)
        data_orm.update({'state': 1})  # 主机状态值
        # Json_dict.orm_data_list.append(data_orm)
        return data_orm
