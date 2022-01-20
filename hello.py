from tkinter import *
from webbrowser import get

root = Tk()

e =Entry(root, width=50, bg="blue", fg="white", borderwidth=5)
e.pack()
e.insert(0, "Enter your Name: ")

def myClick():
    hello = "Hello " + e.get()
    myLabel = Label(root, text = hello)
    myLabel.pack()

myButton = Button(root, text="Enter your Name", command=myClick, fg="blue", bg="yellow")
myButton.pack()

root.mainloop()