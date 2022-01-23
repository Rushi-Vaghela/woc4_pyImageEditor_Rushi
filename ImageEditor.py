from cProfile import label
from tkinter import *
import os
from tkinter import messagebox
from tkinter.filedialog import FileDialog, askopenfilename, asksaveasfilename
from tkinter import Image 
import ctypes
from PIL import Image
import PIL.ImageOps
import PIL.ImageFilter
import PIL.ImageEnhance

from PIL import ImageTk
from PIL import ImageOps
FileDialog 
import imghdr
from PIL import ImageDraw
from collections import *

def crop(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.drawOn=False
   
    canvas.data.cropPopToHappen=True
    messagebox.showinfo(title="Crop", \
                          message="Draw cropping rectangle and press Enter" ,\
                          parent=canvas.data.mainWindow)
    if canvas.data.image!=None:
        canvas.data.mainWindow.bind("<ButtonPress-1>", \
                                    lambda event: startCrop(event, canvas))
        canvas.data.mainWindow.bind("<B1-Motion>",\
                                    lambda event: drawCrop(event, canvas))
        canvas.data.mainWindow.bind("<ButtonRelease-1>", \
                                    lambda event: endCrop(event, canvas))

def startCrop(event, canvas):
    
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.startCropX=event.x
        canvas.data.startCropY=event.y

def drawCrop(event,canvas):
    
    if canvas.data.endCrop==False and canvas.data.cropPopToHappen==True:
        canvas.data.tempCropX=event.x
        canvas.data.tempCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                 canvas.data.tempCropX, \
            canvas.data.tempCropY, fill="gray", stipple="gray12", width=0)

def endCrop(event, canvas):
    
    if canvas.data.cropPopToHappen==True:
        canvas.data.endCrop=True
        canvas.data.endCropX=event.x
        canvas.data.endCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX, \
                                canvas.data.startCropY,
                                 canvas.data.endCropX, \
            canvas.data.endCropY, fill="gray", stipple="gray12", width=0 )
        canvas.data.mainWindow.bind("<Return>", \
                                lambda event: performCrop(event, canvas))

def performCrop(event,canvas):
    canvas.data.image=\
    canvas.data.image.crop(\
    (int(round((canvas.data.startCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.startCropY-canvas.data.imageTopY)*canvas.data.imageScale)),
    int(round((canvas.data.endCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.endCropY-canvas.data.imageTopY)*canvas.data.imageScale))))
    canvas.data.endCrop=False
    canvas.data.cropPopToHappen=False
    save(canvas)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

def reset(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.originalImage.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def mirror(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.mirror(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def flip(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.flip(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)


def transpose(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    
    if canvas.data.image!=None:
        imageData=list(canvas.data.image.getdata())
        newData=[]
        newimg=Image.new(canvas.data.image.mode,\
                (canvas.data.image.size[1], canvas.data.image.size[0]))
        for i in range(canvas.data.image.size[0]):
            addrow=[]
            for j in range(i, len(imageData), canvas.data.image.size[0]):
                addrow.append(imageData[j])
            addrow.reverse()
            newData+=addrow 
        newimg.putdata(newData)
        canvas.data.image=newimg.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

############### FILTERS ######################
        
def covertGray(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    
    if canvas.data.image!=None:
        data=[]
        for col in range(canvas.data.image.size[1]):
            for row in range(canvas.data.image.size[0]):
                #print(canvas.data.image.getpixel((row, col)))[0:3]
                r, g, b= canvas.data.image.getpixel((row, col))[0:3]
                avg= int(round((r + g + b)/3.0))
                R, G, B= avg, avg, avg
                data.append((R, G, B))
        canvas.data.image.putdata(data)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def invert(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    if canvas.data.image!=None:
        print(PIL.ImageOps.invert(canvas.data.image))
        canvas.data.image=PIL.ImageOps.invert(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

def sepia(canvas):
    canvas.data.colourPopToHappen= False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False

    if canvas.data.image!=None:
        sepiaData=[]
        for col in range(canvas.data.image.size[1]):
            for row in range(canvas.data.image.size[0]):
                r, g, b = canvas.data.image.getpixel((row,col))[0:3]
                avg= int(round((r + g + b)/3.0))
                R, G, B= avg+100, avg+50, avg
                sepiaData.append((R, G, B))
        canvas.data.image.putdata(sepiaData)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)
        
def keyPressed(canvas, event):
    if event.keysym=="z":
        undo(canvas)
    elif event.keysym=="y":
        redo(canvas)


def undo(canvas):
    if len(canvas.data.undoQueue)>0:
       
        lastImage=canvas.data.undoQueue.pop()
       
    if len(canvas.data.undoQueue)>0:
        
        canvas.data.image=canvas.data.undoQueue[-1]
    save(canvas)
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

def redo(canvas):
    if len(canvas.data.redoQueue)>0:
        canvas.data.image=canvas.data.redoQueue[0]
    save(canvas)
    if len(canvas.data.redoQueue)>0:
        
        lastImage=canvas.data.redoQueue.popleft()
        canvas.data.undoQueue.append(lastImage)
    canvas.data.imageForTk=makeImageForTk(canvas)
    drawImage(canvas)

############# MENU COMMANDS ################

def saveAs(canvas):
    
    if canvas.data.image!=None:
        filename=asksaveasfilename(defaultextension=".jpg")
        im=canvas.data.image
        im.save(filename)

def save(canvas):
    if canvas.data.image!=None:
        im=canvas.data.image
        im.save(canvas.data.imageLocation)

def newImage(canvas):
    imageName=askopenfilename()
    filetype=""
    
    try: filetype=imghdr.what(imageName)
    except:
        messagebox.showinfo(title="Image File",\
        message="Choose an Image File!" , parent=canvas.data.mainWindow)
   
    
    if filetype in ['jpeg', 'bmp', 'png', 'tiff','jpg']:
        canvas.data.imageLocation=imageName
        print(imageName)
        im = Image.open(imageName)
        canvas.data.image=im
        canvas.data.originalImage=im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize=im.size 
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)
    else:
        messagebox.showinfo(title="Image File",\
        message="Choose an Image File!" , parent=canvas.data.mainWindow)

######## CREATE A VERSION OF IMAGE TO BE DISPLAYED ON THE CANVAS #########

def makeImageForTk(canvas):
    im=canvas.data.image
    if canvas.data.image!=None:
        
        imageWidth=canvas.data.image.size[0] 
        imageHeight=canvas.data.image.size[1]
        
        if imageWidth>imageHeight:
            resizedImage=im.resize((canvas.data.width,\
                int(round(float(imageHeight)*canvas.data.width/imageWidth))))
            
            canvas.data.imageScale=float(imageWidth)/canvas.data.width
        else:
            resizedImage=im.resize((int(round(float(imageWidth)*canvas.data.height/imageHeight)),\
                                    canvas.data.height))
            canvas.data.imageScale=float(imageHeight)/canvas.data.height
       
        canvas.data.resizedIm=resizedImage
        return ImageTk.PhotoImage(resizedImage)
 
def drawImage(canvas):
    if canvas.data.image!=None:
        
        canvas.create_image(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0,
                        canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0,
                            anchor=NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX=int(round(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0))
        canvas.data.imageTopY=int(round(canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0))

############ INITIALIZE ##############

def init(root, canvas):

    buttonsInit(root, canvas)
    menuInit(root, canvas)
    canvas.data.image=None
    canvas.data.angleSelected=None
    canvas.data.rotateWindowClose=False
    canvas.data.brightnessWindowClose=False
    canvas.data.brightnessLevel=None
    canvas.data.histWindowClose=False
    canvas.data.solarizeWindowClose=False
    canvas.data.posterizeWindowClose=False
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.endCrop=False
    canvas.data.drawOn=True
    
    canvas.data.undoQueue=deque([], 10)
    canvas.data.redoQueue=deque([], 10)
    canvas.pack()


def buttonsInit(root, canvas):
    backgroundColour="white"
    buttonWidth=40
    buttonHeight=2
    toolKitFrame=Frame(root)
    cropButton=Button(toolKitFrame, text="Crop",\
                      background=backgroundColour ,\
                      width=buttonWidth, height=buttonHeight, \
                      command=lambda:crop(canvas))
    cropButton.grid(row=0,column=0)
    
    mirrorButton=Button(toolKitFrame, text="Flip Horizontal",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        command=lambda: mirror(canvas))
    mirrorButton.grid(row=5,column=0)
    flipButton=Button(toolKitFrame, text="Flip Vertical",\
                      background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight, \
                      command=lambda: flip(canvas))
    flipButton.grid(row=6,column=0)
    transposeButton=Button(toolKitFrame, text="Transpose",\
                           background=backgroundColour, width=buttonWidth,\
                           height=buttonHeight,command=lambda: transpose(canvas))
    transposeButton.grid(row=7,column=0)
   
    resetButton=Button(toolKitFrame, text="Reset",\
                       background=backgroundColour ,width=buttonWidth,\
                       height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=9,column=0)
    
    toolKitFrame.pack(side=RIGHT)

    
def menuInit(root, canvas):
    menubar=Menu(root)
    menubar.add_command(label="New", command=lambda:newImage(canvas))
    menubar.add_command(label="Save", command=lambda:save(canvas))
    menubar.add_command(label="Save As", command=lambda:saveAs(canvas))
    
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Undo   Z", command=lambda:undo(canvas))
    editmenu.add_command(label="Redo   Y", command=lambda:redo(canvas))
    menubar.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menubar)
    
    filtermenu = Menu(menubar, tearoff=0)
    filtermenu.add_command(label="Black and White", \
                           command=lambda:covertGray(canvas))
   
    filtermenu.add_command(label="Invert", \
                           command=lambda:invert(canvas))

    filtermenu.add_command(label="Sepia",\
                           command=lambda:sepia(canvas))
    
    menubar.add_cascade(label="Filter", menu=filtermenu)
    root.config(menu=menubar)
    


def run():
    
    root = Tk()
    root.title("Image Editor")
    canvasWidth=1000
    canvasHeight=700
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight, \
                    background="gray")
    
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=canvasWidth
    canvas.data.height=canvasHeight
    canvas.data.mainWindow=root
    init(root, canvas)
    root.bind("<Key>", lambda event:keyPressed(canvas, event))
    
    root.mainloop()  


run()

