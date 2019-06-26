# -*- coding:UTF-8 -*-
import requests 
import time
import random

# 名词解释
class Noun():
    def __init__(self, speaker = None):
        self.speaker = speaker

    def process(self, response):
        action_list = response['action_list']
        says = []
        for action in action_list:
            says.append(action['say'])
        tex = random.choice(says)
        self.speaker.speak(tex)
    