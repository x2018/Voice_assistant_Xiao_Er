# -*- coding:UTF-8 -*-
import requests
import re
import pickle
import time

class Ticket():
    def __init__(self, speaker = None):
        self.speaker = speaker
    
    # 根据api返回识别用户查询区间、时间等
    def process(self, response):
        intent = response['schema']['intent']
        slots = response['schema']['slots']
        print(intent)
        info = {}
        info['user_dep'] = info['user_arr'] = info['user_time'] = None
        if intent == "DING_PIAO" or intent == "XUN_JIA":
            for slot in slots:
                if slot['name'] == 'user_time':
                    info[slot['name']] = slot['normalized_word']
                else:
                    info[slot['name']] = slot['original_word']
        tex = self.get_ticket(info['user_dep'], info['user_arr'], info['user_time'])
        self.speaker.speak(tex)

    # 获取车票信息并输出
    def get_ticket(self, src = None,dst = None ,date = None):
        print(src, dst, date)
        if(src == None or dst == None):
            return "抱歉，您提供的目的地或出发地不明确"
        else:
            # 12306的城市名和城市代码js文件url
            url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
            r = requests.get(url, verify=False)
            pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
            result = re.findall(pattern, r.text)
            station = dict(result)  # {'北京北': 'VAP', '北京东': 'BOP', '北京': 'BJP',
            # with open("./robot/skills/station.file", "rb") as f:  # 读取dict文件
            #     station = pickle.load(f)
        headers = {'user-agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}
        if date == None: #默认为今天
            date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date="+date+"&leftTicketDTO.from_station="\
        + str(station[src]) +"&leftTicketDTO.to_station=" + str(station[dst]) + "&purpose_codes=ADULT"
        response = requests.get(url,headers = headers,verify=False)#获取网页html
        data = re.findall(r'".*?"',response.text)#选取目标
        result = []
        sig = False
        for i in data:
            if sig:
                content = i.split("|")
                if len(content) < 30:
                    continue
                if (content[30] != "无" and content[30] != ""):
                    result = content
                    break;
            else:
                if i == "\"result\"":
                    sig = True
                    continue
        if result != []:
            info = "为您查到"+date+src+"到"+dst+"最近的"+str(result[3])+"次列车尚有二等座余票，发车时间为"+str(result[8])+ ",到达时间为"+str(result[9])+",共历时"+str(int(result[10][1:2]))+"小时"+str(result[10][3:])+"分"
        else:
            info ="抱歉，"+date+src+"到"+dst+"的列车均没有余票"
        #f.close()
        return info

