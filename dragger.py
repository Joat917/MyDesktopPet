if 'tk' not in globals():
    import tkinter as tk

class Dragger():
    "Drag the window whenever mouse is down. \
Also provides whether the mouse is down. "

    def __init__(self, main) -> None:
        self.main = main
        self._md = False
        main.root.bind("<Button-1>", self.onclick)
        main.root.bind("<B1-Motion>", self.ondrag)
        main.root.bind("<ButtonRelease-1>", self.onrelease)
        pass

    def onclick(self, event):
        self.x, self.y = event.x, event.y
        self._md = True

    def ondrag(self, event):
        self.main.move(event.x-self.x, event.y-self.y)

    def onrelease(self, event):
        self._md = False

    @property
    def mousedown(self):
        return self._md