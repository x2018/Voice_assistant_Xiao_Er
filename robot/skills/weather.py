# -*- coding:UTF-8 -*-
import requests 
import time

class Weather():
    def __init__(self, speaker = None):
        self.speaker = speaker
    
    # 爬取天气情况
    def get_weather(self, user_loc, user_time):
        null_dict={}
        url = "http://apis.juhe.cn/simpleWeather/query?city="+str(user_loc)+"&key=2474caa0d0c2f1df25909c6a86dfd2c5"
        data = requests.get(url)
        weather=data.json()
        # weather = {'reason': '查询成功!', 'result': {'city': '武汉', 'realtime': {'temperature': '24', 'humidity': '44', 'info': '晴', 'wid': '00', 'direct': '东北风', 'power': '3级', 'aqi': '58'}, 'future': [{'date': '2019-05-01', 'temperature': '14/25℃', 'weather': '多云', 'wid': {'day': '01', 'night': '01'}, 'direct': '东北风'}, {'date': '2019-05-02', 'temperature': '12/25℃', 'weather': '多云转晴', 'wid': {'day': '01', 'night': '00'}, 'direct': '东南风'}, {'date': '2019-05-03', 'temperature': '17/27℃', 'weather': '多云', 'wid': {'day': '01', 'night': '01'}, 'direct': '东南风'}, {'date': '2019-05-04', 'temperature': '17/27℃', 'weather': '多云转小雨', 'wid': {'day': '01', 'night': '07'}, 'direct': '南风转东风'}, {'date': '2019-05-05', 'temperature': '14/26℃', 'weather': '小雨', 'wid': {'day': '07', 'night': '07'}, 'direct': '东风转东北风'}]}, 'error_code': 0}
        result=weather['result']
        if(result == None):
            return None
        if user_time == time.strftime("%Y-%m-%d",time.localtime()):
            realtime = result['realtime']
            temperature = realtime['temperature']
            humidity = realtime['humidity']
            min_temp, max_temp = result['future'][0]['temperature'].strip("℃").split("/")
            temperature = realtime['temperature']
            info = realtime['info']
            direct = realtime['direct']
            power = realtime['power']
            tex = "{}今天{}, {}{}, {}度到{}度，现在的室外温度为{}度".format(user_loc, info, direct, power, min_temp, max_temp, temperature)
            return tex
        else:
            futures = result['future']
            num = 0
            for future in futures:
                if future['date'] == user_time:
                    temperature = future['temperature']
                    min_temp, max_temp = temperature.strip("℃").split("/")
                    weather = future['weather']
                    direct = future['direct']
                    days = ["今天", "明天", "后天", "大后天", "大大后天"]
                    tex = user_loc + days[num] + weather + ", " + min_temp + "度到" + max_temp + "度   " 
                num += 1
        return tex        
    
    # 默认为武汉与当前时间
    def process(self, response):
        slots = response['schema']['slots']
        result = {}
        result['user_loc'] = '武汉'
        result['user_time'] = time.strftime("%Y-%m-%d",time.localtime())
        for slot in slots:
            result[slot['name']] = slot['normalized_word']
        tex = self.get_weather(result['user_loc'], result['user_time'])
        self.speaker.speak(tex)


