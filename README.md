## 运行环境

- Ubuntu 14.04
- Python 2.7

## 功能介绍

简单的语音助手实现。可以进行询问天气、二等座车票、基本问答以及播放音乐等相关功能。

## 语音助手

- 目录结构
  - robot  ： 存放核心功能的各个模块
    - skills  ： 存放各项技能的实现
      - chat.py  ：闲聊内容输出
      - noun_interpretaion.py ：名词解释
      - ticket.py  ：查询车票(二等座)
      - weather.py ：查询天气(武汉)
      - music.py ：音乐播放控制模块
      - music_api.py ：获取网易云音乐中的歌曲与id对应关系
    - music_player.py  ： 音乐播放器     
    - player.py  ：音频播放器
    - recognition.py  ： 语音识别
    - nlu.py  ：  自然语言处理(语义识别)
    - sperker.py  ：语音合成
    - robot.py  ： 功能调度模块
  - snowboy ：存放snowboy的相关模块(加工处理后的)
    - resources ：资源存放(响应词等)
    - snowboydecoder.py ：根据唤醒词识别模型来对唤醒词进行识别，可在此做修改
    - snowboydetect.py ：snowboy核心模块，最好不要做修改
  - main.py ：核心控制模块
  - .pmdl为唤醒词识别模型

## Linux 配置

1. apt-get install git
2. apt-get install vim
3. apt-get install python-pyaudio python3-audio sox
4. apt-get install gcc python3-pip python-pip
5. apt-get install libatlas-base-dev
6. apt-get install swig3.0
7. apt-get install libpcre3 libpcre3-dev
8. pip install mpg123
9. pip install baidu-aip
10. pip install pycrypto

## 参考

[1] Snowboy Hotword Detection：语音唤醒的开源框架. <https://snowboy.kitt.ai/>

[2] THULAC：高效的中文词法分析工具包. <http://thulac.thunlp.org/>

[3] THCHS-30：免费的汉语语料库. <http://www.openslr.org/18/>

[4] RASA：构建上下文聊天的开源框架 . <http://rasa.com/docs/>

[5] 百度AI开放平台API开发指南. <http://ai.baidu.com/docs#/>

[6] 科大讯飞REST API用户开发指南. <https://doc.xfyun.cn/rest_api/>