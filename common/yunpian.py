# Author:gyk

import requests
import json

class YunPian(object):
    def __init__(self,api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'  # 此地址可在api文档里查看

    def send_sms(self,code,mobile):
        parmas = {
            'apikey':self.api_key,
            'mobile':mobile,
            'text':'【高永康】您的验证码是%s。如非本人操作，请忽略本短信'%code  # 与云片中模板保持一致
        }

        response = requests.post(self.single_send_url,data=parmas)
        re_dict = json.loads(response.text)
        print(re_dict)
        return re_dict

if __name__ == '__main__':
    yun_pian = YunPian('57ca89c4b286e82d56db94434b4f4f79')  # 将apikey传入
    yun_pian.send_sms('4651','13572551532')  # 4651就是所设定的验证码，135...为要发送的手机号