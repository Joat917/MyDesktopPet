if 'tk' not in globals():
    import tkinter as tk

class MenuBar():
    "A menubar activated when right click"

    def __init__(self, root, d) -> None:
        "d: dict[str, function]; function canbe None"
        assert isinstance(d, dict)
        self.root=root
        # create a menubar
        self.menuBar = tk.Menu(self.root, tearoff=False)
        # add buttons to menubar
        for t, f in d.items():
            if f is None:
                self.menuBar.add_separator()
            else:
                self.menuBar.add_command(label=t, command=f)
        # add mouseEvent
        self.root.bind('<Button-3>', self.oncontextMenu)

    def oncontextMenu(self, event):
        "event: ButtonPress event"
        # place the menubar according to the mouseEvent
        self.menuBar.post(event.x_root, event.y_root)

