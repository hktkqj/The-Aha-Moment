import tkinter
import random
import math
from tkinter import messagebox

global GameMap
global Canvas
global Flag
global Point
global HighScore
Canvas = tkinter.Tk()
Canvas.title("2048?")
Canvas.geometry('608x808')
Canvas.resizable(0, 0)
ScoreLabel = tkinter.Label(Canvas,text='Score :',font =("微软雅黑",20))
ScoreLabel.place(x=10,y=10)
Score = tkinter.StringVar()
Score.set('0')
ScoreLabelNum = tkinter.Label(Canvas,textvariable=Score,font =("微软雅黑",20))
ScoreLabelNum.place(x=170,y=11)

HighScoreLabel = tkinter.Label(Canvas,text='High Score :',font =("微软雅黑",20))
HighScoreLabel.place(x=10,y=60)
HighScore1 = tkinter.StringVar()
HighScore1.set('0')
HighScoreLabelNum = tkinter.Label(Canvas,textvariable=HighScore1,font =("微软雅黑",20))
HighScoreLabelNum.place(x=170,y=60)
Draw = tkinter.Canvas(Canvas, bg='white', height=602, width=602)  # 0,150,300,450
Draw.place(x=0, y=200)
HintLab = tkinter.Label(Canvas,text="Press w,a,s,d to move blocks",font =("微软雅黑",15,'italic'))
HintLab.place(x=10,y=170)

NumColor = ['White','Ivory','LemonChiffon','Khaki','Orange','DarkOrange','Tomato','OrangeRed','FireBrick','Maroon','Gray','DarkGray','DimGray']

def RandomGenerator() :
    global GameMap
    while True :
        x = random.randint(0,3)
        y = random.randint(0,3)
        if GameMap[x][y] == 0 :
            GameMap[x][y] = random.randrange(2,5,2)
            return

def Merge(Command) :
    global GameMap,Flag,Point
    Flag = False
    Move(Command)
    if Command == "u" :
        for i in range(1,4):
            for j in range(0,4) :
                now = i
                if GameMap[now - 1][j] == GameMap[now][j] :
                    GameMap[now - 1][j] = GameMap[now][j] *2
                    GameMap[now][j] = 0
                    if GameMap[now - 1][j] != 0 :
                        Flag = True
                        Point = Point + GameMap[now - 1][j]
    elif Command == "d":
        for i in range(2, -1, -1):
            for j in range(0, 4):
                now = i
                if GameMap[now + 1][j] == GameMap[now][j] :
                    GameMap[now + 1][j] = GameMap[now][j] *2
                    GameMap[now][j] = 0
                    if GameMap[now + 1][j] != 0 :
                        Flag = True
                        Point = Point + GameMap[now + 1][j]
    elif Command == "l":
        for i in range(1, 4):
            for j in range(0, 4):
                now = i
                if GameMap[j][now - 1] == GameMap[j][now] :
                    GameMap[j][now - 1] = GameMap[j][now] *2
                    GameMap[j][now] = 0
                    if GameMap[j][now - 1] != 0 :
                        Flag = True
                        Point = Point + GameMap[j][now - 1]
    elif Command == "r":
        for i in range(2, -1, -1):
            for j in range(0, 4):
                now = i
                if GameMap[j][now + 1] == GameMap[j][now] :
                    GameMap[j][now + 1] = GameMap[j][now] *2
                    GameMap[j][now] = 0
                    if GameMap[j][now + 1] != 0 :
                        Flag = True
                        Point = Point + GameMap[j][now + 1]
    Move(Command)

def Move(Command) :
    global GameMap,Flag
    if Command == "u" :
        for i in range(1,4) :
            for j in range(0,4) :
                now = i
                while now >=1 and GameMap[now-1][j] == 0 and GameMap[now][j] !=0 :
                    GameMap[now-1][j] = GameMap[now][j]
                    GameMap[now][j] = 0
                    now = now - 1
                    Flag = True
    elif Command == "d" :
        for i in range(2,-1,-1) :
            for j in range(0,4) :
                now = i
                while now <=2 and GameMap[now+1][j] == 0 and GameMap[now][j] !=0 :
                    GameMap[now+1][j] = GameMap[now][j]
                    GameMap[now][j] = 0
                    now = now + 1
                    Flag = True
    elif Command == "l" :
        for i in range(1,4) :
            for j in range(0,4) :
                now = i
                while now >=1 and GameMap[j][now-1] == 0 and GameMap[j][now] !=0 :
                    GameMap[j][now-1] = GameMap[j][now]
                    GameMap[j][now] = 0
                    now = now - 1
                    Flag = True
    elif Command == "r" :
        for i in range(2,-1,-1) :
            for j in range(0,4) :
                now = i
                while now <=2 and GameMap[j][now+1] == 0 and GameMap[j][now] !=0 :
                    GameMap[j][now+1] = GameMap[j][now]
                    GameMap[j][now] = 0
                    now = now + 1
                    Flag = True

def CheckMove() :
    for i in range(0, 4):
        for j in range(0, 4) :
            if GameMap[i][j] == 0 :
                return True
    for i in range(1,4):
        for j in range(0,4) :
            if GameMap[i - 1][j] == GameMap[i][j] :
                return True
    for i in range(2, -1, -1):
        for j in range(0, 4):
            if GameMap[i + 1][j] == GameMap[i][j] :
                return True
    for i in range(1, 4):
        for j in range(0, 4):
            if GameMap[j][i - 1] == GameMap[j][i] :
                return True
    for i in range(2, -1, -1):
        for j in range(0, 4):
            if GameMap[j][i + 1] == GameMap[j][i] :
                return True
    return False

def DrawWindows() :
    for i in range(3,455,150) :
        for j in range(3, 455, 150) :
            if GameMap[i//150][j//150] != 0 :
                Draw.create_rectangle(i,j,i+150,j+150,fill=NumColor[int(math.log(GameMap[i//150][j//150],2))])
            else:
                Draw.create_rectangle(i, j, i + 150, j + 150,fill='white')
            if GameMap[i//150][j//150] != 0:
                Draw.create_text(i+75,j+75,text=str(GameMap[i//150][j//150]),font=("微软雅黑",34))

def CheckKey(event) :
    if event.char == 'w' :
        Merge('l')
        if Flag == True :
            RandomGenerator()
    elif event.char == 'a' :
        Merge('u')
        if Flag == True :
            RandomGenerator()
    elif event.char == 's' :
        Merge('r')
        if Flag == True :
            RandomGenerator()
    elif event.char == 'd' :
        Merge('d')
        if Flag == True :
            RandomGenerator()
    DrawWindows()
    global Point,HighScore
    Score.set(str(Point))
    if CheckMove() == False :
        tkinter.messagebox.showinfo(title="Over!",message='Your score :'+str(Point))
        if Point > HighScore :
            HighScore = Point
            HighScore1.set(str(HighScore))

def Restart() :
    Initiialize()
RestartBut = tkinter.Button(Canvas,text="Restart?",font=("微软雅黑",20),command = Restart,width=10,height=4)
RestartBut.place(x=420,y=20)

def Initiialize() :
    global GameMap,Canvas,Point
    Point = 0
    Score.set(Point)
    GameMap = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    RandomGenerator()
    Canvas.bind("<Key>",CheckKey)
    DrawWindows()

if __name__ == '__main__':
    global HighScore
    HighScore = 0
    Initiialize()
    Canvas.mainloop()
