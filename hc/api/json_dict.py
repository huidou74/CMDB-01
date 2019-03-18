#!/usr/bin/python
#-*- coding:utf8 -*-
#BY:  H.c
import json
import os, sys
# 测试 salt api  已完成


from .salt_api import SaltApi
api = 'https://192.168.1.8:8001/'


# saltstack 命令
salt = SaltApi(api)
salt_client = '*'
salt_test = 'grains.items'
data = salt.salt_command(salt_test,salt_client)


data_list = ['kernel','mem_total','id','num_cpus','localhost','host','ipv4','os']
orm_data_list = []
mes_dict = [
    'id',
    {'messages': {
                  'kernel':'',
                  'os_id':'',
                  'ecsname':'',
                  'hostname':'',
                  'eth0_network':'',
                  'cpu':'',
                  'mem':''
    }
    }
]
# 内核版本  # 取到所有的key, #系统 ,   # 主机名 ,  # 主机名, #内网 ,  # cpu,  # 内存
# for k in data.keys():
#     # print (type(k))
# 以后用到 grains.itmes 时，抓到的数据，对应数据的字段会格式化的减少代码。
cache_data = {}
for v in data.values():
    # print (v)
    if isinstance(v, dict):   # 找字典
        # print ('dict ->   ',v)
        for i in v.keys():
            if i in data_list:
                if i == 'mem_total':
                    a = (v.get(i) / 1024)
                    cache_data.update({'mem':int(str(round(a)).split('.')[0])})
                elif i == 'ipv4':
                    cache_data.update({'eth0_network': v.get(i)[1]})
                elif i == 'kernel':
                    b = v.get('kernel') +'  '+ v.get('kernelrelease')
                    cache_data.update({'kernel':b})
                elif i == 'os':
                    c = v.get('os') +'  '+ v.get('osrelease')
                    cache_data.update({'os': c})
                    os_id = cache_data.pop('os')
                    cache_data.update({'os_id':os_id})
                elif i == 'num_cpus':
                    cache_data.update({ 'cpu':v.get(i)})
                elif i == 'localhost':
                    cache_data.update({'hostname': v.get(i)})
                elif i == 'host':
                    cache_data.update({'ecsname': v.get(i)})
                else:
                    cache_data.update({i: v.get(i)})


    for a in mes_dict:
        if isinstance(a, str):
            mes_dict[0] = cache_data.pop('id')
        elif isinstance(a, dict):
            for kk in a.values():
                kk.update(cache_data)

    cache_data.clear()
    # from hc import models
    data_orm = {}
    for i in mes_dict:
        if isinstance(i, dict):
            for vv in i.values():
                data_orm.update(vv)
    data_orm.update({'state': 1})  # 主机状态值
    orm_data_list.append(data_orm)


