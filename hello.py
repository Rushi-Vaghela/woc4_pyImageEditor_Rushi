from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text="Look! I ckicked a button")
    myLabel.pack()

myButton = Button(root, text="Click me!", command=myClick, fg="blue", bg="yellow")
myButton.pack()

root.mainloop()