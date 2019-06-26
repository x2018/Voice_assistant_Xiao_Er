# -*- coding:UTF-8 -*-
from snowboy import snowboydecoder
import sys
import signal
from robot.player import Player
from robot.robot import Robot
from time import sleep
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SmartSpeaker():
    # 初始化
    def __init__(self):
        self.interrupted = False
        self.model = "嘿小二.pmdl" # 使用的语音模型
        signal.signal(signal.SIGINT, self.signal_handler) # 捕获ctrl+c
        self.detector = snowboydecoder.HotwordDetector(self.model, sensitivity=0.5) # 设置语音模型与敏感度
        print('Listening... Press Ctrl+Z to exit')
        self.robot = Robot() # 创建应用模块
        self.music_player = self.robot.get_music_player() # 创建音乐播放模块
        self.player = Player() # 触发响应词叮咚播放
        
    def signal_handler(self, signal, frame):
        self.interrupted = True

    def interrupt_callback(self):
        return self.interrupted

    def detected_callback(self):
        self.music_player.pause() # 检测到人声时音乐暂停
        self.player.play_ding() # 触发 叮

    def speeched_callback(self, fname):
        self.player.play_dong() # 检测时间到后触发 咚
        self.robot.process(fname) # 将收到的语音传给应用模块执行相应的操作
        sleep(1) # 等待片刻
        self.music_player.cont() # 继续播放音乐

    # 启动机器人
    def run(self):
        self.detector.start(detected_callback=self.detected_callback, speeched_callback=self.speeched_callback,
               interrupt_check=self.interrupt_callback,
               sleep_time=0.03)

SmartSpeaker().run()
