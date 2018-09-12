import tkinter
from  tkinter import simpledialog
from  tkinter import *
import tkinter.messagebox
import os
import hashlib
import pymysql

def md5lize(str) :
    md5sub = hashlib.md5()
    md5sub.update(str.encode(encoding='utf-8'))
    return md5sub.hexdigest()

def ShowAbout() :
    tkinter.messagebox.showinfo(title='About',message='You can edit Username and Password here')

def Import(showsuc=1) :
    UserInfoListBox.place(x=3,y=40)
    global Imported
    global EditBut,DeleteBut
    DeleteBut.config(state='disabled')
    EditBut.config(state='disabled')
    Imported = True
    UserInfoListBox.delete(0,END)
    for row in read_data():
        Authority = ''
        if row[3] == 1:
            Authority = 'Administrator'
        else:
            Authority = 'User              '
        Username = row[2]
        while len(Username) < 25:
            Username += ' '
        UserInfoListBox.insert(END, Username + Authority + '   ' + str(row[4]) + '       ' + row[1])
    if showsuc==1 :
        tkinter.messagebox.showinfo(title='Import', message='Import Successfully')

def Quit():
    ueroot.quit()

Imported = False
ueroot = tkinter.Tk()
ueroot.title('User Management')
ueroot.geometry('720x768')
ueroot.resizable(0,0)

MenuBar =tkinter.Menu(ueroot)
FileMenu = tkinter.Menu(MenuBar)
MenuBar.add_cascade(label='File',menu=FileMenu)
FileMenu.add_command(label='Import',command = Import)
FileMenu.add_command(label='Exit',command = Quit)
MenuBar.add_command(label='About', command=ShowAbout)
ueroot['menu']=MenuBar

UserInfoListBox = tkinter.Listbox(ueroot,selectmode = BROWSE)
UserInfoListBox.config(width=70,height=20,font= ('微软雅黑',13))

def read_data () :
    try :
        db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
    except :
        tkinter.messagebox.showwarning(title='Warning', message='Database Corrupted！Program shutdown')
        ueroot.quit()
    cursor = db.cursor()
    findSQL = "SELECT * FROM userlist"
    try :
        cursor.execute(findSQL)
        result = cursor.fetchall()
        return result
    except :
        tkinter.messagebox.showwarning(title='Warning', message='Database Corrupted！')
    db.close()


UsernameLab = tkinter.Label(ueroot,font=('微软雅黑',13),text='Username        |')
UsernameLab.place(x=0,y=10)
AuthorityLab = tkinter.Label(ueroot, font=('微软雅黑', 13), text='Authority         |')
AuthorityLab.place(x=145,y=10)
UIDLab = tkinter.Label(ueroot, font=('微软雅黑', 13), text='UID |')
UIDLab.place(x=273,y=10)
MD5Lab = tkinter.Label(ueroot, font=('微软雅黑', 13), text='Password MD5                                                    |')
MD5Lab.place(x=320,y=10)

NewUserLab = tkinter.Label(ueroot, font=('微软雅黑', 13), text='New Username:')
NewUserLab.place(x=0,y=560)
NewPasswordLab = tkinter.Label(ueroot, font=('微软雅黑', 13), text='New Password :')
NewPasswordLab.place(x=0,y=590)
NewPasswdConfirmLab = tkinter.Label(ueroot, font=('微软雅黑', 13), text='Confirm Password:')
NewPasswdConfirmLab.place(x=0,y=620)

def NewUser() :
    if Imported==False :
        tkinter.messagebox.showwarning(title='Warning', message='IMPORT User data FIRST')
    else :
        Username = NewUserEnt.get()
        for word in Username :
            if not ((ord(word)>=48 and ord(word)<=57) or (ord(word)>=65 and ord(word)<=90) or (ord(word)>=97 and ord(word)<=122)) :
                Username_str.set('Invalid Username')
                UsernameNot_lab.config(fg='red')
                return
        for Existrow in read_data() :
            if Username==Existrow[2] :
                Username_str.set('Username exist')
                UsernameNot_lab.config(fg='red')
                return
        Username_str.set('Username Available')
        UsernameNot_lab.config(fg='green')
        Password = NewPasswordEnt.get()
        if len(Password)<=5 :
            Password_str.set('Password too short(len>=6)')
            PasswordNot_lab.config(fg='red')
            return
        Password_str.set('Password Available')
        PasswordNot_lab.config(fg='green')
        PasswordConfirm = NewPasswdConfirmEnt.get()
        if PasswordConfirm!=Password :
            PasswordConfirm_str.set('Password not match')
            PasswordConfirm_lab.config(fg='red')
            return
        PasswordConfirm_str.set('Password match')
        PasswordConfirm_lab.config(fg='green')
        global flag
        if flag.get()==1 :
            Authority='Admin'
        else :
            Authority='User'
        if tkinter.messagebox.askyesno('Create','Create New User?\nUsername:'+Username+'\nPassword:'+Password+'\nAuthority:'+Authority) :
            #Upload to MySQL DB
            INSERTsql = """INSERT INTO userlist(UsernameMD5,PasswordMD5,UsernameVig,Authority)
                     VALUES('%s','%s','%s',%d)""" % (md5lize(Username),md5lize(Password),Username,flag.get())
            try:
                db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
            except:
                tkinter.messagebox.showwarning(title='Warning', message='Database Corrupted！Program shutdown')
                ueroot.quit()
            cursor = db.cursor()
            try:
                cursor.execute(INSERTsql)
                db.commit()
            except:
                print('Create Failed')
                db.rollback()
            db.close()
            Import(0)

NewUserEnt =tkinter.Entry(ueroot,font=('微软雅黑', 13),width=20)
NewUserEnt.place(x=160,y=560)
NewPasswordEnt = tkinter.Entry(ueroot,font=('微软雅黑', 13),width=20,show='*')
NewPasswordEnt.place(x=160,y=590)
NewPasswdConfirmEnt =tkinter.Entry(ueroot,font=('微软雅黑', 13),width=20,show='*')
NewPasswdConfirmEnt.place(x=160,y=620)
NewBut = tkinter.Button(ueroot,font=('微软雅黑', 13),text='   New   ',command = NewUser)
NewBut.place(x=200,y=660)

Username_str = tkinter.StringVar()
Username_str.set('')
UsernameNot_lab = tkinter.Label(ueroot,font=("微软雅黑",13),textvariable=Username_str)
UsernameNot_lab.place(x=370,y=560)
Password_str = tkinter.StringVar()
Password_str.set('')
PasswordNot_lab = tkinter.Label(ueroot,font=("微软雅黑",13),textvariable=Password_str)
PasswordNot_lab.place(x=370,y=590)
PasswordConfirm_str = tkinter.StringVar()
PasswordConfirm_str.set('')
PasswordConfirm_lab = tkinter.Label(ueroot,font=("微软雅黑",13),textvariable=PasswordConfirm_str)
PasswordConfirm_lab.place(x=370,y=620)


flag=IntVar()
AdminCheck = tkinter.Radiobutton(ueroot,text='Admin',variable=flag,value=1)
UserCheck = tkinter.Radiobutton(ueroot,text='User',variable=flag,value=0)
AdminCheck.place(x=20,y=665)
UserCheck.place(x=100,y=665)


def DeleteSelected() :
    if tkinter.messagebox.askyesno(title='Delete',message="Are you sure wangt to DELETE "+read_data()[now][2]+"? (UID="+str(read_data()[now][4])+")") :
        db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
        cursor = db.cursor()
        DeleteSQL='''DELETE FROM userlist WHERE UID=%d''' % read_data()[now][4]
        try :
            cursor.execute(DeleteSQL)
            db.commit()
            Import(0)
            tkinter.messagebox.showinfo(title='Notice',message='Delete Successfully.')
        except :
            db.rollback()
            tkinter.messagebox.showwarning(title='Warning',message='Delete FAILED,Contact Developer')
        db.close()

def CheckSelection(event) :
    global  EditBut,DeleteBut
    for index in range(0,UserInfoListBox.size()) :
        if UserInfoListBox.selection_includes(index)==True :
            EditBut.config(state="active")
            DeleteBut.config(state="active")
            global now
            now=index
            return


def EditPasswd() :
    NewPasswd = simpledialog.askstring('New Password','Enter new Password')
    if NewPasswd is None :
        return
    if len(NewPasswd) <= 5:
        tkinter.messagebox.showwarning(title='Warning',message='Password length must >=6')
    else :
        UPDATEpwsql = '''UPDATE userlist set PasswordMD5='%s' WHERE UID=%d''' % (md5lize(NewPasswd),read_data()[now][4])
        try:
            db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
        except:
            tkinter.messagebox.showwarning(title='Warning', message='Database Corrupted！Program shutdown')
            ueroot.quit()
        cursor = db.cursor()
        try :
            cursor.execute(UPDATEpwsql)
            db.commit()
            Import(0)
            tkinter.messagebox.showinfo(title='Notice',message='Edit Successfully.')
        except :
            db.rollback()
            tkinter.messagebox.showwarning(title='Warning',message='Edit FAILED,Contact Developer')
        db.close()
EditBut = tkinter.Button(ueroot,font=('微软雅黑', 13),width=7,text='   Edit*  ',state='disabled',command = EditPasswd)
EditBut.place(x=620,y=560)
DeleteBut = tkinter.Button(ueroot,font=('微软雅黑', 13),width=7,text=' Delete ',state='disabled',command = DeleteSelected)
DeleteBut.place(x=620,y=610)
now=0
UserInfoListBox.bind("<ButtonRelease-1>",CheckSelection)

if __name__ == '__main__':
    if os.path.exists(os.getcwd()+"\\Tempfile\\MasterLogin")==True :
        File = open(os.getcwd()+"\\Tempfile\\MasterLogin",'r')
        Master = open(os.getcwd()+"\\firstrun","r")
        Check = md5lize(Master.readline())
        Master.close()
        if File.readline() == Check :
            File.close()
            ueroot.mainloop()
            os.remove(os.getcwd()+"\\Tempfile\\MasterLogin")
        else :
            tkinter.messagebox.showerror(title="Error",message="Illegal Login!")
    else :
        tkinter.messagebox.showerror(title="Error",message="Illegal Login!")