# -*- coding:UTF-8 -*-
import requests 
import uuid 
from player import Player
import os
import time

# 语音合成
class Speaker():
    def __init__(self):
        self.player = Player()
        self.API_KEY = 'qYtgrI3PxOMBrVywsGtBZfR4'
        self.SECRET_KEY = 'fT2RW8WNVtTTlODjBbDk8T10FUPcjvRl'    

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

    def speak(self, tex):
        print(tex)
        access_token = self.get_access_token()
        url = "https://tsn.baidu.com/text2audio"
        data = {
            'tex': tex,
            'tok': access_token,
            'cuid': str(uuid.uuid1()),
            'ctp': 1, 
            'lan': 'zh',
            'per': 4
        }   
        result = requests.post(url=url, data=data)
        fname = os.path.join('/tmp', str(int(time.time())) + '.mp3')
        if result.headers['Content-Type'] == 'audio/mp3':
            with open(fname, 'wb') as f:
                f.write(result.content)
        self.player.play_music(fname)

