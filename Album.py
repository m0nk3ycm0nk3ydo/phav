import os
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
        self.curImg = None
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
        self.window.title(f)
        self.clear()

        photo = Image.open(f)
        print("screen {},{}".format(self.window.winfo_screenwidth(),  self.window.winfo_screenheight()))
        print("photo  {},{}".format(photo.size[0], photo.size[1]))

        photo = self.resize_to_screen(photo)
        tk_photo = ImageTk.PhotoImage(photo)
        self.window.geometry("%dx%d+0+0" % (self.window.winfo_screenwidth(),  self.window.winfo_screenheight()))
        self.curImg = tkinter.Label(self.window, image=tk_photo)
        self.curImg.place(x=0, y=0, width=photo.size[0], height=photo.size[1])
        self.wait_for_input()

    def clear(self):
        if self.curImg:
            self.curImg.pack_forget()
            self.curImg.destroy()

    def resize_to_screen(self, photo):
        screen_width, screen_height = self.window.winfo_screenwidth(), self.window.winfo_screenheight()
        photo_width, photo_height = photo.size[0], photo.size[1]

        if photo_width >= photo_height:
            if photo_width <= screen_width and photo_height <= screen_height:
                return photo
            wr = screen_width / photo_width
            hr = screen_height / photo_height
        else:
            if photo_height <= screen_height and photo_width <= screen_width:
                return photo
            wr = screen_height / photo_width
            hr = screen_width / photo_height

        resize_ratio = min(wr, hr)
        new_width = photo_width * resize_ratio
        new_height = photo_height * resize_ratio

        return photo.resize((int(new_width), int(new_height)))

    def wait_for_input(self):
        self.window.mainloop()


sel = AlbumSelector("/Users/andreigoldfain/Documents/img-test/*.JPG", "/users/andreigoldfain/Documents/imgsave")
