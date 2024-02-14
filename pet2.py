import tkinter as tk
import os
import sys
import traceback
import random
try:
    import tkinterDnD as tkdnd
except ImportError:
    os.system("pip install python-tkdnd -i https://pypi.tuna.tsinghua.edu.cn/simple")
    os.system(f"start {__file__}")
    sys.exit()

# self-defined functions
from rect import Rect
from resources import RESOURSES
from dragger import Dragger
from menuBar import MenuBar
from speechBubble import SpeechBubble
from say2Me import Say2Me
from digestFile import digestFileProc


class Pet:
    "A pet with its window"
    petNames = set()

    def __init__(self, imageName=None) -> None:
        if imageName is None:
            # random file, but cannot repeat.
            _choi = set(list(RESOURSES.images.keys())
                        ).difference(self.petNames)
            if not len(_choi):
                raise RuntimeError("All friends are here. ")
            imageName = random.choice(list(_choi))
        self.imageName = imageName
        self.petNames.add(self.imageName)
        # use tkdnd instead of tk, reference: https://pypi.org/project/python-tkdnd/
        self.root = tkdnd.Tk()
        # Window be transparent
        self.root.wm_attributes('-transparent', 'black')
        # window on top
        self.root.attributes('-topmost', True)
        # window not resizable
        self.root.resizable(False, False)
        # hide title and icon
        self.root.overrideredirect(True)

        # bind events
        self.root.bind("<Button-1>", self.onclick)
        self.root.bind("<Button-3>", self.oncontextMenu)
        self.root.bind("<Key>", self.onkey)

        # widget the pet: no border, black background
        self.label = tk.ttk.Label(self.root, border=0,
                                  background='black', ondrop=self.ondrop)
        im = RESOURSES.getImage(imageName, (300, 300))
        self.label.config(
            image=RESOURSES.getPhotoImage(im, self, self.root))
        self.label.place(x=0, y=0)

        # show the window
        self.rect = Rect(self.root, im.width, im.height, -400, -400)
        self.root.geometry(self.rect.as_geometry())

        # functions
        self.dragger = Dragger(self)
        self.speechBubble = SpeechBubble(self, 'Hello!')
        self.rightClickMenu = MenuBar(self.root, {
            'Grow': lambda: self.changeSize(1),
            'Shrink': lambda: self.changeSize(-1),
            'sep1': None,
            'Say to me...': lambda: Say2Me(self),
            'Shut up!': lambda: (self.speechBubble.__setattr__("onlineWordCount", 0)
                                 or self.speechBubble.hide()),
            'sep2': None,
            'Call my friend': lambda: Pet(),
            'sep3': None,
            'Quit': self.quit,
            'QuitAll': self.quitAll, })

        # key event specified to <say2me> part
        self.say2meKeyFunc = lambda ev: None
        pass

    def move(self, dx=0, dy=0):
        old_rect = tuple(self.rect)
        self.rect.left += dx
        self.rect.top += dy
        if tuple(self.rect) != old_rect:
            self.root.geometry(self.rect.as_geometry())
            self.speechBubble.rePosition()

    def changeSize(self, direction):
        "direction: +1, bigger; -1, smaller"
        if direction > 0:
            if self.rect.width >= 100 and self.rect.height >= 100:
                newSize = (int(self.rect.width*1.2), int(self.rect.height*1.2))
            else:
                newSize = (int(self.rect.width+20), int(self.rect.height+20))
            if (newSize[0] > self.root.winfo_screenwidth()*0.9
                    or newSize[1] > self.root.winfo_screenheight()*0.9):
                return
        elif direction < 0:
            if self.rect.width > 100 and self.rect.height > 100:
                newSize = (int(self.rect.width/1.2), int(self.rect.height/1.2))
            else:
                newSize = (int(self.rect.width-20), int(self.rect.height-20))
            if (newSize[0] < 30
                    or newSize[1] < 30):
                return
        else:
            return

        ph = RESOURSES.getPhotoImage(
            RESOURSES.getImage(self.imageName, newSize), self, self.root)
        self.label.config(image=ph)
        self.rect.width = ph.width()
        self.rect.height = ph.height()
        self.root.geometry(self.rect.as_geometry())
        self.speechBubble.rePosition()

    def onclick(self, event):
        self.speechBubble.reText("Play with me. ")
        pass

    def oncontextMenu(self, event):
        pass

    def onkey(self, event):
        # print(event)
        self.say2meKeyFunc(event)
        pass

    def ondrop(self, event):
        # print(event.data)
        if os.path.exists(event.data):
            if os.path.isfile(event.data):
                # ask for respond
                self.speechBubble.reText("Can I eat this file?", 0)
                t0 = False

                def eat(ev):
                    # responded
                    print(ev)
                    nonlocal t0
                    if ev.keysym in 'Yy':
                        print(ev)
                        self.root.after(0, digestFileProc, (event.data))
                        self.speechBubble.reText(":)")
                        t0 = True
                        self.say2meKeyFunc = lambda e: None
                    elif ev.keysym in 'Nn':
                        print(ev)
                        self.speechBubble.reText(":(")
                        t0 = True
                        self.say2meKeyFunc = lambda e: None
                    else:
                        self.say2meKeyFunc = eat

                def fin():
                    #not responding, timeout
                    if not t0:
                        self.say2meKeyFunc = lambda ev: None
                        self.speechBubble.reText("~~(o> A <o)~~")
                self.root.after(5000, fin)
                self.say2meKeyFunc = eat
            elif os.path.isdir(event.data):
                self.speechBubble.reText("I cannot eat a folder yet...")
            else:
                self.speechBubble.reText("What's this?")
        else:
            self.speechBubble.reText(
                "I can't find what\n you have mentioned. ")

    def quit(self):
        try:
            self.petNames.remove(self.imageName)
        except KeyError:
            pass
        self.speechBubble.root.destroy()
        self.root.destroy()

    def quitAll(self):
        self.quit()
        sys.exit(0)

if __name__=="__main__":
    p=Pet("f1")
    tk.mainloop()
