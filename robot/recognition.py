# -*- coding:UTF-8 -*-
from aip import AipSpeech

# 语音识别
class Recognition():
    def __init__(self):
        APP_ID = '16150576'
        API_KEY = 'qYtgrI3PxOMBrVywsGtBZfR4'
        SECRET_KEY = 'fT2RW8WNVtTTlODjBbDk8T10FUPcjvRl'
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def recognize(self, fname):
        result = self.client.asr(self.get_file_content(fname), 'wav', 16000, {
            'dev_pid': 1536,
        })
        if 'result' in result:
            return result['result'][0]
        else:
            return None