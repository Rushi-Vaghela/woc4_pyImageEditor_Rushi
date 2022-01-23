from tkinter import Frame, Button,LEFT

class EditBar(Frame):

    def __init__(self, master=None):
        Frame.__init__(master=master)

        self.new_button = Button(self, text="New")
        self.save_button = Button(self, text="Save")
        self.save_as_button = Button(self, text="Save As")
        self.draw_button = Button(self, text="Draw")
        self.crop_button = Button(self, text="Crop")
        self.filter_button = Button(self, text="Filter")
        self.adjust_button = Button(self, text="Adjust")
        self.clear_button = Button(self, text="Clear")
