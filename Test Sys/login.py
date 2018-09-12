import tkinter
import tkinter.messagebox
import os
import hashlib
import pymysql

def md5lize(str) :
    md5sub = hashlib.md5()
    md5sub.update(str.encode(encoding='utf-8'))
    return md5sub.hexdigest()

def read_data () :
    db = pymysql.connect("localhost", 'root', 'dkstFeb.1st', 'testsys')
    cursor = db.cursor()
    findSQL = "SELECT * FROM userlist"
    try :
        cursor.execute(findSQL)
        result = cursor.fetchall()
        return result
    except :
        tkinter.messagebox.showwarning(title='Warning', message='Database Corrupted！')

def login() :
    now_username = username_ent.get()
    now_userpass = userpass_ent.get()
    NowPath = os.getcwd()
    Flag=False
    for data in read_data() :
        if md5lize(now_username)==data[0] :
            if md5lize(now_userpass) == data[1]:
                if data[3]==1 :
                    tkinter.messagebox.showinfo(title='OK', message='Login Successfully with Administrator')
                    File = open(NowPath+"\\Tempfile\\Admin","w")
                    File.write(now_username)
                    File.close()
                else :
                    tkinter.messagebox.showinfo(title='OK', message='Login Successfully with NormalUser')
                    File = open(NowPath + "\\Tempfile\\User", "w")
                    File.write(now_username)
                    File.close()
                root.destroy()
                os.system("""python \"%s\\Problem View.py\" """ % NowPath)
                Flag=True
            else :
                tkinter.messagebox.showwarning(title='Warning', message='Wrong password!')
                return False
    if Flag==False :
        tkinter.messagebox.showinfo(title='Warning', message='No such user!')
    return False

local_path=os.path.abspath('.')

root = tkinter.Tk()

root.title('Test Syetem Login')

root.geometry('500x250')

root.resizable(0,0)

title_image = tkinter.PhotoImage(file = local_path+'\Resources\\title.gif')

title_label = tkinter.Label(root,image = title_image)

title_label.place(x=120,y=30)

title_word = tkinter.Label(root,font="微软雅黑",text="Please Log in:")

title_word.place(x=200,y=35)

username_lab = tkinter.Label(root,font="微软雅黑",text="User:")
userpass_lab = tkinter.Label(root,font="微软雅黑",text="Password:")

username_lab.place(x=95,y=100)
userpass_lab.place(x=80,y=130)

username_ent =tkinter.Entry(root,font="微软雅黑",width=20 )
userpass_ent =tkinter.Entry(root,font="微软雅黑",width=20,show='*')

username_ent.place(x=180,y=100)
userpass_ent.place(x=180,y=130)


login_but = tkinter.Button(root,font="微软雅黑",text="Log in",command=login)
login_but.place(x=220,y=180)

root.mainloop()