'''
Tkinter之Listbox篇
# Listbox为列表框控件，它可以包含一个或多个文本项(text item)，可以设置为单选或多选
'''


#_*_coding:utf-8_*_
import tkinter as tk
from tkinter import *


if __name__ == '__main__':
    root = tk.Tk()
    root.wm_title('Listbox')
    root.geometry("1800x800+120+100")         #设置窗口大小  并初始化桌面位置
    root.resizable(width = True,height = True)  #宽不可变 高可变  默认True

    #1、创建一个Listbox，向其中添加三个item
    fram = Frame(root)
    lb = Listbox(fram)
    for i in ['python','Tkinter','Listbox']:
        lb.insert(END,i)
    lb.pack(side = LEFT)

    fram.pack(side = TOP)



    #2、创建一个可以多选的Listbox,使用属性selectmode
    # 属性MULTIPLE允许多选，每次点击item，它将改变自己的当前选状态，与Checkbox有点相似
    fram1 = Frame(root)
    # 依次点击这三个item，均显示为选中状态。
    lb = Listbox(fram1,selectmode = MULTIPLE)
    for i in ['python','Tkinter','Listbox']:
        lb.insert(END,i)
    lb.pack(side = LEFT)

    fram1.pack(side = TOP)


    #3、这个属性selectmode还可以设置为BROWSE,可以通过鼠标来移动Listbox中的选中位置（不是移动item）
    # 这个属性也是Listbox在默认设置的值，这个程序与1.程序运行的结果的一样的。
    fram2 = Frame(root)
    # 依次点击这三个item，均显示为选中状态。
    lb = Listbox(fram2,selectmode = BROWSE)
    for i in ['python1','Tkinter1','Listbox1']:
        lb.insert(END,i)
    lb.pack(side = LEFT)

    #使用鼠标进行拖动，可以看到选中的位置随之变化。
    # 与BROWSE相似 的为SINGLE，但不支持鼠标移动选中位置。
    lb1 = Listbox(fram2,selectmode = SINGLE)
    for i in ['python2','Tkinter2','Listbox2']:
        lb1.insert(END,i)
    lb1.pack(side = LEFT)

    #4、使用selectmode  = EXTENDED使用Listbox来支持Shift和Control。
    #运行程序，点中“python"，shift + 点击"widget"，会选中所有的item
    #运行程序，点中"python"，control + 点击"widget"，会选中python和widget，第二项tkinter处于非选中状态
    lb2 = Listbox(fram2,selectmode = EXTENDED)
    for i in ['python3','Tkinter3','Listbox3']:
        lb2.insert(END,i)
    lb2.pack(side = LEFT)

    fram2.pack(side = TOP)


    #5.向Listbox中添加一个item
    '''
# 以上的例子均使用了insert来向Listbox中添加 一个item，这个函数有两个属性一个为添加的索引值，另一个为添加的项(item)
# 有两个特殊的值ACTIVE和END，ACTIVE是向当前选中的item前插入一个（即使用当前选中的索引作为插入位置）；END是向Listbox的最后一项添加插入一项
# 先向Listbox中追加三个item，再在Listbox开始添加三项
'''
fram3 = Frame(root)
lb = Listbox(fram3)
for i in ['python4','Tkinter4','Listbox4']:
    lb.insert(END,i)
#添加三项，每个string为一个item
lb.insert(0,'windows','door','pen')
lb.insert(4,'windows1','door1','pen1')
lb.insert(ACTIVE,'windows','red')

#6、删除Listbox中的项，使用delete，这个函数也有两个参数，第一个为开始的索引值；第二个为结束的索引值，如果不指定则只删除第一个索引项。
# 运行程序,1-2被删除
lb.delete(0, 1)
#删除全部内容,使用delete指定第一个索引值0和最后一个参数END，即可
lb.delete(0,END)

lb.pack(side = LEFT)



#7、选中操作函数，使用函数实现。selection_set函数有两个参数第一个为开始的索引；第二个为结束的索引，如果不指定则只选中第一个参数指定的索引项
lb1 = Listbox(fram3)
for i in range(10):
    lb1.insert(END,i*10+3)

# 程序运行结果，选中了0-7。 此代码并未指定Listbox为MULTIPLE或EXTENDED，查通过selection_set仍旧可以对Listbox进行操作。
lb1.selection_set(0,7)
#与之相对的便是取消选中的函数select_clear了，参数与selection_set在参数相同，如下代码取消索引从0－3在状态
lb1.select_clear(0, 3)

#8、得到当前Listbox中的item个数
num = lb1.size()
print(num)

#9、返回指定索引的项
print(lb1.get(3))
#get也为两个参数的函数，可以返回多个项(item)，如下返回索引值3－7的值,是一个tuple类型
print(lb1.get(3,7))

#10、curselection()返回当前选中的项的索引，不是item的值
print(lb1.curselection())

#11、selection_includes(i)判断 一个项是否被选中，i使用索引
# 返回结果：True Flase，即4包含在选中的索引中，0不包含在选中的索引中
print(lb1.selection_includes(4))
print(lb1.selection_includes(0))

lb1.pack(side = LEFT)

#12、Listbox与变量绑定
v = StringVar()
# 使用listvariable属性绑定变量v
lb2 = Listbox(fram3,listvariable = v)
for i in range(10):
    lb2.insert(END,i*10+2)
print(v.get())
#改变v的值,使用tuple可以与item对应
v.set(('1000','200'))
print(v.get())   #结果只有两项了1000和200

lb2.pack(side = LEFT)


#13、Listbox与事件绑定
# 它不支持command属性来设置回调函数了，使用bind来指定回调函数,打印当前选中的值

#回调函数
def callListbox(event):
    print(lb1.curselection())

lb3 = Listbox(fram3)
for i in range(10):
    lb3.insert(END,i*10+2)

lb3.bind('<Button-1>',callListbox)
lb3.pack(side = LEFT)


fram3.pack(side = TOP)


root.mainloop()