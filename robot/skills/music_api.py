# -*- coding:UTF-8 -*-
import requests
import random
import base64
from Crypto.Cipher import AES
import sys
import json
import binascii
import urllib

class Music_api():
    # 设置从JS文件提取的RSA的模数、协商的AES对称密钥、RSA的公钥等重要信息
    def __init__(self):
        self.modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pubKey = '010001'
        self.url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
        self.HEADER = {}
        self.setHeader()
        self.secKey = self.getRandom()

    # 生成16字节即256位的随机数
    def getRandom(self):
        string = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        res = ""
        for i in range(16):
            res += string[int(random.random()*62)]
        return res

    # AES加密，用seckey对text加密
    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey, 2, '0102030405060708')
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext).decode("utf-8")
        return ciphertext

    # 快速模幂运算，求 x^y mod mo 
    def quickpow(self, x, y, mo):
        res = 1
        while y:
            if y & 1:
                res = res * x % mo
            y = y // 2
            x = x * x % mo
        return res 

    # rsa加密
    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        a = int(binascii.hexlify(str.encode(text)), 16)
        b = int(pubKey, 16)
        c = int(modulus, 16)
        rs = self.quickpow(a, b, c)
        return format(rs, 'x').zfill(256)

    # 设置请求头
    def setHeader(self):
        self.HEADER = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'https://music.163.com/search/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }

    # 设置相应的请求参数，从而搜索列表
    # 总体的密码加密步骤为：
    # 首先用nonce对text加密生成密文1
    # 然后用随机数seckey加密密文1生成密文2
    # 随后，用公钥加密seckey生成密文3
    # 其中，密文2作为请求参数中的params，密文3作为encSeckey字段
    # 这样，接收方可以通过私钥解密密文3获得seckey(随机数)
    # 然后用seckey解密密文2获得密文1
    # 最终用统一协商的密钥nonce解密密文1最终获得text
    def search(self, s,offset,type="1"):
        text = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "#/discover": "", "s": s, "type": type,"offset": offset, "total": "true", "limit": "30", "csrf_token": ""}
        text = json.dumps(text)
        params = self.aesEncrypt(self.aesEncrypt(text,self.nonce),self.secKey)
        encSecKey = self.rsaEncrypt(self.secKey,self.pubKey,self.modulus)
        data = {
            'params': params,
            'encSecKey': encSecKey
        }
        result = requests.post(url=self.url, data=data, headers = self.HEADER,verify=False).json()
        return result

    # 获取指定音乐列表(相当于主函数)
    def get_music_list(self, keywords):
        music_list = []
        for offset in range(1):
            result = Music_api().search(keywords, str(offset))
            result = result['result']['songs']
            singer = None
            for music in result:
                if keywords == music['name']:#播放第一个结果中同一歌手的歌
                    singer = music['ar'][0]['name']
                    music_list.append(music)
                    return music_list + self.get_music_list(singer)
                # if music['copyright'] == 1 and music['fee'] == 8:
                if (music['privilege']['fee'] == 0 or music['privilege']['payed']) and music['privilege']['pl'] > 0 and music['privilege']['dl'] == 0:#版权问题
                    continue
                if music['privilege']['dl'] == 0 and music['privilege']['pl'] == 0:
                    continue
                # if music['fee'] == 8 or music['fee'] == 0:
                music_list.append(music)
        return music_list

# print(Music_api().get_music_list("像我这样的人"))