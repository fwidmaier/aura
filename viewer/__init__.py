from tkinter import *
from PIL import ImageTk, Image
import sys


class Viewer(Tk):
    def __init__(self, ex, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ca = False
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.panel = Label(self)
        # self.panel.image = img
        self.ex = ex
        self.panel.pack(side="bottom", fill="both", expand="yes")
        # self.update()

    def update(self, img):
        if self.ca:
            return
        img = ImageTk.PhotoImage(img)
        self.panel.configure(image=img)
        self.panel.image = img
        self.panel.update()

    def close_window(self):
        self.ca = True
        for f in self.ex:
            try:
                f.cancel()
            except Exception as e:
                print(e)
        self.destroy()
        sys.exit(0)