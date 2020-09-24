from tanTan import api_config
from pip._vendor import requests
import time
from hashlib import md5
import json

def send_sms(phonenum, vcode):
    appid = api_config.CD_APPID
    appkey = api_config.CD_APPKEY
    data = {
        'appid': appid,
        'to': phonenum,
        'project': api_config.CD_TEMPLATE,
        'timestamp': int(time.time()),
        'sign_type': 'md5',
        'vars': json.dumps({'vcode': vcode}),
    }
    # 计算签名
    sort_data = sorted(data.items())
    data_str = '&'.join([f'{key}={value}' for key, value in sort_data])
    sign_str = f'{appid}{appkey}{data_str}{appid}{appkey}'
    signature = md5(sign_str.encode('utf8')).hexdigest()
    data['signature'] = signature
    # 发送短信
    response = requests.post(api_config.CD_API, data=data)
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            return True
    return False