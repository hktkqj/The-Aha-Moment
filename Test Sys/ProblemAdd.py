import tkinter as tk
from  tkinter import filedialog
from  tkinter import *
import shutil
from tkinter import scrolledtext
import tkinter.messagebox
import os
import hashlib
import pymysql
import zipfile

Addroot =tkinter.Tk()
Addroot.title("Add new problem")
Addroot.geometry('521x820')
Addroot.resizable(0,0)

ProblemTitleLab = tkinter.Label(Addroot,font = ('微软雅黑',13),text='Enter problem title:')
ProblemTitleLab.place(x=0,y=0)
ProblemTitleEnt = tkinter.Entry(Addroot,font = ('微软雅黑',13),width=50)
ProblemTitleEnt.place(x=0,y=30)

ProblemDescriptionLab = tkinter.Label(Addroot,font= ('微软雅黑',13),text='Enter problem description:')
ProblemDescriptionLab.place(x=0,y=65)
ProblemDescriptionText = scrolledtext.ScrolledText(Addroot,font= ('微软雅黑',13),width=50,height=10,wrap=tk.WORD)
ProblemDescriptionText.place(x=0,y=95)

ProblemSolveLab = tkinter.Label(Addroot,font= ('微软雅黑',13),text='Enter problem solution:')
ProblemSolveLab.place(x=0,y=430)
ProblemSolveText = scrolledtext.ScrolledText(Addroot,font= ('微软雅黑',13),width=50,height=10,wrap=tk.WORD)
ProblemSolveText.place(x=0,y=460)


def SelectFile() :
    FileName = tkinter.filedialog.askopenfilename(filetypes=(("All File", "*"),("Image files", "*.jpg;*.jpeg;*.png;*.gif")))
    FileName = FileName.replace('/','\\')
    global Filepath,AddPicBut
    Filepath.set(FileName)
    ClearPicBut.config(state='active')
def ClearSet() :
    Filepath.set('')
    ClearPicBut.config(state='disabled')
AddPicLab = tkinter.Label(Addroot,font= ('微软雅黑',13),text='Add Picture? (Available type:.gif/.jpg/.jpeg)')
AddPicLab.place(x=0,y=345)
AddPicPathLab = tkinter.Label(Addroot,font= ('微软雅黑',12,'italic'),fg='black',text = 'Pic path:')
AddPicPathLab.place(x=0,y=393)
AddPicBut = tkinter.Button(Addroot,font= ('微软雅黑',13),text='Select*',width=6,height=1,command=SelectFile)
AddPicBut.place(x=400,y=340)
ClearPicBut = tkinter.Button(Addroot,font= ('微软雅黑',13),text='Clear',width=6,height=1,state='disabled',command=ClearSet)
ClearPicBut.place(x=400,y=390)

Filepath = tkinter.StringVar()
Filepath.set('')
PicPathEnt = tkinter.Entry(Addroot,font= ('微软雅黑',12,'italic'),width=33,state='readonly',textvariable=Filepath)
PicPathEnt.place(x=80,y=396)

def DoubleCheck() :
    global Filepath,ProblemTitleEnt,ProblemSolveText,ProblemDescriptionText
    if Filepath.get()!='' or ProblemTitleEnt.get()!='' or len(ProblemSolveText.get("0.0","end"))>1 or len(ProblemDescriptionText.get("0.0","end"))>1 :
        if tkinter.messagebox.askyesno(title='Cancel',message='Abandon Edit?') :
            Addroot.destroy()
        return
    else :
        Addroot.destroy()

def Submit() :
    if ProblemTitleEnt.get() == '' or len(ProblemSolveText.get("0.0", "end")) <= 1 or len(ProblemDescriptionText.get("0.0", "end")) <= 1:
        tkinter.messagebox.showwarning(title='Submit',message='Please complete problem description!')
        return
    if tkinter.messagebox.askyesno(title='Submit', message='Confirm upload Problem?\nTitle: '+ProblemTitleEnt.get()+"\nPoint: "+str(v.get())):
        db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
        cursor = db.cursor()
        InsertSQL = """INSERT INTO problem (ProblemName,ProblemDescriptionFile,WorthPoint,TotalRank,TotalRankedPeoPle,UploadPeople)
                        VALUES ('%s','',%d,0,0,'%s')""" % (ProblemTitleEnt.get(),v.get(),NowUser)
        try :
            cursor.execute(InsertSQL)
            db.commit()
        except :
            tkinter.messagebox.showwarning(title='Warning', message='Database Corrupted！Program shutdown2&^%$#@')
            db.rollback()
        QuerySQL = """SELECT * FROM problem"""
        cursor.execute(QuerySQL)
        NowUID = str(cursor.fetchall()[-1][-1])

        CurrentPath=os.getcwd()+'\\Tempfile\\'
        ProblemPath=os.getcwd()+'\\Problems\\'
        fp = open(CurrentPath+'Description.txt',"w+")
        fp.write(ProblemDescriptionText.get("0.0", "end").rstrip("\n"))
        fp.close()
        fp1 = open(CurrentPath+'Solve.txt',"w+")
        fp1.write(ProblemSolveText.get("0.0", "end").rstrip("\n"))
        fp1.close()
        if Filepath.get()!='' :
            FileAbsName=Filepath.get().split('\\')[-1]
            FileAbsType=FileAbsName.split('.')[-1]
            command = """copy "%s" "%s" /Y"""%(Filepath.get(),CurrentPath)
            os.system(command)
            command = """rename "%s" "%s" """ % (CurrentPath+FileAbsName,"Photo."+FileAbsType)
            os.system(command)
        ZipFile = zipfile.ZipFile(CurrentPath+NowUID+".zip","w")
        ZipFile.write(CurrentPath+'Description.txt','Description.txt')
        ZipFile.write(CurrentPath+'Solve.txt','Solve.txt')
        if Filepath.get() != '':
            ZipFile.write(CurrentPath+'Photo.'+FileAbsType,'Photo.'+FileAbsType)
        ZipFile.close()
        command = """copy "%s" "%s" /Y"""%(CurrentPath+NowUID+'.zip',ProblemPath)
        os.system(command)
        if os.path.exists(os.getcwd() + "\\Tempfile\\Description.txt"):
            os.remove(os.getcwd() + "\\Tempfile\\Description.txt")
        if os.path.exists(os.getcwd() + "\\Tempfile\\Solve.txt"):
            os.remove(os.getcwd() + "\\Tempfile\\Solve.txt")
        if os.path.exists(os.getcwd() + "\\Tempfile\\Photo.gif"):
            os.remove(os.getcwd() + "\\Tempfile\\Photo.gif")
        os.system(command)
        NewProblemPath = (ProblemPath + NowUID + ".zip").replace("\\","\\\\")
        UpdateSQL1 = """UPDATE problem SET ProblemDescriptionFile='%s' WHERE UID=%d """ % (NewProblemPath,int(NowUID))
        try :
            cursor.execute(UpdateSQL1)
            db.commit()
            tkinter.messagebox.showinfo(title="Add new problem",message="Add successfully")
            Addroot.destroy()
        except :
            tkinter.messagebox.showwarning(title='Warning', message='Database Corrupted！Program shutdown')
            db.rollback()

SubmitBut = tkinter.Button(Addroot,font= ('微软雅黑',13),text='Submit',width=8,height=1,command=Submit)
SubmitBut.place(x=100,y=760)
CancelBut = tkinter.Button(Addroot,font= ('微软雅黑',13),text='Cancel',width=8,height=1,command=DoubleCheck)
CancelBut.place(x=320,y=760)
ScoreLab = tkinter.Label(Addroot,font= ('微软雅黑',13),text='Score:')
ScoreLab.place(x=50, y=710)
PointStr = tkinter.StringVar()
PointStr.set("")
ScoreNumLab = tkinter.Label(Addroot,font= ('微软雅黑',13),textvariable=PointStr)
ScoreNumLab.place(x=390,y=713)
v = tkinter.IntVar()
ScoreScale = tkinter.Scale(Addroot,from_=1,to=10,orient=HORIZONTAL,resolution=1,tickinterval=1,length=200,variable=v)
ScoreScale.place(x=150,y=695)
def ChangePoint(event) :
    if v.get()!=10 :
        PointStr.set(str(v.get())+"  Point")
    else:
        PointStr.set(str(v.get()) + " Point")
ScoreScale.bind("<B1-Motion>",ChangePoint)

if __name__ == '__main__':
    if os.path.exists(os.getcwd()+"\\Tempfile\\Addproblem") :
        File = open(os.getcwd()+"\\Tempfile\\Addproblem","r")
        NowUser = File.read()
        Addroot.mainloop()
        File.close()
        os.remove(os.getcwd()+"\\Tempfile\\Addproblem")
        Addroot.destroy()
    else:
        tkinter.messagebox.showerror(title="Error!",message="Illegal Login!")
