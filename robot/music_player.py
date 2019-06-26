# -*- coding:UTF-8 -*-
import subprocess
import signal
import time
import threading
import random 

# 音乐播放控制模块
class Music_Player():
    def __init__(self):
        #super(Music_Player, self).__init__()
        self.music_list = []
        self.P = None
        t = threading.Thread(target=self.check_music)
        t.start()
        self.mode = 0

    def check_music(self):
        while True:
            time.sleep(10)
            if self.P is not None and self.P.poll() is not None:
                self.next_music()

    def set_musci_list(self, music_list):
        self.music_list = music_list
        self.cur_id = 0
        self.stop()

    def get_url(self):
        url = "http://music.163.com/song/media/outer/url?id="
        url += str(self.music_list[self.cur_id]['id'])
        url += ".mp3"
        return url

    def play_music(self):
        if self.music_list == []:
            return
        url = self.get_url()
        print("正在播放" + str(self.music_list[self.cur_id]['ar'][0]['name']) + "的" + str(self.music_list[self.cur_id]['name']))
        print(url)
        self.P = subprocess.Popen(['mpg123', '-q', url])
    
    def stop(self):
        if self.P is not None:
            self.P.send_signal(signal.SIGINT)
            self.P = None

    def pause(self):
        if self.P is not None:
            self.P.send_signal(signal.SIGSTOP)

    def cont(self):
        if self.P is not None:
            self.P.send_signal(signal.SIGCONT)
    
    def next_music(self):
        #self.stop()
        if self.mode == 0:
            self.cur_id += 1
            if self.cur_id == len(self.music_list):
                self.cur_id = 0
        elif self.mode == 1:
            self.cur_id = random.randint(0, len(self.music_list) - 1)
        self.play_music()

    def change_mode(self, mode):
        if mode == "循环":
            self.mode = 0
        elif mode == "随机":
            self.mode = 1