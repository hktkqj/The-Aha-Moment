from  tkinter import simpledialog
from  tkinter import *
from PIL import ImageTk
import shutil
from tkinter import scrolledtext
import tkinter.messagebox
import os
import hashlib
import pymysql
import zipfile

global DescriptionImage,NowIndex,DescriptionImage1
DescriptionImage1=[]
UserRanked = []
InTest = []
for index in range(0,10086) :
    UserRanked.append(-1)
Flag = ""
root = tkinter.Tk()
root.geometry('1024x768')
root.resizable(0,0)
root.title("Problems")

def ShowAuthority() :
    global Flag
    if Flag == "Admin" :
        tkinter.messagebox.showinfo(title="Authority",
                                    message="You are login with "+Flag+".\nYou could : View all problems/tests, Submit new problem, Edit problems, Create new test.")
    else :
        tkinter.messagebox.showinfo(title="Authority",
                                    message="You are login with " + Flag + ".\nYou could  : View all problems, View all tests.")

def Import() :
    try :
        db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
        cursor = db.cursor()
        ProblemInfoSQL = "SELECT * FROM problem"
        TestInfoSQL = "SELECT * FROM test"
        cursor.execute(ProblemInfoSQL)
        global ProblemInfo
        ProblemInfo = cursor.fetchall()
        TestInfoSQL = "SELECT * FROM test"
        global TestInfo
        cursor.execute(TestInfoSQL)
        TestInfo = cursor.fetchall()
        db.close()
    except :
        tkinter.messagebox.showerror(title="Error",message="Database currupted! Try re-build by firstrun.py.")
        db.close()
    global ProblemBut,TestBut
    ProblemBut.config(state="active")
    TestBut.config(state="active")

MenuBar =tkinter.Menu(root)
FileMenu = tkinter.Menu(MenuBar)
MenuBar.add_cascade(label='File',menu=FileMenu)
FileMenu.add_command(label='Import',command = Import)
FileMenu.add_command(label='Exit',command = root.destroy)
MenuBar.add_command(label='About', command=ShowAuthority)
EditMenu = tkinter.Menu(MenuBar)
def NewCommand() :
    if TestBut['state'] == "active" :#Add new problem
        TempUserFile = open(os.getcwd()+"\\Tempfile\\Addproblem","w")
        TempUserFile.write(NowUser)
        TempUserFile.close()
        os.system("python ProblemAdd.py")
        Import()
        ShowProblem()
    elif ProblemBut['state'] == "active" :
        if len(InTest)==0 :
            tkinter.messagebox.showwarning(title="Warning",message="Please selecet problem first.")
        else :
            ProblemsetStr=""
            TotalPoint = 0
            for indexnum in InTest :
                ProblemsetStr=ProblemsetStr+str(indexnum)+","
                for problem in ProblemInfo :
                    if problem[6]==indexnum :
                        TotalPoint = TotalPoint + problem[2]
                        break
            TestTitle=simpledialog.askstring("Title","Enter title for new test:")
            if len(TestTitle)!=0 :
                if tkinter.messagebox.askyesno(title="Create new test?",message="Confirm create new test?\nTitle: "+TestTitle+"\nProblems: "+ProblemsetStr+"\nTotal point: "+str(TotalPoint)) :
                    db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
                    cursor = db.cursor()
                    InsertSQL = """INSERT INTO test (TestName,ProblemSet, ProblemNumber, TotalPoint, CreateUser) VALUES ('%s','%s',%d,%d,'%s')""" % (TestTitle,ProblemsetStr,len(InTest),TotalPoint,NowUser)
                    try :
                        cursor.execute(InsertSQL)
                        db.commit()
                        tkinter.messagebox.showinfo(title="Create",message="Create new test successfully")
                    except:
                        db.rollback()
                        tkinter.messagebox.showerror(title="Delete", message="Delete failed, database currupted!")
                    finally:
                        db.close()
                    while len(InTest)!=0 :
                        del InTest[0]
                    ShowTest()

def EditCommand() :
    if TestBut['state'] == "active":  # Edit probelm
        TempUserFile = open(os.getcwd() + "\\Tempfile\\Editproblem", "w")
        TempUserFile.write(str(ProblemInfo[NowIndex][6]))
        TempUserFile.close()
        os.system("python ProblemEdit.py")
        Import()
        ShowProblem()
    elif ProblemBut['state'] == "active" :
        return
def DeleteCommand() :
    if TestBut['state'] == "active" :#delete problem
        if tkinter.messagebox.askyesno(title="Delete",message="""Are you sure to delete problem '%s'? \n(UID=%d)"""%(ProblemInfo[NowIndex][0],ProblemInfo[NowIndex][6])) :
            DeleteProblemSQL = """DELETE FROM problem WHERE UID=%d """ % ProblemInfo[NowIndex][6]
            db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
            cursor = db.cursor()
            try :
                cursor.execute(DeleteProblemSQL)
                db.commit()
                os.remove(os.getcwd()+"\\Problems\\%d.zip"%int(ProblemInfo[NowIndex][6]))
                tkinter.messagebox.showinfo(title="Delete", message="Delete successfully")
                Import()
                ShowProblem()
            except :
                db.rollback()
                tkinter.messagebox.showerror(title="Delete", message="Delete failed, database currupted!")
            finally :
                db.close()
            Import()
            ShowProblem()
    elif ProblemBut['state'] == "active" :
        if tkinter.messagebox.askyesno(title="Delete",message="""Are you sure to delete test '%s'? \n(UID=%d)"""%(TestInfo[NowIndex][0],TestInfo[NowIndex][5])) :
            DeleteProblemSQL = """DELETE FROM test WHERE UID=%d """ % TestInfo[NowIndex][5]
            db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
            cursor = db.cursor()
            try :
                cursor.execute(DeleteProblemSQL)
                db.commit()
                tkinter.messagebox.showinfo(title="Delete", message="Delete successfully")
                Import()
                ShowProblem()
            except :
                db.rollback()
                tkinter.messagebox.showerror(title="Delete", message="Delete failed, database currupted!")
            finally :
                db.close()
            Import()
            ShowTest()
root['menu']=MenuBar

def ShowProblem() :
    Import()
    NewBut.config(state="active")
    EditBut.config(state="disabled")
    DeleteBut.config(state="disabled")
    AddToTestBut.config(state="disabled")
    ShowResultBut.config(state="disabled")
    SubmitRankBut.config(state="disabled")
    DescriptionText.config(state="normal")
    NewBut.config(text="New")
    SolveText.config(state="normal")
    SelectListBox.delete(0,END)
    DescriptionText.delete('0.0', END)
    SolveText.delete('0.0', END)
    DescriptionText.config(state="disabled")
    SolveText.config(state="disabled")
    for Problem in ProblemInfo :
        SelectListBox.insert(END,Problem[0])
    ProblemBut.config(state="disabled")
    TestBut.config(state="active")

def ShowTest() :
    Import()
    NewBut.config(state="active")
    EditBut.config(state="disabled")
    DeleteBut.config(state="disabled")
    AddToTestBut.config(state="disabled")
    SubmitRankBut.config(state="disabled")
    ShowResultBut.config(state="disabled")
    DescriptionText.config(state="normal")
    SolveText.config(state="normal")
    NewBut.config(text="Create")
    DescriptionText.delete('0.0', END)
    SolveText.delete('0.0', END)
    SelectListBox.delete(0, END)
    for Test in TestInfo :
        SelectListBox.insert(END,Test[0])
    DescriptionText.config(state="disabled")
    SolveText.config(state="disabled")
    ProblemBut.config(state="active")
    TestBut.config(state="disabled")

ProblemBut = tkinter.Button(root,font=('微软雅黑', 13),width=8,text='Problems',state='disabled',command=ShowProblem)
ProblemBut.place(x=0,y=0)
TestBut = tkinter.Button(root,font=('微软雅黑', 13),width=8,text='Tests',state='disabled',command=ShowTest)
TestBut.place(x=90,y=0)

def ShowStars() :
    NowX = 410
    Score = round(ProblemInfo[NowIndex][3])
    RankedPeople = ProblemInfo[NowIndex][4]
    RankString = tkinter.StringVar()
    RankResLab = tkinter.Label(root, font=('微软雅黑', 10, "italic"), textvariable=RankString)
    RankResLab.place(x=407, y=730)
    if RankedPeople == 0:
        RankString.set("(no rank score yet)")
        for i in range(0, 5):
            DarkImageList[i].place(x=NowX, y=707)
            NowX = NowX + 20
            ShineImageList[i].place(x=10086, y=10086)
        NowX = 410
    else:
        RankString.set("(%.1f point out of 5)" % ProblemInfo[NowIndex][3])
        if Score == 0:
            for i in range(0, 5):
                DarkImageList[i].place(x=NowX, y=707)
                NowX = NowX + 20
                ShineImageList[i].place(x=10086, y=10086)
        else:
            NowX = 410
            for i in range(0, Score):
                ShineImageList[i].place(x=NowX, y=707)
                NowX = NowX + 20
                DarkImageList[i].place(x=10086, y=10086)
            for i in range(Score, 5):
                DarkImageList[i].place(x=NowX, y=707)
                NowX = NowX + 20
                ShineImageList[i].place(x=10086, y=10086)
            NowX = 410
    RankedPeopleStr = tkinter.StringVar()
    RankedPeopleLab = tkinter.Label(root, font=('微软雅黑', 10, "italic"), textvariable=RankedPeopleStr)
    RankedPeopleLab.place(x=530, y=704)
    RankedPeopleStr.set("Ranked by %d people" % RankedPeople)

def CheckSelection(event) :
    for index in range(0,SelectListBox.size()) :
        if SelectListBox.selection_includes(index)==True :
            ShowResultBut.config(state="active")
            if TestBut['state'] == "active" and ProblemBut['state'] =='disabled' :
                SubmitRankBut.config(state = 'active')
                if Flag == "Admin":
                    DeleteBut.config(state="active")
                    EditBut.config(state="active")
                    NewBut.config(state="active")
                    AddToTestBut.config(state="active")
                global NowIndex
                NowIndex = index
                if ProblemInfo[NowIndex][6] in InTest :
                    InTestStr.set("Remove")
                else :
                    InTestStr.set("Add")
                if UserRanked[index] == -1 :
                    SubmitRankBut.config(state="active")
                    YourRankStr.set("Your rank :")
                else :
                    SubmitRankBut.config(state="disabled")
                    YourRankStr.set("Your rank : "+str(UserRanked[index]))
                DescriptionText.config(state="normal")
                SolveText.config(state="normal")
                DescriptionText.delete('0.0',END)
                SolveText.delete('0.0',END)
                #Check zip existance
                NowZip = zipfile.ZipFile(ProblemInfo[index][1])
                NowZip.extractall(os.getcwd()+"\\Tempfile")
                global Description,Solve
                Description = NowZip.read("Description.txt").decode('utf-8')
                #Solve = NowZip.read("Solve.txt").decode('utf-8')
                DescriptionText.insert(END,"(UID: %d, Author : %s, Point: %d)\n"%(ProblemInfo[index][6],ProblemInfo[index][5],ProblemInfo[index][2]))
                DescriptionText.insert(END,Description)
                if len(NowZip.namelist()) == 3:
                    global DescriptionImage
                    DescriptionText.insert(END,"\nPhoto for this problem:\n")
                    DescriptionImage = ImageTk.PhotoImage(file=os.getcwd() + '\\Tempfile\\Photo.gif')
                    DescriptionText.image_create(END,image=DescriptionImage)
                    def ShowOrigin() :
                        os.system('"%s"' % (os.getcwd() + "\\Tempfile\\Photo.gif"))
                    ShowOriginBut = tkinter.Button(DescriptionText,text='Show Origin Photo',width=20,command=ShowOrigin)
                    DescriptionText.insert(END, "\n\n")
                    DescriptionText.window_create(END,window=ShowOriginBut)
                #SolveText.insert(END,Solve)
                DescriptionText.config(state="disabled")
                SolveText.config(state="disabled")
                ShowStars()
                NowZip.close()
                return
            elif TestBut['state'] == "disabled" and ProblemBut['state'] =='active' :
                if Flag == "Admin":
                    DeleteBut.config(state="active")
                    NewBut.config(state="active")
                NowTest = TestInfo[index]
                NowIndex=index
                AllProblem = NowTest[1].split(',')
                del AllProblem[-1]
                DescriptionText.config(state="normal")
                SolveText.config(state="normal")
                DescriptionText.delete('0.0', END)
                SolveText.delete('0.0', END)
                Count = 0
                UpdateBadProblem = False
                for UIDNum in AllProblem :
                    ProblemExistFlag = False
                    Count = Count + 1
                    for problem in ProblemInfo :
                        if int(UIDNum)==problem[6] :
                            ProblemExistFlag = True
                            NowZip = zipfile.ZipFile(problem[1])
                            NowZip.extractall(os.getcwd() + "\\Tempfile")
                            Description = NowZip.read("Description.txt").decode('utf-8')
                            #Solve = NowZip.read("Solve.txt").decode('utf-8')
                            DescriptionText.insert(END,str(Count)+".")
                            DescriptionText.insert(END,"%s(UID: %d, Author : %s, Point: %d)\n"%(problem[0],problem[6],problem[5],problem[2]))
                            DescriptionText.insert(END,Description)
                            if len(NowZip.namelist()) == 3:
                                global DescriptionImage1
                                DescriptionText.insert(END,"\nPhoto for this problem:\n")
                                DescriptionImage1.append(ImageTk.PhotoImage(file=os.getcwd() + '\\Tempfile\\Photo.gif'))
                                DescriptionText.image_create(END,image=DescriptionImage1[-1])
                            DescriptionText.insert(END,"\n\n")
                            #SolveText.insert(END,str(Count)+".")
                            #SolveText.insert(END, Solve)
                            #SolveText.insert(END,"\n\n")
                            NowZip.close()
                            break
                    if ProblemExistFlag == False :
                        tkinter.messagebox.showwarning(title="Warning",message="Problem(UID=%d) no longer exist, problem removed" % (int(UIDNum)))
                        AllProblem.remove(UIDNum)
                        UpdateBadProblem = True
                DescriptionText.config(state="disabled")
                SolveText.config(state="disabled")
                if UpdateBadProblem == True :
                    NewStr=""
                    TotalProblemNum=0
                    TotalPoint=0
                    for UIDNum in AllProblem :
                        NewStr = NewStr + UIDNum + ","
                        TotalProblemNum = TotalProblemNum + 1
                        for problem in ProblemInfo :
                            if int(UIDNum)==problem[6] :
                                TotalPoint = TotalPoint + problem[2]
                                break
                    print(NewStr)
                    db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
                    cursor = db.cursor()
                    UPDATESQL = """UPDATE test SET ProblemSet='%s',ProblemNumber=%d,TotalPoint=%d WHERE UID=%d""" % (NewStr,TotalProblemNum,TotalPoint,TestInfo[NowIndex][5])
                    try :
                        cursor.execute(UPDATESQL)
                        db.commit()
                    except :
                        tkinter.messagebox.showwarning(title='Warning', message='Database Corrupted！Program shutdown')
                        db.rollback()
                    finally :
                        db.close()
                    Import()
            break
def ShowSolution() :
    ShowResultBut.config(state = "disabled")
    SolveText.config(state='normal')
    if TestBut['state'] == "active" and ProblemBut['state'] == 'disabled':
        Solve = str( open(os.getcwd() + "\\Tempfile\\Solve.txt").read() )
        print(Solve)
        SolveText.insert(END, Solve)
    elif TestBut['state'] == "disabled" and ProblemBut['state'] == 'active':
        NowTest = TestInfo[NowIndex]
        AllProblem = NowTest[1].split(',')
        del AllProblem[-1]
        SolveText.delete('0.0', END)
        Count = 0
        for UIDNum in AllProblem:
            Count = Count + 1
            for problem in ProblemInfo:
                if int(UIDNum) == problem[6]:
                    NowZip = zipfile.ZipFile(problem[1])
                    NowZip.extractall(os.getcwd() + "\\Tempfile")
                    Solve = NowZip.read("Solve.txt").decode('utf-8')
                    SolveText.insert(END, str(Count) + ".")
                    SolveText.insert(END, Solve)
                    SolveText.insert(END, "\n\n")
                    NowZip.close()
                    break
    SolveText.config(state="disabled")


LeftScroll = tkinter.Scrollbar(root)
SelectListBox = tkinter.Listbox(root,selectmode = BROWSE,yscrollcommand=LeftScroll.set)
SelectListBox.config(width=30,height=30,font= ('微软雅黑',13))
LeftScroll.config(command=SelectListBox.yview)
SelectListBox.place(x=0,y=40)
LeftScroll.place(x=303,y=40,height=725,width=20)
SelectListBox.bind("<ButtonRelease-1>",CheckSelection)

DescriptionLab = tkinter.Label(root,font= ('微软雅黑',15),text='Description:')
DescriptionLab.place(x=345,y=27)
DescriptionText = scrolledtext.ScrolledText(root,font= ('微软雅黑',13),width=60,height=15,wrap=tkinter.WORD,state='disabled')
DescriptionText.place(x=350,y=60)


DeleteBut = tkinter.Button(root,text="Delete",font= ('微软雅黑',13),width=6,state="disabled",command=DeleteCommand)
DeleteBut.place(x=880,y=15)
EditBut = tkinter.Button(root,text="Edit",font= ('微软雅黑',13),width=6,state="disabled",command=EditCommand)
EditBut.place(x=800,y=15)
NewBut = tkinter.Button(root,text="New",font= ('微软雅黑',13),width=6,state="disabled",command=NewCommand)
NewBut.place(x=720,y=15)

def Switch() :
    if InTestStr.get()=="Add" :
        InTestStr.set("Remove")
        InTest.append(ProblemInfo[NowIndex][6])
    else :
        InTestStr.set("Add")
        InTest.remove(ProblemInfo[NowIndex][6])


InTestStr = tkinter.StringVar()
InTestStr.set("Add")
AddToTestBut = tkinter.Button(root,textvariable=InTestStr,font= ('微软雅黑',13),width=6,state="disabled",command=Switch)
AddToTestBut.place(x=640,y=15)
ShowResultBut = tkinter.Button(root,text = "Show solution",font = ('微软雅黑',13),width=13,state="disabled",command=ShowSolution)
ShowResultBut.place(x=430,y=410)

RankLab = tkinter.Label(root,font= ('微软雅黑',15),text='Rank:')
RankLab.place(x=345,y=700)
LoadShineStarImage = ImageTk.Image.open(os.getcwd()+"\\Resources\\star_onmouseover.png")
LoadDarkStarImage = ImageTk.Image.open(os.getcwd()+"\\Resources\\star_hollow_hover.png")
ShineStarImage = ImageTk.PhotoImage(LoadShineStarImage)
DarkStarImage = ImageTk.PhotoImage(LoadDarkStarImage)
ShineImageList = []
DarkImageList = []
for i in range(0,5) :
    ShineImageList.append(tkinter.Label(root,image=ShineStarImage))
    DarkImageList.append(tkinter.Label(root,image=DarkStarImage))
YourRankStr = tkinter.StringVar()
YourRankStr.set("Your rank :")
YourRankLab = tkinter.Label(root,textvariable=YourRankStr,font= ('微软雅黑',13))
YourRankLab.place(x=730,y=690)
v=tkinter.IntVar()
RankScale = tkinter.Scale(root,from_=0,to=5,orient=HORIZONTAL,resolution=1,tickinterval=1,length=200,variable=v)
RankScale.place(x=730,y=725)
def SubmitRank() :
    if tkinter.messagebox.askyesno(title="Submit?",message="Submit score?") :
        SubmitRankBut.config(state="disabled")
        global NowIndex
        UserRanked[NowIndex] = v.get()
        YourRankStr.set(YourRankStr.get()+str(v.get()))

        print("Your score is "+str(v.get()))
        NowRankedPeople = ProblemInfo[NowIndex][4]+1
        NowScore = (ProblemInfo[NowIndex][3]*ProblemInfo[NowIndex][4]+v.get())/NowRankedPeople
        UPDATEScoreSQL = """UPDATE problem SET TotalRank=%f, TotalRankedPeople=%d WHERE UID=%d""" % (NowScore,NowRankedPeople,ProblemInfo[NowIndex][6])
        db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
        cursor = db.cursor()
        try :
            cursor.execute(UPDATEScoreSQL)
            db.commit()
            tkinter.messagebox.showinfo(title="Submit",message="Rank successfully")
        except :
            db.rollback()
            tkinter.messagebox.showwarning(title='Warning', message='Database Corrupted！Program shutdown')
        db.close()
        Import()
        ShowStars()
    else :
        return
SubmitRankBut = tkinter.Button(root,text="Submit",font= ('微软雅黑',13),state="disabled",height=1,command=SubmitRank)
SubmitRankBut.place(x=860,y=685)

SolveLab = tkinter.Label(root,font= ('微软雅黑',15),text='Solve:')
SolveLab.place(x=345,y=410)
SolveText = scrolledtext.ScrolledText(root,font= ('微软雅黑',13),width=60,height=10,wrap=tkinter.WORD,state='disabled')
SolveText.place(x=350,y=450)


if __name__ == '__main__':
    if os.path.exists(os.getcwd()+"\\Tempfile\\Admin")==True :
        Flag = "Admin"
        File = open(os.getcwd()+"\\Tempfile\\Admin","r")
        NowUser = File.read()
        File.close()
        root.mainloop()
        #os.remove(os.getcwd()+"\\Tempfile\\Admin")
    elif os.path.exists(os.getcwd()+"\\Tempfile\\User")==True :
        Flag = "User"
        File = open(os.getcwd()+"\\Tempfile\\Admin","r")
        NowUser = File.read()
        root.mainloop()
        File.close()
        #os.remove(os.getcwd() + "\\Tempfile\\User")
    else :
        tkinter.messagebox.showerror(title="Error", message="Illegal Run!")
    if os.path.exists(os.getcwd() + "\\Tempfile\\Description.txt"):
        os.remove(os.getcwd() + "\\Tempfile\\Description.txt")
    if os.path.exists(os.getcwd() + "\\Tempfile\\Solve.txt"):
        os.remove(os.getcwd() + "\\Tempfile\\Solve.txt")
    if os.path.exists(os.getcwd() + "\\Tempfile\\Photo.gif"):
        os.remove(os.getcwd() + "\\Tempfile\\Photo.gif")