import tkinter as tk
if 'RESOURCES' not in globals():
    from resources import RESOURSES
from rect import Rect


class SpeechBubble:
    def __init__(self, pet, text, timeout=3) -> None:
        self.pet = pet
        self.root = tk.Tk()
        # Window be transparent
        self.root.wm_attributes('-transparent', 'black')
        # window on top
        self.root.attributes('-topmost', True)
        # window not resizable
        self.root.resizable(False, False)
        # hide title and icon
        self.root.overrideredirect(True)
        # widget : text container
        self.label = tk.Label(self.root, border=0, background='black')
        self.im = RESOURSES.getBubble(self, text, self.root)
        self.label.config(image=self.im)
        self.label.place(x=0, y=0)
        # obtain position
        self.rect = Rect(self.root, self.im.width(), self.im.height(),
                         self.pet.rect.right, self.pet.rect.top)
        # hide if this count become zero
        self.onlineWordCount = 0
        # display
        self.root.geometry(self.rect.as_geometry())
        self.show(timeout=timeout)
        pass

    def rePosition(self):
        # obtain position
        self.rect = Rect(self.root, self.im.width(), self.im.height(),
                         self.pet.rect.right, self.pet.rect.top)
        # display
        self.root.geometry(self.rect.as_geometry())

    def reText(self, text, timeout=3):
        self.im = RESOURSES.getBubble(self, text, self.root)
        self.label.config(image=self.im)
        # obtain position
        self.rect.width = self.im.width()
        self.rect.height = self.im.height()
        # display
        self.root.geometry(self.rect.as_geometry())
        self.show(timeout=timeout)
        

    def hide(self):
        self.onlineWordCount -= 1
        if self.onlineWordCount <= 0:
            self.onlineWordCount = 0
            self.root.attributes('-alpha', 0)

    def show(self, timeout=3):
        self.root.attributes('-alpha', 1)
        if timeout > 0:
            self.onlineWordCount += 1
            self.root.after(timeout*1000, self.hide)
