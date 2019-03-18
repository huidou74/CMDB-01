#!/usr/bin/python
#-*- coding:utf-8 -*-
# BY :   H .c
import hashlib
import base64

class Jiami(object):
    @staticmethod
    def encrypt(pwd):
        # MD5 加密  用于 CMDB用户登录密码的加密---- 不可逆
        obj = hashlib.md5()
        obj.update(pwd.encode('utf-8'))
        data = obj.hexdigest()
        return data

    def base_str_encrypt(self, str_p1):
        # base 64 加密  ---  加密简单，可逆解密
        str_p1 = 'shi`bushi`SB@pile'+ str(str_p1) + 'wo+_;^%#baba'
        return base64.encodestring(str_p1.encode()).decode()

    def base_str_decrypt(self, str_p2):
        # base 64 解密  ---  加密简单，可逆解密
        try :
            str_p2 = base64.decodestring(str(str_p2).encode())
            return str_p2.decode()[17:-12]
        except Exception:
            return '不识别！'

    def decrypt(self,str_p2):
        str_p2 = base64.decodestring(str(str_p2).encode())
        return str_p2


#print (Jiami.encrypt('abc'))   # 静态方法  可以不用实例化
# md = Jiami()
# print (md.encrypt('abc'))   # MD5 加密 ->  '900150983cd24fb0d6963f7d28e17f72'

# base = Jiami()
# # base64 加密
# new_pwd1 = base.base_str_encrypt('123123')  # 括号内的 就是 用户设置的密码，它的返回值就可以写入数据库
# print (new_pwd1)  # base64 加密 ->  'c2hpYnVzaGl5b3VwaWxlYWJjd29zaGluaWJhYmE='
#
# # base64  解密
# new_pwd2 = base.base_str_decrypt(new_pwd1)   #
# print(new_pwd2)
