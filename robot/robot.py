# -*- coding:UTF-8 -*-
from recognition import Recognition
from nlu import Nlu
from speaker import Speaker
from skills import Weather, Chat, Ticket, Noun, Music
from music_player import Music_Player

# 功能调度模块
class Robot():
    def __init__(self):
        self.recognizer = Recognition() # 语音识别
        self.nlu = Nlu() # 语义识别
        self.speaker = Speaker() # 语音合成
        self.music_player = Music_Player() # 音乐播放器
        self.weather = Weather(self.speaker) # 查询天气功能
        self.chat = Chat(self.speaker) # 闲聊功能
        self.ticket = Ticket(self.speaker) # 查询车票功能
        self.noun = Noun(self.speaker) # 名词解释功能
        self.music = Music(self.speaker, self.music_player) # 播放音乐功能

    def get_music_player(self):
        return self.music_player
    
    # 识别语音并进行对应的处理
    def process(self, fname):
        speech = self.recognizer.recognize(fname) # 语音识别(语音转文字)
        if speech is not None:
            skill, response = self.nlu.query(speech) # 语义识别(情感倾向)
            if skill == 'weather':
                print("命中技能天气")
                self.weather.process(response)
            elif skill == 'chat':
                print("命中技能闲聊")
                self.chat.process(response)
            elif skill == 'noun_interpretaion':
                print("命中技能名词解释")
                self.noun.process(response)
            elif skill == 'ticket':
                print("命中技能订购车票")
                self.ticket.process(response)
            elif skill == 'music':
                print("命中技能播放音乐")
                self.music.process(response)