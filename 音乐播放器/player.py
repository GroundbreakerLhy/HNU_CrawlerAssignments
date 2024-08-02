# -*- coding=utf-8 -*-
'''
花了一点时间写的，音乐播放器
基本功能：播放音乐、上一首下一首切换，展示歌词，歌词追踪，根据链接下载音乐，自动播放
@Author:brucexia@tencent.com
@Date:23rd,Oct 2020
'''


import wx
import urllib.request
import pygame
import os
import re
import time
from threading import Thread
import math
import datetime

APP_TITLE = u'音乐播放器'
MAX_LYRIC_ROW = 18
LYRIC_ROW_REG = '\[[0-9]{2}:[0-9]{2}.[0-9]{2,}\]'
MAX_MUSIC_NAME_LEN = 15  # 歌名展示的时候最长字符限制


class mainFrame(wx.Frame):
    '''程序主窗口类，继承自wx.Frame'''

    def __init__(self):
        '''构造函数'''
        # 播放器的整体属性
        self.width = 1280
        self.height = 720
        self.volume = 0
        self.local_music_folder = "音乐播放器/music"
        wx.Frame.__init__(self, None, -1, APP_TITLE)
        self.SetSize(self.width, self.height)
        self.SetBackgroundColour((142, 169, 193))  # 设置界面的背景颜色为亮色

        # 音乐列表有关
        self.local_music_name_list = []  # 当前音乐名字列表
        self.lyrcis_static_text = []  # 当前播放的音乐的歌词列表
        self.play_stop_button = None  # 播放、暂停按钮
        self.current_music_state = 0  # 是否有音乐在播放，0表示否
        self.current_music_index = 0  # 当前音乐的索引

        # 初始化本地歌曲列表
        self.get_local_music_list()
        self.current_music_static_text = None  # 当前播放的音乐的名字

        # 按钮使用的图片
        self.play_bmp = wx.Image("音乐播放器/fig/play.bmp", wx.BITMAP_TYPE_BMP).Rescale(30, 30).ConvertToBitmap()
        self.stop_bmp = wx.Image("音乐播放器/fig/stop.bmp", wx.BITMAP_TYPE_BMP).Rescale(30, 30).ConvertToBitmap()

        # 导航栏所在的panel
        self.navi_panel = None
        self.draw_navi_panel()

        # 歌曲列表所在的panel
        self.music_list_panel = None
        self.draw_music_list_panel()

        # 播放部分所在的panel
        self.play_music_panel = None
        self.draw_play_music_panel()

        # 歌词部分所在的panel
        self.music_lyric_panel = None
        self.draw_music_lyric_panel()

        # 下载音乐面板
        self.down_music_panel = None
        self.input_url_text_ctrl = None  # 输入的下载路径
        self.down_button = None  # 下载按钮
        self.draw_down_music_panel()

        pygame.mixer.init()
        self.music = pygame.mixer.music
        self.SONG_FINISHED = pygame.USEREVENT + 1

    def get_path_by_name(self, file_name):
        '''
        通过名称获取音乐的完整路径
        :return:
        '''
        return os.path.join(self.local_music_folder, file_name)

    def get_local_music_list(self):
        '''
        获取本地音乐列表
        :return:
        '''
        self.local_music_name_list.clear()  # 这一步必须有
        for local_music_file_name in os.listdir(self.local_music_folder):
            if local_music_file_name.endswith(".mp3"):
                self.local_music_name_list.append(local_music_file_name)

    def draw_navi_panel(self):
        # 导航栏所在的panel
        self.navi_panel = wx.Panel(self, id=-1, pos=(0, 0), size=(100, self.height - 100))
        # 本地音乐
        local_music_text = wx.StaticText(self.navi_panel, -1, "本地音乐", pos=(20, 20), style=wx.ALIGN_LEFT)
        local_music_text.SetOwnForegroundColour((0, 0, 0))

    def draw_music_list_panel(self):
        '''
        绘制音乐列表所在的panel
        :param draw:
        :param show:
        :return:
        '''
        # 重新计算本地音乐列表
        self.get_local_music_list()
        # 绘制面板整体
        if self.music_list_panel is not None:
            self.music_list_panel.Destroy()
        self.music_list_panel = wx.Panel(self, id=-1, pos=(100, 0), size=(300, self.height - 100))
        # 音乐列表
        local_music_num = len(self.local_music_name_list)
        for music_index in range(local_music_num):
            music_full_name = self.local_music_name_list[music_index].replace(".mp3", "")
            if len(music_full_name) > MAX_MUSIC_NAME_LEN:
                music_full_name = music_full_name[0:MAX_MUSIC_NAME_LEN] + "..."
            music_text = wx.StaticText(self.music_list_panel, -1, music_full_name,
                                       pos=(0, music_index * 40 + 20), size=(270, 30), style=wx.ALIGN_RIGHT)
            music_text.SetOwnForegroundColour((0, 0, 0))
            music_text.Refresh()  # 这句话不能少
            play_button = wx.BitmapButton(self.music_list_panel, -1, self.play_bmp, pos=(280, music_index * 40 + 20),
                                            size=(20, 20))
            play_button.Bind(wx.EVT_LEFT_DOWN, lambda e, index=music_index: self.play_index_music(index))

    def draw_play_music_panel(self):
        # 播放音乐所在的panel
        self.play_music_panel = wx.Panel(self, id=-1, pos=(0, self.height - 100), size=(self.width, 100))
        # 歌的名字
        self.current_music_static_text = wx.StaticText(self.play_music_panel, -1, "请选择歌曲",
                                                        pos=(100, 15), size=(200, 30), style=wx.ALIGN_RIGHT)
        self.current_music_static_text.SetOwnForegroundColour((0, 0, 0))
        last_music_bpm = wx.Image("音乐播放器/fig/last.bmp", wx.BITMAP_TYPE_BMP).Rescale(30, 30).ConvertToBitmap()
        next_music_bpm = wx.Image("音乐播放器/fig/next.bmp", wx.BITMAP_TYPE_BMP).Rescale(30, 30).ConvertToBitmap()

        last_music_button = wx.BitmapButton(self.play_music_panel, -1, last_music_bpm, pos=(340, 15), size=(30, 30))
        self.play_stop_button = wx.BitmapButton(self.play_music_panel, -1, self.play_bmp,  pos=(380, 15), size=(30, 30))
        next_music_button = wx.BitmapButton(self.play_music_panel, -1, next_music_bpm, pos=(420, 15), size=(30, 30))
        # 调节音量的按钮
        volume_slider = wx.Slider(self.play_music_panel, -1, 50, 0, 100, pos=(500, 15), size=(570, -1), style=wx.SL_HORIZONTAL)

        # 上述按钮的监听器
        last_music_button.Bind(wx.EVT_LEFT_DOWN, self.play_last_music)
        self.play_stop_button.Bind(wx.EVT_LEFT_DOWN, self.play_stop_music)
        next_music_button.Bind(wx.EVT_LEFT_DOWN, self.play_next_music)
        volume_slider.Bind(wx.EVT_SLIDER, self.change_volume)

    def redraw_music_lyric_panel(self, start_index=0):
        # 隐藏之前的歌词的每一行
        for x in self.lyrcis_static_text:
            x.SetLabelText("")
            x.Refresh()

        # 获取歌词
        lyric_list = self.get_lyrics()
        # 展示歌词
        for lyric_index in range(start_index, start_index + MAX_LYRIC_ROW, 1):
            if lyric_index < len(lyric_list):
                lyric_relative_index = lyric_index - start_index
                lyric = lyric_list[lyric_index]
                self.lyrcis_static_text[lyric_relative_index].SetLabelText(lyric)
                self.lyrcis_static_text[lyric_relative_index].SetOwnForegroundColour((0, 0, 0))
                self.lyrcis_static_text[lyric_relative_index].Refresh()

    def draw_music_lyric_panel(self):
        '''
        歌词所在的面板的控制
        :return:
        '''
        self.music_lyric_panel = wx.Panel(self, id=-1, pos=(400, 60), size=(self.width - 400, self.height - 160))

        # 获取歌词
        lyric_list = self.get_lyrics()
        # 展示歌词
        for lyric_index in range(MAX_LYRIC_ROW):
            if lyric_index < len(lyric_list):
                lyric = lyric_list[lyric_index]
            else:
                lyric = ""
            lyric_row = wx.StaticText(self.music_lyric_panel, -1, lyric, pos=(300, 30 * lyric_index + 10),
                                    size=(200, -1), style=wx.ALIGN_CENTER_HORIZONTAL)
            lyric_row.SetOwnForegroundColour((0, 0, 0))
            self.lyrcis_static_text.append(lyric_row)

    def draw_down_music_panel(self):
        '''
        下载音乐所在的面板
        :return:
        '''
        self.down_music_panel = wx.Panel(self, id=-1, pos=(400, 0), size=(self.width - 400, 60))
        # 下载地址输入框
        self.input_url_text_ctrl = wx.TextCtrl(self.down_music_panel, -1, "请输入下载链接", pos=(100, 20), size=(600, 30))
        #self.input_url_text_ctrl.SetOwnBackgroundColour((63, 63, 63))
        # 绘制下载图标
        down_bmp = wx.Image("音乐播放器/fig/download.bmp", wx.BITMAP_TYPE_BMP).Rescale(30, 30).ConvertToBitmap()
        self.down_button = wx.BitmapButton(self.down_music_panel, -1, down_bmp, pos=(700, 20), size=(30, 30))
        # 监听下载图标按钮的鼠标点击事件
        self.down_button.Bind(wx.EVT_LEFT_DOWN, self.download_music)

    def get_lyric_path(self):
        current_music_path = self.get_path_by_name(self.local_music_name_list[self.current_music_index])
        lyric_path = current_music_path.replace(".mp3", ".lrc")
        if os.path.exists(lyric_path):
            return lyric_path
        else:
            return None

    def play_music(self):
        '''
        重新载入，播放音乐
        :return:
        '''
        current_music_path = self.get_path_by_name(self.local_music_name_list[self.current_music_index])
        self.music.load(current_music_path)
        # step1：播放音乐
        self.music.play(loops=1, start=0.0)
        # step2：重写歌词面板
        self.redraw_music_lyric_panel()
        # step3：开启新线程，追踪歌词
        self.display_lyric()
        self.current_music_state = 1
        self.play_stop_button.SetBitmap(self.stop_bmp)
        # 更改当前播放的音乐的名字
        current_music_name = self.local_music_name_list[self.current_music_index].replace(".mp3", "")
        if len(current_music_name) > MAX_MUSIC_NAME_LEN:
            current_music_name = current_music_name[0:MAX_MUSIC_NAME_LEN] + "..."
        self.current_music_static_text.SetLabelText(current_music_name)

    def play_index_music(self, music_index):
        '''
        播放指定索引的音乐
        :return:
        '''
        self.current_music_index = music_index
        # 载入音乐
        self.play_music()

    def play_stop_music(self, evt):
        if self.music.get_busy():  # 有音乐在播放，需要暂停，或者音乐暂停中
            if 1 == self.current_music_state:
                print("有音乐在播放，需要暂停")
                self.music.pause()
                self.current_music_state = 0
                self.play_stop_button.SetBitmap(self.play_bmp)
            else:  # 恢复暂停的音乐
                self.music.unpause()
                self.current_music_state = 1
                self.play_stop_button.SetBitmap(self.stop_bmp)
        else:  # 重新载入音乐
            self.play_music()

    def play_last_music(self, evt):
        # 计算上一首音乐的名字和路径
        if self.current_music_index > 0:
            self.play_index_music(self.current_music_index - 1)
        else:
            self.play_index_music(0)

    def play_next_music(self, evt):
        # 计算下一首音乐的名字和路径
        if self.current_music_index < len(self.local_music_name_list) - 1:
            self.play_index_music(self.current_music_index + 1)
        else:
            self.play_index_music(len(self.local_music_name_list) - 1)

    def change_volume(self, evt):
        '''
        修改音量
        :param evt:
        :return:
        '''
        obj = evt.GetEventObject()
        val = obj.GetValue()
        self.volume = float(val / 100)
        self.music.set_volume(self.volume)

    def get_lyrics(self):
        '''
        读取歌词，不带时间标记
        :param lyrics_file_path:
        :return:
        '''
        current_lyric_path = self.get_lyric_path()
        if current_lyric_path is None or not os.path.exists(current_lyric_path):
            return ["暂无歌词"]
        with open(current_lyric_path, 'r', encoding="utf-8") as file_pointer:
            content_list = file_pointer.readlines()
        lyrics_list = []
        for content in content_list:
            if re.match(LYRIC_ROW_REG, content):
                # 找到]符号第一次出现的地方
                index_of_right_blank = content.index(']')
                lyric_clause = content.replace('\n', '')[index_of_right_blank + 1:]
                lyrics_list.append(lyric_clause)
        return lyrics_list

    def display_lyric(self):
        lyric_refersh_thread = Thread(target=self.refersh_lyrics)
        lyric_refersh_thread.start()

    def parse_lyrics(self):
        current_lyric_path = self.get_lyric_path()
        if current_lyric_path is None or not os.path.exists(current_lyric_path):
            content_list = ["[00:00.00]暂无歌词"]
        else:
            # 读文件内容
            with open(current_lyric_path, 'r', encoding="utf-8") as file_pointer:
                content_list = file_pointer.readlines()
        lyrics_list = []
        for content in content_list:
            if re.match(LYRIC_ROW_REG, content):
                time_lyric = dict()
                start_time = float(content[1:3]) * 60 + float(content[4:6]) + float(content[7:9]) / 100
                index_of_right_blank = content.index(']')
                time_lyric[start_time] = content.replace('\n', '')[index_of_right_blank + 1:]
                lyrics_list.append(time_lyric)
        return lyrics_list

    def refersh_lyrics(self):
        '''
        刷新歌词子线程
        :return:
        '''
        lyrics_time_dict_list = self.parse_lyrics()
        relative_start_index = 0  # 相对起始歌词索引
        while self.music.get_busy():  # 播放中
            current_time = float(self.music.get_pos() / 1000)
            for lyric_index, lyrics_time_dict in enumerate(lyrics_time_dict_list):
                lyric_time = list(lyrics_time_dict.keys())[0]
                if math.fabs(lyric_time - current_time) < 0.7:
                    # 当歌词已经超过底部了，则刷新歌词面板，展示第二页的歌词
                    if lyric_index > 0 and lyric_index % MAX_LYRIC_ROW == 0:
                        relative_start_index = lyric_index
                        self.redraw_music_lyric_panel(start_index=relative_start_index)
                    self.lyrcis_static_text[lyric_index - relative_start_index].SetOwnForegroundColour((0, 0, 0))
                    # 这句话千万不能少，少了颜色不会刷新（来自调试了4个小时的忠告）
                    self.lyrcis_static_text[lyric_index - relative_start_index].Refresh()
                    break
            time.sleep(1)

    def download_music(self, evt):
        '''
        下载音乐
        :param evt:
        :return:
        '''
        # 获取文本框中输入的下载地址
        music_down_url = self.input_url_text_ctrl.GetValue()
        # 给下载的音乐在本地确定一个存储地址
        down_music_path = os.path.join(self.local_music_folder, datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + ".mp3")
        before_music_name = self.local_music_name_list[self.current_music_index]
        # 开始下载
        urllib.request.urlretrieve(music_down_url, down_music_path)
        # 下载完成后，重新绘制音乐列表面板
        self.draw_music_list_panel()
        # 调整当前音乐的索引
        for index in range(len(self.local_music_name_list)):
            if before_music_name == self.local_music_name_list[index]:
                self.current_music_index = index


if __name__ == "__main__":
    app = wx.App()
    frame = mainFrame()
    frame.Show()
    app.MainLoop()


