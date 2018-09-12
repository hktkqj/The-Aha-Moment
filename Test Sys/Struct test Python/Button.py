import tkinter as tk
from PIL import Image, ImageTk

global attackTime
attackTime = 1


def show1():
    top1 = tk.Toplevel()
    image = Image.open('random.jpg')
    img = ImageTk.PhotoImage(image)
    canvas1 = tk.Canvas(top1, width=image.width * 2, height=image.height * 2, bg='white')
    canvas1.create_image(0, 0, image=img, anchor="nw")
    canvas1.create_image(image.width, 0, image=img, anchor="nw")
    canvas1.pack()
    top1.mainloop()


def show2():
    top1 = tk.Toplevel()
    image = Image.open('random.jpg')
    img = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(top1, width=image.width, height=image.height, bg='white')
    canvas.create_image(0, 0, image=img, anchor="nw")
    canvas.pack()
    top1.mainloop()


def showMessage():
    top = tk.Toplevel()
    l = tk.Label(top, text='Attacks cost ' + str(attackTime) + ' s', width=20)
    l.pack()
    top.mainloop()


root = tk.Tk()
b1 = tk.Button(root, text='start1', command=show1)
b1.pack()
b2 = tk.Button(root, text='start2', command=showMessage)
b2.pack()
root.mainloop()