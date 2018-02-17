import numpy as np
import wx

BOARD_SIZE = 6
# black = 1, white = 0

class game_board():
    def __init__(self):
        self.board = -1*np.ones((BOARD_SIZE,BOARD_SIZE))
        self.board[int(BOARD_SIZE/2)-1][int(BOARD_SIZE/2)-1] = 1
        self.board[int(BOARD_SIZE/2)][int(BOARD_SIZE/2)] = 1
        self.board[int(BOARD_SIZE/2)][int(BOARD_SIZE/2)-1] = 0
        self.board[int(BOARD_SIZE/2)-1][int(BOARD_SIZE/2)] = 0

    def show_board(self):
        temp = np.array(self.board.copy())
        temp = temp.reshape(-1)
        temp = temp.tolist()
        for i in range(BOARD_SIZE*BOARD_SIZE):
            if temp[i] == -1:
                temp[i] = " "
            elif temp[i] == 0:
                temp[i] = "w"
            else:
                temp[i] = "b"
        temp = np.array(temp).reshape(BOARD_SIZE,BOARD_SIZE)
        print(" ",end="")
        print(np.array([str(x) for x in list(range(BOARD_SIZE))]))
        for i in range(BOARD_SIZE):
            print(i,end="")
            print(temp[i])

class MyApp(wx.Frame):
    def __init__(self,*args,**kw):
        super(MyApp,self).__init__(*args,**kw)
        self.size = 600
        self.offset = 50
        self.step = int((self.size-self.offset)/BOARD_SIZE)
        self.black_img = wx.Image("black.png").Scale(self.step*0.8,self.step*0.8,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.white_img = wx.Image("white.png").Scale(self.step*0.8,self.step*0.8,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.init_ui()
    def init_ui(self):
        self.SetTitle("オセロ")
        self.SetSize(self.size, self.size)
        self.Show()
        panels = {}
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                panels[i*BOARD_SIZE+j] = wx.Panel(self,-1,name = str(j*BOARD_SIZE+i),pos = (self.offset/2+self.step*i,10+self.step*j),size = (self.step,self.step))
        for p in panels.keys():
            panels[p].SetBackgroundColour((30,220,30))
            panels[p].Bind(wx.EVT_LEFT_DOWN,self.OnMouseLeftDown)
        for i in range(BOARD_SIZE+1):
            y = self.step*i
            wx.StaticLine(self, pos=(self.offset/2,10+self.step*i), size=(self.size-self.offset,3), style = wx.LI_HORIZONTAL)
        for i in range(BOARD_SIZE+1):
            x = self.step*i
            wx.StaticLine(self, pos=(self.offset/2+self.step * i,10), size=(3,self.size-self.offset), style = wx.LI_VERTICAL)
        wx.StaticBitmap(self, -1, self.black_img, pos=(self.offset / 2 + self.step * (int(BOARD_SIZE * BOARD_SIZE / 2 - 0.5 * BOARD_SIZE) % BOARD_SIZE + 0.1-1),10 + self.step * (int((BOARD_SIZE * BOARD_SIZE / 2 - 0.5 * BOARD_SIZE) / BOARD_SIZE) + 0.1)),size=self.black_img.GetSize())
        wx.StaticBitmap(self, -1, self.black_img, pos=(self.offset / 2 + self.step * (int(BOARD_SIZE * BOARD_SIZE / 2 - 0.5 * BOARD_SIZE) % BOARD_SIZE + 0.1),10 + self.step * (int((BOARD_SIZE * BOARD_SIZE / 2 - 0.5 * BOARD_SIZE) / BOARD_SIZE) + 0.1+1)),size=self.black_img.GetSize())
        wx.StaticBitmap(self, -1, self.white_img, pos=(self.offset / 2 + self.step * (int(BOARD_SIZE * BOARD_SIZE / 2 - 0.5 * BOARD_SIZE) % BOARD_SIZE + 0.1),10 + self.step * (int((BOARD_SIZE * BOARD_SIZE / 2 - 0.5 * BOARD_SIZE) / BOARD_SIZE) + 0.1)),size=self.white_img.GetSize())
        wx.StaticBitmap(self, -1, self.white_img, pos=(self.offset / 2 + self.step * (int(BOARD_SIZE * BOARD_SIZE / 2 - 0.5 * BOARD_SIZE) % BOARD_SIZE + 0.1-1),10 + self.step * (int((BOARD_SIZE * BOARD_SIZE / 2 - 0.5 * BOARD_SIZE) / BOARD_SIZE) + 0.1+1)),size=self.white_img.GetSize())

    def OnMouseLeftDown(self,event):
        p = event.GetEventObject()
        p_label = p.GetName()
        a1 = int(int(p_label)/BOARD_SIZE)
        a2 = int(p_label)%BOARD_SIZE
        wx.StaticBitmap(self,-1,self.black_img,pos=(self.offset/2+self.step*(a2+0.1),10+self.step*(a1+0.1)),size = self.black_img.GetSize())





app = wx.App()
MyApp(None)
app.MainLoop()