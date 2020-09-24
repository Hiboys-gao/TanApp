
import random
import re

from django.core.cache import cache

from libs.sms import send_sms

"""
SMS:
"""
# 生成随机验证码
def random_vcode(length=4):
    vcode = ''
    for i in range(length):
        vcode += str(random.randint(0, 9))
    return vcode


# 判断手机号的合法性
def is_phonenum(phonenum):
    if re.match(r'1[3-9]\d{9}$', phonenum):
        return True
    else:
        return False


# 发送短信验证码
def send_vcode(phonenum):
    if not is_phonenum(phonenum):
        return False
    key='sendvcode_%s' % phonenum
    if cache.get(key):
        return True
    vcode=random_vcode()
    cache.set(key,vcode,180)
    return send_sms(phonenum=phonenum,vcode=vcode)