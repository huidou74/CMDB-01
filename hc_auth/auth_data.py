#!/usr/bin/python
#-*- coding:utf8 -*-
#BY:  H.c

def menu_auth(host_obj,request):
    obj_all = host_obj.values('name',  # 使用values()方法时，对象必须是queryset_list
                              'pos__name',
                              'pos__auth__url',  # 这是 url 路径
                              'pos__auth__name',  # 这是 对应的 名字
                              'pos__auth__to_display__url',  # 权限对应权限的 路径
                              'pos__auth__to_display__name',  # 权限对应权限的 名字
                              'pos__auth__group__name',  # 权限组名
                              'pos__auth__group__ti__title',  # 菜单名
                              )
    menu_dict = {}  # 自定义字典数据

    for i in obj_all:
        menu_auth_dict = {      # 临时字典
            'url': i.get('pos__auth__url'),  # 把数据库取到的值，赋给字典
            'name': i.get('pos__auth__name'),
            'display_url': i.get('pos__auth__to_display__url'),  # to_display 里面是对应单个查询的权限名的ID，
            'display_name': i.get('pos__auth__to_display__name'),  # ID里面包含了 对应ID 的url + name
        }  # {'url': '/auth/update/(\\d+)/', 'name': '编辑权限', 'display_url': '/auth/list/', 'display_name': '查询权限'}

        # print (i.get('pos__auth__group__ti__title'),menu_dict.keys())  # 菜单名 ( 主机 , dict_keys([]) )
        if i.get('pos__auth__group__ti__title') in menu_dict.keys():  # 第一次是空字典，所以是走else
            if not i.get('pos__auth__to_display__name'):  # 第二次 字典有值了 判断 to_display 一对多关系
                # not + None 为负负得正   # 如果是空的则是母菜单，有值才是该母菜单的子菜单，层级关系
                menu_dict[i.get('pos__auth__group__ti__title')]['lower'].append(menu_auth_dict)
                # 将字典的lower 的值， 是一个列表 [{},{},{}]，往里面添加列表的值(字典) -> append(dict)
        else:
            menu_dict[i.get('pos__auth__group__ti__title')] = {}  # 创建新字典格式  # {'主机': {}}
            menu_dict[i.get('pos__auth__group__ti__title')]['title'] = i.get('pos__auth__group__ti__title')
            # print (menu_dict[i.get('pos__auth__group__ti__title')]) # {'title': '主机'}
            # print (menu_dict[i.get('pos__auth__group__ti__title')]['title'] )   # title -> 主机
            # print (i.get('pos__auth__to_display__name'))   # -> None 取不到
            if not i.get('pos__auth__to_display__name'):  # not + None 为负负得正
                menu_dict[i.get('pos__auth__group__ti__title')]['lower'] = [menu_auth_dict, ]
                # 创建 lower  ->   {'lower': [{}]}
            else:
                menu_dict[i.get('pos__auth__group__ti__title')]['lower'] = []
                # i.get('pos__auth__to_display__name') 取到值了，就创建列表
    # print('菜单 --- ', menu_dict)
    request.session['menu_dict']=menu_dict   # 存入session
    request.session.set_expiry(0)  # 意思就是关闭浏览器就清掉session, (10) 就是10秒

    auth_dict = {}
    for i in obj_all:
        if i.get('pos__auth__group__name') in auth_dict.keys():
            auth_dict.get(i.get('pos__auth__group__name')).get('url').append(i.get('pos__auth__url'))
            # 将每个url 以列表的append的方法添加进去,成为单个权限组名的 值 {'用户表':{url: ['a','b','c',]}, }
        else:
            auth_dict[i.get('pos__auth__group__name')] = {'url': [i.get('pos__auth__url'), ], }
            # 将 权限组名 作为 auth_dict 字典的 keys, 将对应权限组的url  作为 auth_dict 字典的 values
    # print('权限  ---  ', auth_dict)
    request.session['auth_dict']=auth_dict   # 存入session
    request.session.set_expiry(0)  # 意思就是关闭浏览器就清掉session, (10) 就是10秒