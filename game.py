import numpy as np
import wx

BOARD_SIZE = 6
# black = 1, white = -1

vs_cpu = 0
# 0:player vs player, 1:player vs cpu, 2:cpu vs player

class game_board():
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE,BOARD_SIZE))
        self.board[int(BOARD_SIZE/2)-1][int(BOARD_SIZE/2)-1] = 1
        self.board[int(BOARD_SIZE/2)][int(BOARD_SIZE/2)] = 1
        self.board[int(BOARD_SIZE/2)][int(BOARD_SIZE/2)-1] = -1
        self.board[int(BOARD_SIZE/2)-1][int(BOARD_SIZE/2)] = -1

    def show_board(self):
        temp = np.array(self.board.copy())
        temp = temp.reshape(-1)
        temp = temp.tolist()
        for i in range(BOARD_SIZE*BOARD_SIZE):
            if temp[i] == 0:
                temp[i] = " "
            elif temp[i] == -1:
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
        self.vs_cpu = vs_cpu
        self.turn = "b"
        self.step = int((self.size-self.offset)/BOARD_SIZE)
        self.black_img = wx.Image("black.png").Scale(self.step*0.8,self.step*0.8,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.white_img = wx.Image("white.png").Scale(self.step*0.8,self.step*0.8,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        # initializing osero board
        self.board = np.zeros((BOARD_SIZE,BOARD_SIZE))
        self.board[int(BOARD_SIZE / 2) - 1][int(BOARD_SIZE / 2) - 1] = 1
        self.board[int(BOARD_SIZE / 2)][int(BOARD_SIZE / 2)] = 1
        self.board[int(BOARD_SIZE / 2)][int(BOARD_SIZE / 2) - 1] = -1
        self.board[int(BOARD_SIZE / 2) - 1][int(BOARD_SIZE / 2)] = -1
        # initialized osero board
        self.init_ui()
    def init_ui(self):
        self.SetTitle("オセロ")
        self.SetSize(self.size, self.size)
        self.Show()
        panels = {}
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                panels[i*BOARD_SIZE+j] = wx.Panel(self,-1,name = str(j*BOARD_SIZE+i),pos = (self.offset/2+self.step*i,10+self.step*j),size = (self.step,self.step))
        # initializing panels
        for p in panels.keys():
            panels[p].SetBackgroundColour((30,220,30))
            panels[p].Bind(wx.EVT_LEFT_DOWN,self.OnMouseLeftDown)
        # initialized panels
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
        a1 = int(int(p_label)/BOARD_SIZE) # 行
        a2 = int(p_label)%BOARD_SIZE # 列
        if self.turn == "b":
            if self.vs_cpu == 0 or self.vs_cpu == 1:
                if self.can_place(a1,a2) == True:
                    wx.StaticBitmap(self,-1,self.black_img,pos=(self.offset/2+self.step*(a2+0.1),10+self.step*(a1+0.1)),size = self.black_img.GetSize())
                    self.board[a1][a2] = 1
                    self.reverse()
                    if self.vs_cpu == 0:
                        self.turn = "w"
                    else:
                        self.cpu_play()
                        self.reverse()
        elif self.turn == "w":
            if self.vs_cpu == 0 or self.vs_cpu == 2:
                if self.can_place(a1,a2) == True:
                    wx.StaticBitmap(self, -1, self.white_img,pos=(self.offset / 2 + self.step * (a2 + 0.1), 10 + self.step * (a1 + 0.1)),size=self.black_img.GetSize())
                    self.board[a1][a2] = -1
                    self.reverse()
                    if self.vs_cpu == 0:
                        self.turn = "b"
                    else:
                        self.cpu_play()
                        self.reverse()
    def can_place(self,a1,a2):
        check_board = np.pad(self.board,[(1,1),(1,1)],"constant")
        out = False
        if self.turn == "b":
            koma = 1
        else:
            koma = -1
        a1 = a1+1
        a2 = a2+1
        choice = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x = a1 + i
                y = a2 + j
                if koma*check_board[x][y] == -1:
                   choice.append((x,y))# 周囲に反対色の駒がある時、そっち方向はおける候補になるので、反対色の駒の座標を記録
        return  out

    def reverse(self):
        pass

    def cpu_play(self):
        pass


app = wx.App()
MyApp(None)
app.MainLoop()