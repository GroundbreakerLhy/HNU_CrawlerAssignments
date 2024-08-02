import wx 
import os

APP_TITLE = u'小说阅读器'
MOST_DISPALY_LINES = 18
MAX_CONTENT_LINES = 18
MAX_CONTENT_NUM = 20
MAX_NOVAL_LINES = 50

class mainFrame(wx.Frame):
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.volume = 0
        self.local_noval_folder = '音乐播放器/小说阅读器/noval'
        wx.Frame.__init__(self, None, -1, APP_TITLE)
        self.SetSize(self.width, self.height)
        self.SetBackgroundColour((0, 0, 0))
        self.local_noval_name_list = []
        self.now_reading_index = 0
        self.now_reading = None
        self.noval_content = {}
        self.start_line = 0

        self.title_font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.text_font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

        self.navi_panel = None
        self.draw_navi_panel()

        self.content_panel = None
        self.draw_content_panel()

        self.noval_panel = None
        self.draw_noval_panel()

        self.page_panel = None
        self.draw_page_panel()
    
    def update_local_noval_name_list(self):
        self.local_noval_name_list.clear()
        for file in os.listdir(self.local_noval_folder):
            if file.endswith('.txt'):
                self.local_noval_name_list.append(file.replace('.txt', ''))

    def draw_navi_panel(self):
        self.navi_panel = wx.Panel(self, id=-1, pos=(0, 0), size=(180, self.height))
        self.navi_panel.SetForegroundColour(wx.WHITE)
        self.navi_panel.SetBackgroundColour((85, 245, 237))

        local_noval_text = wx.StaticText(self.navi_panel, -1, "文档列表", pos=(20, 20), style=wx.ALIGN_LEFT)
        local_noval_text.SetOwnForegroundColour((0, 0, 0))
        local_noval_text.SetFont(self.title_font)
        read_bmp = wx.Image('音乐播放器/小说阅读器/fig/read.bmp', wx.BITMAP_TYPE_BMP).Rescale(35, 35).ConvertToBitmap()

        self.update_local_noval_name_list()
        for noval_index in range(len(self.local_noval_name_list)):
            noval_name_text = wx.StaticText(self.navi_panel, -1, self.local_noval_name_list[noval_index], pos=(20, 100 + noval_index * 75), style=wx.ALIGN_LEFT)
            noval_name_text.SetOwnForegroundColour((0, 0, 0))
            noval_name_text.SetFont(self.text_font)
            noval_name_text.Refresh()

            read_button = wx.BitmapButton(self.navi_panel, -1, read_bmp, pos=(140, 85 + noval_index * 80), size=(35, 35))
            read_button.Bind(wx.EVT_LEFT_DOWN, lambda e, index=noval_index: self.read_index_content(index))

    def update_noval_content(self, noval_name):
        self.noval_content.clear()
        with open(os.path.join(self.local_noval_folder, noval_name + '.content'), 'r', encoding='utf-8') as f:
            for line in f.readlines():
                lst = line.split('\t')
                self.noval_content[lst[0]] = lst[1]

    def draw_content_panel(self):
        self.content_panel = wx.Panel(self, id=-1, pos=(180, 0), size=(320, self.height))
        self.content_panel.SetForegroundColour(wx.WHITE)
        self.content_panel.SetBackgroundColour(wx.GREEN)

        noval_name_text = wx.StaticText(self.content_panel, -1, "目录", pos=(20, 20), style=wx.ALIGN_LEFT)
        noval_name_text.SetOwnForegroundColour((0, 0, 0))
        noval_name_text.SetFont(self.title_font)

        if self.now_reading:
            self.update_noval_content(self.now_reading)
            self.start_line = 0
            read_bmp = wx.Image('音乐播放器/小说阅读器/fig/read.bmp', wx.BITMAP_TYPE_BMP).Rescale(15, 15).ConvertToBitmap()

            for i, content in enumerate(self.noval_content.keys()):
                content = content.replace(u'\u3000',u'')
                if len(content) > MAX_CONTENT_LINES:
                    content = content[:MAX_CONTENT_LINES - 3] + '...'
                if i == MAX_CONTENT_NUM - 1:
                    stop_here = wx.StaticText(self.content_panel, -1, "... ...", pos=(10, 80 + i * 30), style=wx.ALIGN_LEFT)
                    stop_here.SetOwnForegroundColour((0, 0, 0))
                    stop_here.SetFont(self.text_font)
                    stop_here.Refresh()
                    break

                noval_content = wx.StaticText(self.content_panel, -1, content, pos=(10, 80 + i * 30), style=wx.ALIGN_LEFT)
                noval_content.SetOwnForegroundColour((0, 0, 0))
                noval_content.SetFont(self.text_font)
                noval_content.Refresh()

                read_button = wx.BitmapButton(self.content_panel, -1, read_bmp, pos=(270, 75 + i * 30), size=(15, 15))
                read_button.Bind(wx.EVT_LEFT_DOWN, lambda e, index=i: self.read_index_noval())
        
        else:
            noval_content = wx.StaticText(self.content_panel, -1, '请选择小说', pos=(70, 360), style=wx.ALIGN_LEFT)
            noval_content.SetOwnForegroundColour((0, 0, 0))
            noval_content.SetFont(self.title_font)

    def redraw_contest_panel(self):
        self.content_panel.Destroy()
        self.draw_content_panel()

    def draw_noval_panel(self):
        self.noval_panel = wx.Panel(self, id=-1, pos=(500, 0), size=(self.width - 500, self.height - 150))
        self.noval_panel.SetForegroundColour(wx.WHITE)
        self.noval_panel.SetBackgroundColour((231, 234, 210))

        noval_text = wx.StaticText(self.noval_panel, -1, "正文", pos=(20, 20), style=wx.ALIGN_LEFT)
        noval_text.SetOwnForegroundColour((0, 0, 0))
        noval_text.SetFont(self.title_font)
        noval_text.Refresh()

        if self.now_reading:
            txt = open(os.path.join(self.local_noval_folder, self.now_reading + '.txt'), 'r', encoding='utf-8').read().replace(u'\u3000','').replace(u'\n', '')
            txt = [txt[i:i+35] for i in range(0, len(txt), 35)]
            now_reading_title = wx.StaticText(self.noval_panel, -1, self.now_reading, pos=(20, 60), style=wx.ALIGN_LEFT)
            now_reading_title.SetOwnForegroundColour((0, 0, 0))
            now_reading_title.SetFont(self.text_font)

            for i in range(MOST_DISPALY_LINES):
                dispaly = txt[self.start_line].replace(u'\u3000','')
                reading_txt = wx.StaticText(self.noval_panel, -1, dispaly, pos=(20, 100 + i * 30), style=wx.ALIGN_LEFT)
                reading_txt.SetOwnForegroundColour((0, 0, 0))
                reading_txt.SetFont(self.text_font)
                reading_txt.Refresh()
                self.start_line += 1
    
        else:
            noval_content = wx.StaticText(self.noval_panel, -1, '请选择小说', pos=(330, 275), style=wx.ALIGN_LEFT)
            noval_content.SetOwnForegroundColour((0, 0, 0))
            noval_content.SetFont(self.title_font)

    def draw_page_panel(self):
        self.page_panel = wx.Panel(self, id=-1, pos=(500, self.height - 150), size=(self.width - 500, 150))
        self.page_panel.SetForegroundColour(wx.WHITE)
        self.page_panel.SetBackgroundColour((255, 183, 183))

        string = f"正在阅读第 {self.start_line // MOST_DISPALY_LINES + 1} 页"
        page_panel_text = wx.StaticText(self.page_panel, -1, string, pos=(20, 20), style=wx.ALIGN_LEFT)
        page_panel_text.SetOwnForegroundColour((0, 0, 0))
        page_panel_text.SetFont(self.text_font)

        last_page_bmp = wx.Image('音乐播放器/小说阅读器/fig/last_page.bmp', wx.BITMAP_TYPE_BMP).Rescale(35, 35).ConvertToBitmap()
        next_page_bmp = wx.Image('音乐播放器/小说阅读器/fig/next_page.bmp', wx.BITMAP_TYPE_BMP).Rescale(35, 35).ConvertToBitmap()

        last_page_button = wx.BitmapButton(self.page_panel, -1, last_page_bmp, pos=(self.width - 500 - 100, 20), size=(35, 35))
        last_page_button.Bind(wx.EVT_LEFT_DOWN, lambda e: self.last_page())

        next_page_button = wx.BitmapButton(self.page_panel, -1, next_page_bmp, pos=(self.width - 500 - 50, 20), size=(35, 35))
        next_page_button.Bind(wx.EVT_LEFT_DOWN, lambda e: self.next_page())

    def read_index_content(self, index):
        self.now_reading_index = index
        self.read_content()

    def read_content(self):
        current_noval_path = os.path.join(self.local_noval_folder, self.local_noval_name_list[self.now_reading_index] + '.txt')
        self.now_reading = self.local_noval_name_list[self.now_reading_index]
        self.update_noval_content(self.now_reading)
        self.redraw_contest_panel()

    def read_index_noval(self):
        self.read_noval()

    def read_noval(self):
        self.draw_noval_panel()

    def last_page(self):
        if self.start_line > 0:
            self.start_line -= MOST_DISPALY_LINES
            self.draw_noval_panel()
            self.draw_page_panel()
    
    def next_page(self):
        if self.start_line < len(self.noval_content.keys()):
            self.draw_noval_panel()
            self.draw_page_panel()

if __name__ == "__main__":
    app = wx.App()
    frame = mainFrame()
    frame.Show()
    app.MainLoop()