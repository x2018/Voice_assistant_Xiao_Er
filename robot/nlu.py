# -*- coding:UTF-8 -*-
import requests
import uuid

# 自然语言处理(语义识别)
class Nlu():
    def __init__(self):
        self.API_KEY = 'qYtgrI3PxOMBrVywsGtBZfR4'
        self.SECRET_KEY = 'fT2RW8WNVtTTlODjBbDk8T10FUPcjvRl'    
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.API_KEY,
            'client_secret': self.SECRET_KEY,
        }
        result = requests.get(url=url, params=params).json()
        access_token = result['access_token']
        return access_token

    def query(self, tex):
        print(tex)
        url = "https://aip.baidubce.com/rpc/2.0/unit/service/chat?access_token=" + self.access_token
        headers = {'Content-Type': 'application/json'}
        request = {
            'user_id': '123456',
            'query': tex
        }
        data = {
            'version': '2.0',
            'log_id': str(uuid.uuid1()),
            'service_id': 'S17481',
            'session_id': str(uuid.uuid1()),
            'request': request
        }
        result = requests.post(url=url, json=data, headers=headers).json()
        import json
        with open("temp.json",'w') as f:#,encoding='utf-8'
            json.dump(result, f)#, ensure_ascii=False
        return self.parser(result)
    
    def parser(self, result):
        response_list = result['result']['response_list']
        response = response_list[0]
        if response['origin'] == '51011':
            return ('weather', response)
        elif response['origin'] == '51010':
            return ('chat', response)
        elif response['origin'] == '51027':
            return ('ticket', response)
        elif response['origin'] == '51028':
            return ('noun_interpretaion', response)
        elif response['origin'] == '50968':
            return ('music', response)
            


