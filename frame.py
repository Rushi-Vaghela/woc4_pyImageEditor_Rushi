from tkinter import *
from PIL import ImageTk,Image

root = Tk()
root.title('Learn to code here')


frame = LabelFrame(root, padx=50, pady=50)
frame.pack(padx=10,pady=10)

b = Button(frame, text="Don't click here")
b2 = Button(frame, text="... or here")
b.grid(row=0, column=0)
b2.grid(row=1, column=1)

root.mainloop()