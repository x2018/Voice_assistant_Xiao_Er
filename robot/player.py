# -*- coding:UTF-8 -*-
import pyaudio
import wave
import time
import subprocess

# 音频播放器
class Player():
    def __init__(self):
        pass

    def play_ding(self):
        ding_wav = wave.open("snowboy/resources/ding.wav", 'rb')
        ding_data = ding_wav.readframes(ding_wav.getnframes())
        audio = pyaudio.PyAudio()
        stream_out = audio.open(
            format=audio.get_format_from_width(ding_wav.getsampwidth()),
            channels=ding_wav.getnchannels(),
            rate=ding_wav.getframerate(), input=False, output=True)
        stream_out.start_stream()
        stream_out.write(ding_data)
        time.sleep(0.2)
        stream_out.stop_stream()
        stream_out.close()
        audio.terminate()

    def play_dong(self):
        ding_wav = wave.open("snowboy/resources/dong.wav", 'rb')
        ding_data = ding_wav.readframes(ding_wav.getnframes())
        audio = pyaudio.PyAudio()
        stream_out = audio.open(
            format=audio.get_format_from_width(ding_wav.getsampwidth()),
            channels=ding_wav.getnchannels(),
            rate=ding_wav.getframerate(), input=False, output=True)
        stream_out.start_stream()
        stream_out.write(ding_data)
        time.sleep(0.2)
        stream_out.stop_stream()
        stream_out.close()
        audio.terminate()

    def play_music(self, fname):
        print(fname)
        subprocess.Popen(['mpg123', '-q', fname]).wait()
        
# Player().play_music("http://music.163.com/song/media/outer/url?id=108485.mp3")