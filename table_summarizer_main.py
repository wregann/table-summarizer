from tkinter import *

root = Tk()

myLabel1 = Label(root, text="Hello!")
myLabel2 = Label(root, text="Hello2!")

myLabel1.grid(row=5, column=5)
myLabel2.grid(row=0, column=0)
root.mainloop()