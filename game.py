import numpy as np
import wx
from time import sleep

BOARD_SIZE = 6
# black = 1, white = -1

vs_cpu = 2
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
        self.num = 0
        self.size = 600
        self.offset = 50
        self.vs_cpu = vs_cpu
        self.turn = 1
        self.black_stone = 2
        self.white_stone = 2
        self.step = int((self.size-self.offset)/BOARD_SIZE)
        self.reverse_line = [[[] for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.placable = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.black_img = wx.Image("black.png").Scale(self.step*0.8,self.step*0.8,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.white_img = wx.Image("white.png").Scale(self.step*0.8,self.step*0.8,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.bitmaps = np.zeros((BOARD_SIZE,BOARD_SIZE)).tolist()
        # initializing osero board
        self.board = np.zeros((BOARD_SIZE,BOARD_SIZE))
        self.board[int(BOARD_SIZE / 2) - 1][int(BOARD_SIZE / 2) - 1] = 1
        self.board[int(BOARD_SIZE / 2)][int(BOARD_SIZE / 2)] = 1
        self.board[int(BOARD_SIZE / 2)][int(BOARD_SIZE / 2) - 1] = -1
        self.board[int(BOARD_SIZE / 2) - 1][int(BOARD_SIZE / 2)] = -1
        # initialized osero board
        self.pl_bool = True
        self.init_ui()
        if vs_cpu  == 2:
            self.cpu_play()
            self.flow = self.p2c
        elif vs_cpu == 0:
            self.flow = self.p2p
        else:
            self.flow = self.p2c
    def init_ui(self):
        self.SetTitle("オセロ")
        self.SetSize(self.size, self.size)
        self.Show()
        panels = {}
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                panels[i*BOARD_SIZE+j] = wx.Panel(self,-1,name = str(i*BOARD_SIZE+j),pos = (10+self.step*j,self.offset/2+self.step*i),size = (self.step,self.step))
        # initializing panels
        for p in panels.keys():
            panels[p].SetBackgroundColour((30,220,30))
            panels[p].Bind(wx.EVT_LEFT_DOWN,self.OnMouseLeftDown)
        # initialized panels
        for i in range(BOARD_SIZE+1):
            y = self.step*i
            wx.StaticLine(self, pos=(10,self.offset/2+self.step*i), size=(self.size-self.offset,3), style = wx.LI_HORIZONTAL)
        for i in range(BOARD_SIZE+1):
            x = self.step*i
            wx.StaticLine(self, pos=(10+self.step * i,self.offset/2), size=(3,self.size-self.offset), style = wx.LI_VERTICAL)
        for line in self.board_center():
            self.show_and_contain_bitmaps(line[0],line[1],line[2])

    def OnMouseLeftDown(self,event):
        p = event.GetEventObject()
        p_label = p.GetName()
        a1 = int(int(p_label)/BOARD_SIZE) # 行
        a2 = int(p_label)%BOARD_SIZE # 列
        self.flow(a1,a2)

    def p2p(self,a1,a2):
        if self.pl_bool:
            if self.can_place(a1,a2):
                self.board[a1][a2] = self.turn
                self.show_and_contain_bitmaps(a1,a2,self.turn)
                self.update_gui_board(self.reverse(a1,a2))
                self.turn = self.turn*-1
                self.placable_update()
                if not self.pl_bool:
                    print("player",end="")
                    print(self.turn)
                    print("has nowhere to put")
                    self.turn = self.turn*-1
                    self.placable_update()
                    if not self.pl_bool:
                        print("game set")
                        self.count()
            else:
                return 0

    def p2c(self,a1,a2):
        if self.pl_bool:
            if self.can_place(a1,a2):
                self.board[a1][a2] = self.turn
                self.show_and_contain_bitmaps(a1,a2,self.turn)
                self.update_gui_board(self.reverse(a1,a2))
                self.turn = self.turn*-1
                self.placable_update()
                if not self.pl_bool:
                    self.turn = self.turn*-1
                    print("cpu has nowhere to put")
                    self.placable_update()
                    if not self.pl_bool:
                        print("game set")
                        self.count()
                else:
                    self.cpu_loop()
            else:
                return 0

        else:
            return 0
    def cpu_loop(self):
        self.cpu_play()
        if not self.pl_bool:
            self.turn = self.turn * -1
            print("player has nowhere to put")
            self.placable_update()
            if not self.pl_bool:
                print("game set")
                self.count
            else:
                self.cpu_loop()

    def can_place(self,a1,a2):
        check_board = np.pad(self.board,[(1,1),(1,1)],"constant")
        out = False
        koma = self.turn
        a11 = a1+1
        a22 = a2+1
        choice = []
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                x = a11 + i
                y = a22 + j
                if koma*check_board[x][y] == -1:
                   choice.append([x,y])# 周囲に反対色の駒がある時、そっち方向はおける候補になるので、反対色の駒の座標を記録
        if len(choice) == 0:
            return False
        else:
            for i in range(len(choice)):
                choice[i][0] = choice[i][0]-a11
                choice[i][1] = choice[i][1]-a22
        reverse_line = []
        for line in choice:
            vector_k = 2
            while  abs(a11+vector_k*line[0]-((BOARD_SIZE-1)/2+1))<=((BOARD_SIZE-1)/2+1) and abs(a22+vector_k*line[1]-((BOARD_SIZE-1)/2+1))<=((BOARD_SIZE-1)/2+1):
                if check_board[a11+vector_k*line[0]][a22+vector_k*line[1]] == 0:
                    break
                if check_board[a11+vector_k*line[0]][a22+vector_k*line[1]] * koma == 1:
                    reverse_line.append([line[0],line[1]])
                    out = True
                    break
                vector_k += 1
        self.reverse_line[a1][a2] = reverse_line
        return  out

    def reverse(self,a1,a2):
        rev_change = []
        for line in self.reverse_line[a1][a2]:
            if len(line) != 0:
                vector_k = 1
                while abs(a1 + vector_k * line[0] - ((BOARD_SIZE - 1) / 2)) <= ((BOARD_SIZE - 1) / 2) and abs(a2 + vector_k * line[1] - ((BOARD_SIZE - 1) / 2)) <= ((BOARD_SIZE - 1) / 2):
                    if self.board[a1 + vector_k * line[0]][a2 + vector_k * line[1]] == self.turn*-1:
                        self.board[a1 + vector_k * line[0]][a2 + vector_k * line[1]] = self.turn
                        rev_change.append([a1 + vector_k * line[0], a2 + vector_k * line[1]])
                    else:
                        break
                    vector_k += 1

        self.black_stone += self.turn*len(rev_change)
        self.white_stone += -self.turn*len(rev_change)
        return  rev_change

    def placable_update(self):
        self.placable = [[False for i in range(BOARD_SIZE)] for j in range(BOARD_SIZE)]
        self.pl_bool = False
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0:
                    if self.can_place(i, j):
                        self.placable[i][j] = True
                        self.pl_bool = True

    def show_and_contain_bitmaps(self,a1,a2,stone):
        if stone == 1:
            self.bitmaps[a1][a2] = wx.StaticBitmap(self, -1, self.black_img,pos=(self.step * (a2 + 0.1)+10, self.step * (a1 + 0.1)+self.offset/2),size=self.black_img.GetSize())
        else:
            self.bitmaps[a1][a2] = wx.StaticBitmap(self, -1, self.white_img,pos=(self.step * (a2 + 0.1)+10, self.step * (a1 + 0.1)+self.offset/2),size=self.white_img.GetSize())

    def board_center(self):
        return ((int(BOARD_SIZE/2),int(BOARD_SIZE/2),1),(int(BOARD_SIZE/2)-1,int(BOARD_SIZE/2)-1,1),(int(BOARD_SIZE/2)-1,int(BOARD_SIZE/2),-1),(int(BOARD_SIZE/2),int(BOARD_SIZE/2)-1,-1))

    def update_gui_board(self,change):
        for line in change:
            self.bitmaps[line[0]][line[1]].Destroy()
            self.show_and_contain_bitmaps(line[0],line[1],self.turn)
    def cpu_play(self):
        if self.pl_bool:
            a1,a2 = self.cpu_think()
            self.board[a1][a2] = self.turn
            self.show_and_contain_bitmaps(a1,a2,self.turn)
            sleep(0.5)
            self.update_gui_board(self.reverse(a1,a2))
            self.turn = self.turn*-1
            self.placable_update()
    def cpu_think(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 0 and self.can_place(i,j):
                    return (i,j)
    def count(self):
        b = 0
        w = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == 1:
                    b+=1
                elif self.board[i][j] == -1:
                    w+=1
        print("white: ",end="")
        print(w)
        print("black: ",end="")
        print(b)
        if b > w:
            print("black win")
        elif w > b:
            print("white win")
        else:
            print("draw")


app = wx.App()
MyApp(None)
app.MainLoop()