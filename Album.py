import os
import sys
from PIL import Image
import glob
import tkinter
from PIL import ImageTk
from shutil import copyfile


class AlbumSelector:

    currentEvent = None

    def __init__(self, src, tgt):
        self.src = src
        self.tgt = tgt
        self.files = glob.glob(self.src)
        self.curIdx = 0
        self.window = tkinter.Tk()
        self.window.bind("<Key>", self.key_press)
        self.display()

    # keys
    def key_press(self, event):
        self.currentEvent = event
        print(repr(self.currentEvent.keysym))
        if self.currentEvent.keysym == 'q':
            exit(1)
        if self.currentEvent.keysym == 'Right':
            self.move_forward()
        if self.currentEvent.keysym == 'Left':
            self.move_back()
        if self.currentEvent.keysym == 'Down':
            self.copy()

    def move_forward(self):
        if self.curIdx + 1 < len(self.files):
            self.currentEvent.widget.quit()
            self.curIdx += 1
            self.display()

    def move_back(self):
        if self.curIdx - 1 >= 0:
            self.currentEvent.widget.quit()
            self.curIdx -= 1
            self.display()

    def copy(self):
        s = self.files[self.curIdx]
        t = self.tgt + "/" + os.path.basename(self.files[self.curIdx])
        print("saving {} to {} ".format(s, t))
        copyfile(s, t)

    def display(self):
        f = self.files[self.curIdx]
        print(f)
        self.window.title(f)
        photo = Image.open(f)
        tk_photo = ImageTk.PhotoImage(photo)
        self.window.geometry("{}x{}+100+100".format(photo.size[0], photo.size[1]))
        image_widget = tkinter.Label(self.window, image=tk_photo)
        image_widget.place(x=0, y=0, width=photo.size[0], height=photo.size[1])
        self.wait_for_input()

    def wait_for_input(self):
        self.window.mainloop()


sel = AlbumSelector("/users/andreigoldfain/Downloads/*.jpg", "/users/andreigoldfain/Downloads/phav")