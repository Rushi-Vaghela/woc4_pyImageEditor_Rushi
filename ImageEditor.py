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

################ DRAW ################

def drawOnImage(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=True
    drawWindow=Toplevel(canvas.data.mainWindow)
    drawWindow.title="Draw"
    drawFrame=Frame(drawWindow)
    redButton=Button(drawFrame, bg="red", width=2, \
                     command=lambda: colourChosen(drawWindow,canvas, "red"))
    redButton.grid(row=0,column=0)
    blueButton=Button(drawFrame, bg="blue", width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "blue"))
    blueButton.grid(row=0,column=1)
    greenButton=Button(drawFrame, bg="green",width=2, \
                       command=lambda: colourChosen(drawWindow,canvas, "green"))
    greenButton.grid(row=0,column=2)
    magentaButton=Button(drawFrame, bg="magenta", width=2,\
                         command=lambda: colourChosen(drawWindow,canvas, "magenta"))
    magentaButton.grid(row=1,column=0)
    cyanButton=Button(drawFrame, bg="cyan", width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "cyan"))
    cyanButton.grid(row=1,column=1)
    yellowButton=Button(drawFrame, bg="yellow",width=2,\
                        command=lambda: colourChosen(drawWindow,canvas, "yellow"))
    yellowButton.grid(row=1,column=2)
    orangeButton=Button(drawFrame, bg="orange", width=2,\
                        command=lambda: colourChosen(drawWindow,canvas, "orange"))
    orangeButton.grid(row=2,column=0)
    purpleButton=Button(drawFrame, bg="purple",width=2, \
                        command=lambda: colourChosen(drawWindow,canvas, "purple"))
    purpleButton.grid(row=2,column=1)
    brownButton=Button(drawFrame, bg="brown",width=2,\
                       command=lambda: colourChosen(drawWindow,canvas, "brown"))
    brownButton.grid(row=2,column=2)
    blackButton=Button(drawFrame, bg="black",width=2,\
                       command=lambda: colourChosen(drawWindow,canvas, "black"))
    blackButton.grid(row=3,column=0)
    whiteButton=Button(drawFrame, bg="white",width=2, \
                       command=lambda: colourChosen(drawWindow,canvas, "white"))
    whiteButton.grid(row=3,column=1)
    grayButton=Button(drawFrame, bg="gray",width=2,\
                      command=lambda: colourChosen(drawWindow,canvas, "gray"))
    grayButton.grid(row=3,column=2)
    drawFrame.pack(side=BOTTOM)


def colourChosen(drawWindow, canvas, colour):
    if canvas.data.image!=None:
        canvas.data.drawColour=colour
        canvas.data.mainWindow.bind("<B1-Motion>",\
                                    lambda event: drawDraw(event, canvas))
    drawWindow.destroy()
    

def drawDraw(event, canvas):
    if canvas.data.drawOn==True:
        x=float(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
        y=float(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
        draw = ImageDraw.Draw(canvas.data.image)
        draw.ellipse((x-3, y-3, x+3, y+3), fill=canvas.data.drawColour,\
                    outline=None )
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=makeImageForTk(canvas)
        drawImage(canvas)

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

def closeBrightnessWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.brightnessWindowClose=True

def changeBrightness(canvas, brightnessWindow, brightnessSlider, \
                     previousVal):
    if canvas.data.brightnessWindowClose==True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose=False
        
    else:
        # increasing pixel values according to slider value increases
        #brightness we change ot according to the difference between the
        # previous value and the current slider value
        if canvas.data.image!=None and brightnessWindow.winfo_exists():
            sliderVal=brightnessSlider.get()
            scale=(sliderVal-previousVal)/100.0
            canvas.data.image=canvas.data.image.point(\
                lambda i: i+ int(round(i*scale)))  
            canvas.data.imageForTk=makeImageForTk(canvas)
            drawImage(canvas)
            canvas.after(200, \
            lambda: changeBrightness(canvas, brightnessWindow, \
                                     brightnessSlider, sliderVal))

       
def brightness(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    brightnessWindow=Toplevel(canvas.data.mainWindow)
    brightnessWindow.title("Brightness")
    brightnessSlider=Scale(brightnessWindow, from_=-100, to=100,\
                           orient=HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame=Frame(brightnessWindow)
    OkBrightnessButton=Button(OkBrightnessFrame, text="OK", \
                              command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0,column=0)
    OkBrightnessFrame.pack(side=BOTTOM)
    changeBrightness(canvas, brightnessWindow, brightnessSlider,0)
    brightnessSlider.set(0)

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
        #print(PIL.ImageOps.invert(canvas.data.image))
        canvas.data.image=PIL.ImageOps.invert(canvas.data.image.convert('RGB'))
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

def solarize(canvas):
    canvas.data.colorPopToHappen=False
    canvas.data.colorPopToHappen=False
    solarizeWindow=Toplevel(canvas.data.mainWindow)
    solarizeWindow.title("Solarize")
    solarizeSlider=Scale(solarizeWindow, from_=0, to=255, orient=HORIZONTAL)
    solarizeSlider.pack()
    OkSolarizeFrame=Frame(solarizeWindow)
    OkSolarizeButton=Button(OkSolarizeFrame, text="OK",\
                            command=lambda: closeSolarizeWindow(canvas))
    OkSolarizeButton.grid(row=0, column=0)
    OkSolarizeFrame.pack(side=BOTTOM)
    performSolarize(canvas, solarizeWindow, solarizeSlider, 255)

def performSolarize(canvas, solarizeWindow, solarizeSlider, previousThreshold):
    if canvas.data.solarizeWindowClose==True:
        solarizeWindow.destroy()
        canvas.data.solarizeWindowClose=False
        
    else:
        # the  slider denotes the % of solarization thta the user wants,
        # so the threshold (above which pixels are inverted) is inversely
        # related to the slider value
        if solarizeWindow.winfo_exists():
            sliderVal=solarizeSlider.get()
            threshold_=255-sliderVal
            if canvas.data.image!=None and threshold_!=previousThreshold:
                canvas.data.image=ImageOps.solarize(canvas.data.image,\
                                                    threshold=threshold_)
                canvas.data.imageForTk=makeImageForTk(canvas)
                drawImage(canvas)
            canvas.after(200, lambda: performSolarize(canvas, \
                                solarizeWindow, solarizeSlider, threshold_))

def closeSolarizeWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.solarizeWindowClose=True
    
def posterize(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    # we basically reduce the range of colurs from 256 to 5 bits
    # and so, assign a single new value to each colour value
    # in each succesive range
    posterData=[]
    if canvas.data.image!=None:
        for col in range(canvas.data.imageSize[1]):
            for row in range(canvas.data.imageSize[0]):
                r, g, b= canvas.data.image.getpixel((row, col))
                if r in range(32):
                    R=0
                elif r in range(32, 96):
                    R=64
                elif r in range(96, 160):
                    R=128
                elif r in range(160, 224):
                    R=192
                elif r in range(224,256):
                    R=255
                if g in range(32):
                    G=0
                elif g in range(32, 96):
                    G=64
                elif g in range(96, 160):
                    G=128
                elif r in range(160, 224):
                    g=192
                elif r in range(224,256):
                    G=255
                if b in range(32):
                    B=0
                elif b in range(32, 96):
                    B=64
                elif b in range(96, 160):
                    B=128
                elif b in range(160, 224):
                    B=192
                elif b in range(224,256):
                    B=255
                posterData.append((R, G, B))
        canvas.data.image.putdata(posterData)
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

    brightnessButton=Button(toolKitFrame, text="Brightness",\
                            background=backgroundColour ,\
                            width=buttonWidth, height=buttonHeight,\
                            command=lambda: brightness(canvas))
    brightnessButton.grid(row=1 ,column=0)
    
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
    
    transposeButton=Button(toolKitFrame, text="Rotate",\
                           background=backgroundColour, width=buttonWidth,\
                           height=buttonHeight,command=lambda: transpose(canvas))
    transposeButton.grid(row=7,column=0)

    drawButton=Button(toolKitFrame, text="Draw",\
                      background=backgroundColour ,width=buttonWidth,\
                      height=buttonHeight,command=lambda: drawOnImage(canvas))
    drawButton.grid(row=8,column=0)

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

    filtermenu.add_command(label="Solarize",\
                           command=lambda:solarize(canvas))

    filtermenu.add_command(label="Posterize",\
                            command=lambda:posterize(canvas))
    
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

