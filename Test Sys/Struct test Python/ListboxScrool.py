from tkinter import *

root=Tk()
v=StringVar()
#Listbox与变量绑定'
lb1=Listbox(root,listvariable=v)
v.set(('10','20','30','40','50'))
print(v.get())
lb1.pack()

#.创建一个可以多选的Listbox,使用属性selectmaod'
lb2=Listbox(root,selectmode=MULTIPLE)
for item in range(10):
    lb2.insert(END,str(item))
#  有两个特殊的值ACTIVE和END，ACTIVE是向当前选中的item前插入一个
# （即使用当前选中的索引作为插入位置）；END是向
#  Listbox的最后一项添加插入一项

lb2.delete(1,3)
#删除全部内容,使用delete指定第一个索引值0和最后一个参数END，即可
lb2.pack()

#这个属性selectmode还可以设置为BROWSE,可以通过鼠标来移动Listbox中的选中位置
# （不是移动item），
#这个属性也是Listbox在默认设置的值，这个程序与1.程序运行的结果的一样的
scrollbar=Scrollbar(root)
scrollbar.pack(side=RIGHT,fill=Y)
lb3=Listbox(root,selectmode=BROWSE,yscrollcommand=scrollbar.set)
for item in range(20):
    lb3.insert(END,str(item))
    lb3.pack(side=LEFT,fill=BOTH)
scrollbar.config(command=lb3.yview)

#将一个垂直方向的Scrollbar和listboxs/canvases/text fields这些控件结合起来，
# 你只需要按照下面的步骤即可：
#1.将这些控件的yscrollcommand选项设置为scrollbar的set方法。
#2.将scrollbar的command选项设置为这些控件的yview方法。

print(lb3.size())
print(lb3.get(3))
print(lb3.get(3,7))
lb3.selection_set(0,10)
lb3.selection_clear(0,3)
lb3.pack()


def printlist(event):
    print(lb4.get(lb4.curselection()))


#使用selectmode  = EXPANDED使用Listbox来支持Shift和Control
lb4=Listbox(root,selectmode=EXTENDED)
lb4.bind('<Double-Button-1>',printlist)
for item in ['python','tkinter','widget']:
    lb4.insert(END,item)
lb4.pack()


root.mainloop()