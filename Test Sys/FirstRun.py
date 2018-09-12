import tkinter
import tkinter.messagebox
import pymysql
import hashlib
import time
import os

def md5lize(str) :
    md5sub = hashlib.md5()
    md5sub.update(str.encode(encoding='utf-8'))
    return md5sub.hexdigest()

MasterCode = ''

def MasterCodeCheck() :
    root = tkinter.Tk()
    root.title('First Run')
    root.geometry('400x400')
    root.resizable(0,0)

    info_lab = tkinter.Label(root,font=("微软雅黑",13),text="Please enter a MASTER CODE:")
    info_lab.place(x=30,y=20)
    confirminfo_lab = tkinter.Label(root, font=("微软雅黑", 13), text="Please re-confirm the MASTER CODE:")
    confirminfo_lab.place(x=30, y=80)
    master_ent = tkinter.Entry(root,width=45,show='*')
    master_ent.place(x=30,y=50)
    confirmmaster_ent = tkinter.Entry(root, width=45, show='*')
    confirmmaster_ent.place(x=30, y=110)

    notice_str = tkinter.StringVar()
    notice_str.set('Please enter master code')
    notice_lab = tkinter.Label(root,font=("微软雅黑",13),textvariable=notice_str)
    notice_lab.place(x=30,y=150)

    def check():
        Entered = master_ent.get()
        ConfirmEntered = confirmmaster_ent.get()
        if len(Entered)==0 :
            return
        if len(Entered)<=9 :
            notice_str.set('Master code too short !')
            notice_lab.config(fg='red')
            return
        if Entered == ConfirmEntered:
            notice_str.set('Master code accepted.')
            notice_lab.config(fg='green')
            tkinter.messagebox.showwarning(title = "WARNING",message='IMPORTANT: PLEASE REMEMBER YOUR MASTER CODE \'%s\'' % Entered)
            global MasterCode
            MasterCode = Entered
            check_but.config(state='disabled')
            InitBut.config(state='active')
        else:
            notice_str.set('Master code doesn\'t match !')
            notice_lab.config(fg='red')

    def Initialize() :
        InitializeStr.set('Initializing......')
        InitBut.config(state='disabled')
        root.update()

        time.sleep(2)
        MySQLStr=tkinter.StringVar()
        MySQLStr.set("MySQL database build......")
        MySQLLab = tkinter.Label(root, font=("微软雅黑", 13,'italic'), textvariable=MySQLStr)
        MySQLLab.place(x=30, y=240)
        root.update()
        time.sleep(2)
        db=pymysql.connect('localhost','root','dkstFeb.1st',charset='utf8')
        cursor = db.cursor()
        try :
            cursor.execute("""DROP database IF EXISTS testsys""")
            db.commit()
            cursor.execute("""CREATE database IF NOT EXISTS testsys""")
            db.commit()
            db.close()
            db = pymysql.connect('localhost', 'root', 'dkstFeb.1st','testsys')
            cursor = db.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS `userlist`(
                                `UsernameMD5` VARCHAR(50) NOT NULL,
                                `PasswordMD5` VARCHAR(50) NOT NULL,
                                `UsernameVig` VARCHAR(50) NOT NULL,
                                `Authority` TINYINT,
                                `UID` INT UNSIGNED AUTO_INCREMENT,
                                `LastLogin` TIMESTAMP,
                                PRIMARY KEY (`UID`)
                            )  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4;""")
            db.commit()
            cursor.execute("""CREATE TABLE IF NOT EXISTS `problem` (
                                `ProblemName` VARCHAR(100) NOT NULL,
                                `ProblemDescriptionFile` VARCHAR(1024) NOT NULL,
                                `WorthPoint` INT unsigned,
                                `TotalRank` DOUBLE,
                                `TotalRankedPeople` INT unsigned,
                                `UploadPeople` VARCHAR(20) NOT NULL,
                                `UID` INT UNSIGNED AUTO_INCREMENT,
                                PRIMARY KEY (`UID`)
                            )  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4;""")
            db.commit()
            cursor.execute("""CREATE TABLE IF NOT EXISTS `test` (
                                `TestName` VARCHAR(100) NOT NULL,
                                `ProblemSet` VARCHAR(2048) NOT NULL,
                                `ProblemNumber` INT unsigned,
                                `TotalPoint` INT unsigned,
                                `CreateUser` VARCHAR(20) NOT NULL,
                                `UID` INT UNSIGNED AUTO_INCREMENT,
                                PRIMARY KEY (`UID`)
                            )  ENGINE=INNODB DEFAULT CHARSET=UTF8MB4;""")
            db.commit()
            MySQLStr.set(MySQLStr.get()+'Success')
            MySQLLab.config(fg='green')
        except :
            MySQLStr.set(MySQLStr.get() + 'Failed')
            MySQLLab.config(fg='red')
            db.rollback()
        root.update()
        time.sleep(1)

        FolderStr = tkinter.StringVar()
        FolderStr.set('Folder build......')
        FolderLab = tkinter.Label(root, font=("微软雅黑", 13, 'italic'), textvariable=FolderStr)
        FolderLab.place(x=30, y=270)
        root.update()
        time.sleep(2)
        NowPath= os.getcwd()
        if os.path.exists(NowPath+"\Tempfile")==False :
            try :
                os.mkdir(NowPath+"\Tempfile")
            except :
                FolderStr.set(FolderStr.get()+"Failed")
                MySQLLab.config(fg='red')
                root.update()
        if os.path.exists(NowPath+"\Problems")==False :
            try :
                os.mkdir(NowPath+"\Problems")
            except :
                FolderStr.set(FolderStr.get()+"Failed")
                MySQLLab.config(fg='red')
                root.update()
        FolderStr.set(FolderStr.get() + "Success")
        FolderLab.config(fg='green')
        root.update()
        time.sleep(1)
        FirstStr = tkinter.StringVar()
        FirstStr.set('Almost complete......')
        FirstLab = tkinter.Label(root, font=("微软雅黑", 13, 'italic'), textvariable=FirstStr)
        FirstLab.place(x=30, y=300)
        root.update()
        time.sleep(2)
        FirstFile = open(NowPath+"\\firstrun","w")
        global MasterCode
        MD5CODE = md5lize(MasterCode)
        FirstFile.write(MD5CODE)
        FirstFile.close()
        if os.path.exists(NowPath+"\\firstrun")==False :
            FirstStr.set(FirstStr.get()+"Failed")
            FirstLab.config(fg='red')
        else :
            FirstStr.set(FirstStr.get() + "Success")
            FirstLab.config(fg='green')
        root.update()
        time.sleep(1)
        InitializeStr.set(InitializeStr.get()+"Done.")
        DoneBut =tkinter.Button(root,font=("微软雅黑",13),text="Done",width=8,height=1,command=root.quit)
        DoneBut.place(x=290,y=295)

    check_but = tkinter.Button(root,font=("微软雅黑",13),text="Check",width=8,height=1,command=check)
    check_but.place(x=290,y=145)
    InitBut = tkinter.Button(root, font=("微软雅黑", 13), text="Initialize",width=8,height=1,state='disabled',command = Initialize)
    InitBut.place(x=290, y=195)

    InitializeStr = tkinter.StringVar()
    InitializeStr.set('')
    confirminfo_lab = tkinter.Label(root, font=("微软雅黑", 13), textvariable=InitializeStr)
    confirminfo_lab.place(x=30, y=200)

    if os.path.exists(os.getcwd()+"\\firstrun")==True :
        tkinter.messagebox.showwarning(title='Warning',message="Not firstrun, Initialization shutdown.")
    else :
        root.mainloop()

if __name__ == '__main__':
    print(md5lize("1234567890"))
    MasterCodeCheck()