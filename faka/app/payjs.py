#-*- coding=utf-8 -*-
import requests
from hashlib import md5
import copy
from config import *

url = 'https://payjs.cn/api/native'


data = {'mchid': PAYJS_ID,
        'total_fee': '1',
        'out_trade_no': '2017122712581',
        'body': 'test'}


def get_sign(data):
    str_d = sorted(['='.join(i) for i in data.items()], key=lambda x: x[0])
    str_d.append('key={}'.format(PAYJS_KEY))
    str_ = '&'.join(str_d)
    a = md5(str_.encode('utf-8'))
    return a.hexdigest().upper()


def getqr(money, tradeid, info='faka', feedback=None):
    sd = copy.deepcopy(data)
    sd['total_fee'] = str(int(money * 100))
    sd['out_trade_no'] = str(tradeid)
    sd['body'] = info
    if feedback != None:
        sd['notify_url'] = feedback
    sign = get_sign(sd)
    sd['sign'] = sign
    try:
        r = requests.post(url, data=sd)
        return r.json()['code_url']
    except Exception as e:
        print(e)
        return False
