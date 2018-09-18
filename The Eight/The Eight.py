import tkinter
from tkinter import messagebox
import os
import math
import random

global state
global result
global now
UI = tkinter.Tk()
UI.title("The eight")
UI.geometry("608x808")
UI.resizable(0,0)
StepStr = tkinter.StringVar()
NowstepStr = tkinter.StringVar()
StepStr.set("Total Step : ")
StepLable = tkinter.Label(UI,textvariable = StepStr,font=("微软雅黑", 15, 'italic'))
StepLable.place(x=7,y=90)

def runprogram() :
    os.system("main.exe")
    tkinter.messagebox.showinfo(title="Done",message="Calc finished")
    global result,now,NowstepStr
    now = 1
    resultFile = open("out.txt","r")
    result = str(resultFile.read()).split('\n')
    if result[0] != '-1' :
        StepStr.set("Total Step : "+ result[0])
        PreviousBut.config(state='active')
        NextBut.config(state='active')
        if now == 1 :
            PreviousBut.config(state='disabled')
        if now == int(result[0])+1 :
            NextBut.config(state='disabled')
        NowstepStr.set("Now : "+str(now-1))
        NowstepLabel = tkinter.Label(UI,textvariable=NowstepStr,font=("微软雅黑", 17))
        NowstepLabel.place(x=7,y=150)
    elif result[0] == '0' :
        StepStr.set("Total Step : " + "0")
        NowstepStr = tkinter.StringVar()
        NowstepStr.set("Now : "+str(now-1))
        NowstepLabel = tkinter.Label(UI, textvariable=NowstepStr, font=("微软雅黑", 17))
        NowstepLabel.place(x=7, y=150)
        PreviousBut.config(state='disabled')
        NextBut.config(state='disabled')
    else :
        StepStr.set("Total Step : " + "no solution")
        NowstepStr = tkinter.StringVar()
        NowstepStr.set("N/A")
        NowstepLabel = tkinter.Label(UI,textvariable=NowstepStr,font=("微软雅黑", 17))
        NowstepLabel.place(x=7,y=150)
    print(result)



Canvas = tkinter.Canvas(UI,bg="white",height=602,width=602)
Canvas.place(x=0,y=200)
TextIn = tkinter.Entry(UI,width=20,font=("微软雅黑", 20))
TextIn.place(x=10,y=50)
InputLabel = tkinter.Label(UI,text="Enter table here(split with space):",font=("微软雅黑", 20))
InputLabel.place(x=7,y=4)
ResultStepBut = tkinter.Button(UI,text="Calculate",font=("微软雅黑", 13),command=runprogram)
ResultStepBut.place(x=470,y=48)

def showeight() :
    File = open("in.txt", "r")
    state = (str(File.read())[:-1]).split(' ')
    print(state)
    for i in range(3, 405, 200):
        for j in range(3, 405, 200):
            if int(state[(i//200)+(j//200)*3]) == 0 :
                Canvas.create_rectangle(i, j, i + 200, j + 200, fill="white")
            else :
                Canvas.create_rectangle(i, j, i + 200, j + 200, fill="LightCyan")
            Canvas.create_text(i + 100, j + 100, text=int(state[(i//200)+(j//200)*3]), font=("微软雅黑", 40))


def writefile():
    Input = str(TextIn.get()).strip().split(' ')
    for i in range(0,9) :
        if not(str(i) in Input) :
            print("Yes")
            tkinter.messagebox.showwarning(title="Warning",message="Input illegal!")
            return
    File = open("in.txt","w")
    File.write(str(TextIn.get()+"\n"))
    File.close()
    showeight()


def showprevious():
    global now,result,NowstepStr
    now = now - 1
    NowstepStr.set("Now : " + str(now-1))
    if now == 1:
        PreviousBut.config(state='disabled')
    if now != int(result[0]) + 1:
        NextBut.config(state='active')
    tempres = result[now].split(' ')[:-1]
    for i in range(3, 405, 200):
        for j in range(3, 405, 200):
            if int(tempres[(i//200)+(j//200)*3]) == 0 :
                Canvas.create_rectangle(i, j, i + 200, j + 200, fill="white")
            else :
                Canvas.create_rectangle(i, j, i + 200, j + 200, fill="LightCyan")
            Canvas.create_text(i + 100, j + 100, text=int(tempres[(i//200)+(j//200)*3]), font=("微软雅黑", 40))


def shownext():
    global now,result,NowstepStr
    now = now + 1
    NowstepStr.set("Now : " + str(now-1))
    if now == int(result[0]) + 1:
        NextBut.config(state='disabled')
    if now != 1 :
        PreviousBut.config(state='active')
    tempres = result[now].split(' ')[:-1]
    for i in range(3, 405, 200):
        for j in range(3, 405, 200):
            if int(tempres[(i//200)+(j//200)*3]) == 0 :
                Canvas.create_rectangle(i, j, i + 200, j + 200, fill="white")
            else :
                Canvas.create_rectangle(i, j, i + 200, j + 200, fill="LightCyan")
            Canvas.create_text(i + 100, j + 100, text=int(tempres[(i//200)+(j//200)*3]), font=("微软雅黑", 40))


ShowBut = tkinter.Button(UI,text="Show",font=("微软雅黑", 13),command=writefile)
ShowBut.place(x=370,y=48)
PreviousBut = tkinter.Button(UI, text="Prev",font=("微软雅黑", 13), command=showprevious,state='disabled')
PreviousBut.place(x=410,y=150)
NextBut = tkinter.Button(UI, text="Next", font=("微软雅黑", 13),command=shownext,state='disabled')
NextBut.place(x=490,y=150)


if __name__ == '__main__':
    UI.mainloop()