import tkinter
import tkinter.messagebox
import os
import hashlib
import time
import string

def md5lize(str) :
    md5sub = hashlib.md5()
    md5sub.update(str.encode(encoding='utf-8'))
    return md5sub.hexdigest()


def MasterCodeCheck() :
    root = tkinter.Tk()
    root.title('User Management')
    root.geometry('500x250')
    root.resizable(0,0)

    info_lab = tkinter.Label(root,font=("微软雅黑",13),text="Enter master code first :")
    info_lab.place(x=50,y=50)
    master_ent = tkinter.Entry(root,width=40,show='*')
    master_ent.place(x=50,y=100)

    notice_str = tkinter.StringVar()
    notice_str.set('Please enter master code')
    notice_lab = tkinter.Label(root,font=("微软雅黑",13),textvariable=notice_str)
    notice_lab.place(x=45,y=130)

    def check1(event):
        Entered = master_ent.get()
        if md5lize(Entered) == master:
            notice_str.set('Check Successfully')
            notice_lab.config(fg='green')
            root.update()
            time.sleep(1)
            # Enter Main UserEdit UI....
            root.destroy()
            time.sleep(1)
            global Flag
            Flag = True
        else:
            if notice_str.get().split()[0] != 'Wrong':
                notice_str.set('Wrong Master Code')
            else:
                notice_str.set(notice_str.get() + '! ')
            notice_lab.config(fg='red')
    def check():
        Entered = master_ent.get()
        if md5lize(Entered) == master:
            notice_str.set('Check Successfully')
            notice_lab.config(fg='green')
            root.update()
            time.sleep(1)
            # Enter Main UserEdit UI....
            root.destroy()
            time.sleep(1)
            global Flag
            Flag = True
        else:
            if notice_str.get().split()[0] != 'Wrong':
                notice_str.set('Wrong Master Code')
            else:
                notice_str.set(notice_str.get() + '! ')
            notice_lab.config(fg='red')
    check_but = tkinter.Button(root,font=("微软雅黑",13),text="Check",height=1,command=check)
    check_but.place(x=350,y=90)
    root.bind("<Return>",check1)
    root.mainloop()

if __name__ == '__main__':
    Flag = False
    CurrentPath = os.getcwd()
    print(CurrentPath)
    if os.path.exists(CurrentPath+"\\firstrun")==False :
        tkinter.messagebox.showwarning(title='Warning',message="Please run firstrun Initialization first.")
    else :
        File = open(CurrentPath+"\\firstrun",'r')
        master = File.readline()
        File.close()
        MasterCodeCheck()
        if Flag==True :
            NewVerify = open(CurrentPath+"\\Tempfile\\MasterLogin","w")
            NewVerify.write(md5lize(master))
            NewVerify.close()
            os.system("""python "%s" """% (CurrentPath+"\\Main UserEdit.py"))
